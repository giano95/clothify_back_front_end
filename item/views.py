from django.shortcuts import render, redirect
from item.models import Item, ItemImage, ItemQuantitySize
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.forms import modelformset_factory
from django.template import RequestContext
from item.forms import ItemForm, ItemImageForm, ItemQuantitySizeForm
from core.views import is_sub_seller, is_unsub_seller
from django.views.generic import View, DetailView


class ItemView(DetailView):
    model = Item
    template_name = 'item.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ItemView, self).get_context_data(*args, **kwargs)

        context['images'] = ItemImage.objects.filter(item=self.object)
        context['similar_posts'] = Item.objects.filter(
            category=self.object.category).exclude(id=self.object.id)[:4]
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_sub_seller), name='dispatch')
class AddView(View):
    def get(self, *args, **kwargs):
        ItemImageFormSet = modelformset_factory(
            ItemImage, form=ItemImageForm, extra=3)
        formset = ItemImageFormSet(queryset=ItemImage.objects.none())
        ItemQuantitySizeFormSet = modelformset_factory(
            ItemQuantitySize, form=ItemQuantitySizeForm, extra=6)
        formset2 = ItemQuantitySizeFormSet(
            queryset=ItemQuantitySize.objects.none())
        itemForm = ItemForm()
        return render(
            self.request,
            'post_form.html',
            {
                'itemForm': itemForm,
                'formset': formset,
                'formset2': formset2
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
            item.quantity_size.set(item_quantity_sizes)
            item.images.set(images)
            item.save()
            return redirect('core:home')
        else:
            print(itemForm.errors, formset.errors)
        return render(self.request, 'post_form.html', {'itemForm': itemForm, 'formset': formset}, content_type=RequestContext(self.request))
