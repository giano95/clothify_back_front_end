from django.shortcuts import render, redirect
from item.models import Item, ItemImage, ItemQuantitySize, ItemSize
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.forms import modelformset_factory
from django.template import RequestContext
from item.forms import ItemForm, ItemImageForm, ItemQuantitySizeForm, ItemReviewForm
from core.views import is_sub_seller, is_unsub_seller
from django.views.generic import View, DetailView
import datetime
import json
from django.core import serializers
import itertools


class ItemView(DetailView):
    model = Item
    template_name = 'item.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ItemView, self).get_context_data(*args, **kwargs)
        context['images'] = ItemImage.objects.filter(item=self.object)
        context['similar_posts'] = Item.objects.filter(
            category=self.object.category).exclude(id=self.object.id)[:4]
        context['itemReviewForm'] = ItemReviewForm()
        return context

    def post(self, *args, **kwargs):

        itemReviewForm = ItemReviewForm(
            self.request.POST or None,
            self.request.FILES or None
        )

        if itemReviewForm.is_valid():

            itemReview = itemReviewForm.save(commit=False)
            itemReview.user = self.request.user
            itemReview.item = self.get_object()
            itemReview.date = datetime.date.today()
            itemReview.save()

            return redirect('item:item', pk=kwargs['pk'])
        else:
            print(itemReviewForm.errors)

        return render(self.request, 'item.html', {'itemReviewForm': itemReviewForm}, content_type=RequestContext(self.request))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_sub_seller), name='dispatch')
class AddView(View):
    def get(self, *args, **kwargs):

        sizes = ItemSize._meta.get_field('tag').choices

        ItemImageFormSet = modelformset_factory(
            ItemImage, form=ItemImageForm, extra=3)
        formset = ItemImageFormSet(queryset=ItemImage.objects.none())
        ItemQuantitySizeFormSet = modelformset_factory(
            ItemQuantitySize, form=ItemQuantitySizeForm, extra=6)
        formset2 = ItemQuantitySizeFormSet(
            queryset=ItemQuantitySize.objects.none())
        itemForm = ItemForm()

        list_formset2 = list(itertools.zip_longest(formset2, sizes))

        return render(
            self.request,
            'post_form.html',
            {
                'itemForm': itemForm,
                'formset': formset,
                'formset2': formset2,
                'list_formset2': list_formset2,
            },
            content_type=RequestContext(self.request)
        )

    def post(self, *args, **kwargs):
        itemForm = ItemForm(self.request.POST or None,
                            self.request.FILES or None)
        ItemImageFormSet = modelformset_factory(
            ItemImage, form=ItemImageForm, extra=3)
        formset = ItemImageFormSet(
            self.request.POST, self.request.FILES, queryset=ItemImage.objects.none())
        ItemQuantitySizeFormSet = modelformset_factory(
            ItemQuantitySize, form=ItemQuantitySizeForm, extra=6)
        formset2 = ItemQuantitySizeFormSet(
            self.request.POST, queryset=ItemQuantitySize.objects.none())

        if itemForm.is_valid() and formset.is_valid() and formset2.is_valid():

            item = itemForm.save(commit=False)
            item.owner = self.request.user
            item.save()
            itemForm.save_m2m()

            images = []
            for form in formset.cleaned_data:
                if (form):
                    image = ItemImage(image=form['image'])
                    image.save()
                    images.append(image)
                else:
                    break
            item_quantity_sizes = []
            for form in formset2.cleaned_data:
                if (form):
                    item_quantity_size = ItemQuantitySize(
                        size=form['size'],
                        quantity=form['quantity']
                    )
                    item_quantity_size.save()
                    item_quantity_sizes.append(item_quantity_size)
                else:
                    break
            item.quantities_size.set(item_quantity_sizes)
            item.images.set(images)
            item.save()
            return redirect('core:home')
        else:
            print(itemForm.errors, formset.errors, formset2.errors)
        return render(self.request, 'post_form.html', {'itemForm': itemForm, 'formset': formset, 'formset2': formset2}, content_type=RequestContext(self.request))


@method_decorator(login_required, name='dispatch')
class DeleteView(View):

    def get(self, *args, **kwargs):
        item = Item.objects.get(id=self.kwargs['pk'])
        if(item.owner == self.request.user):
            item.delete()

        return redirect('core:home')


@method_decorator(login_required, name='dispatch')
class UpdateView(View):

    def get(self, *args, **kwargs):

        item = Item.objects.get(id=self.kwargs['pk'])

        sizes = ItemSize._meta.get_field('tag').choices
        itemImage = item.images.all()
        itemQuantitySize = item.quantities_size.all()

        sizes_dict = {"sizes": [x[0] for x in sizes]}

        sizes_json = json.dumps(sizes_dict)
        images_json = serializers.serialize('json', itemImage)
        qntsz_json = serializers.serialize('json', itemQuantitySize)

        itemForm = ItemForm(instance=item)

        extra_image = 3 - item.images.all().count()
        ItemImageFormSet = modelformset_factory(
            ItemImage, form=ItemImageForm, extra=extra_image)
        formset = ItemImageFormSet(
            queryset=item.images.all(), prefix='images')

        extra_qntsz = 6 - item.quantities_size.all().count()
        ItemQuantitySizeFormSet = modelformset_factory(
            ItemQuantitySize, form=ItemQuantitySizeForm, extra=extra_qntsz)
        formset2 = ItemQuantitySizeFormSet(
            queryset=item.quantities_size.all(), prefix='qntsz')

        return render(
            self.request,
            'item-update.html',
            {
                'itemForm': itemForm,
                'formset': formset,
                'formset2': formset2,
                'sizes_json': sizes_json,
                'images_json': images_json,
                'qntsz_json': qntsz_json,
            },
            content_type=RequestContext(self.request)
        )

    def post(self, *args, **kwargs):

        old = Item.objects.get(id=self.kwargs['pk'])

        itemForm = ItemForm(self.request.POST or None,
                            self.request.FILES or None, instance=old)

        extra_image = 3 - old.images.all().count()
        ItemImageFormSet = modelformset_factory(
            ItemImage, form=ItemImageForm, extra=0)
        formset = ItemImageFormSet(
            self.request.POST or None, self.request.FILES or None, queryset=old.images.all(), prefix='images')

        extra_qntsz = 6 - old.quantities_size.all().count()
        ItemQuantitySizeFormSet = modelformset_factory(
            ItemQuantitySize, form=ItemQuantitySizeForm, extra=extra_qntsz)
        formset2 = ItemQuantitySizeFormSet(
            self.request.POST or None, queryset=old.quantities_size.all(), prefix='qntsz')

        if itemForm.is_valid() and formset2.is_valid() and formset.is_valid():

            item = itemForm.save(commit=False)
            item.owner = self.request.user
            item.save()
            itemForm.save_m2m()

            images = []
            for form in formset.cleaned_data:
                if (form):
                    image = ItemImage(image=form['image'])
                    image.save()
                    images.append(image)
                else:
                    break
            item_quantity_sizes = []
            for form in formset2.cleaned_data:
                if (form):
                    item_quantity_size = ItemQuantitySize(
                        size=form['size'],
                        quantity=form['quantity']
                    )
                    item_quantity_size.save()
                    item_quantity_sizes.append(item_quantity_size)
                else:
                    break
            item.quantities_size.set(item_quantity_sizes)
            item.images.set(images)
            item.save()
            return redirect('item:item', pk=self.kwargs['pk'])
        else:
            print(itemForm.errors, formset.errors, formset2.errors)
        return render(
            self.request,
            'item-update.html',
            {
                'itemForm': itemForm,
                'formset': formset,
                'formset2': formset2
            },
            content_type=RequestContext(self.request)
        )
