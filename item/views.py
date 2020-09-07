from django.shortcuts import render, redirect, get_object_or_404
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
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView, Response
from rest_framework.mixins import UpdateModelMixin
from rest_framework.generics import GenericAPIView, UpdateAPIView
from item.models import *
from item.serializers import *


# GET all the items
class GetAllItemsAPI(APIView):
    
    def get(self, request, format=None):

        queryset = Item.objects.all()
        serializer = GetItemSerializer(queryset, many=True)
        return Response(serializer.data)


# GET a signle item from his id
class GetItemByIdAPI(APIView):

    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        if not item:
            return Response({"Message" : "Oggetto non presente"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = GetItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# GET items filtered by a query
class GetQueryItemAPI(generics.ListCreateAPIView):

    serializer_class = GetItemSerializer

    def get_queryset(self):
        

        # by default we take all the instances
        queryset = Item.objects.all().distinct()


        # --- REUSED CODE FROM: core.views.py ---
        context = {}
        context['categories'] = ItemCategory.objects.all()
        context['colors'] = [color[0] for color in ItemColor.CHOICES]
        context['sizes'] = [size[0] for size in ItemSize.CHOICES]
        category_name = (self.request.query_params.get('category_name') or None)
        if category_name:
            context['category_name'] = category_name.split(",")[:-1]
        context['query_text'] = (self.request.query_params.get('query_text') or None)
        reviews_vote = (self.request.query_params.get('reviews_vote') or None)
        if reviews_vote:
            context['reviews_vote'] = int(reviews_vote)
        from_price = (self.request.query_params.get('from_price') or None)
        if from_price:
            context['from_price'] = int(from_price)
        to_price = (self.request.query_params.get('to_price') or None)
        if to_price:
            context['to_price'] = int(to_price)
        colors_name = (self.request.query_params.get('colors_name') or None)
        if colors_name:
            context['colors_name'] = colors_name.split(",")[:-1]
        sizes_tag = (self.request.query_params.get('sizes_tag') or None)
        if sizes_tag:
            context['sizes_tag'] = sizes_tag.split(",")[:-1]

        # Filter by the category
        category_name = (self.request.GET.get('category_name') or None)
        if category_name:
            category_name = category_name.split(",")[:-1]

            items = Item.objects.all().filter(
                category__name__in=category_name).distinct()
            queryset &= items

        # Filter by the some query text
        query_text = self.request.GET.get('query_text')
        if query_text:
            items = Item.objects.filter(name__icontains=query_text).distinct()
            queryset &= items

        # Filter by the avg reviews vote
        reviews_vote = self.request.GET.get('reviews_vote')
        if reviews_vote:
            ids = []
            for item in Item.objects.all():
                if int(reviews_vote) == item.reviews_vote:
                    ids.append(item.id)
            items = Item.objects.filter(id__in=ids).distinct()
            queryset &= items

        # Filter by the price
        from_price = self.request.GET.get('from_price')
        to_price = self.request.GET.get('to_price')
        if from_price and to_price:
            items = Item.objects.filter(
                price__range=(int(from_price), int(to_price))).distinct()
            queryset &= items
        elif from_price:
            items = Item.objects.filter(price__gte=int(from_price)).distinct()
            queryset &= items
        elif to_price:
            items = Item.objects.filter(price__lte=int(to_price)).distinct()
            queryset &= items

        # Filter by the colors
        colors_name = (self.request.GET.get('colors_name') or None)
        if colors_name:
            colors_name = colors_name.split(",")[:-1]
            for size in Item.objects.all().values_list('color'):
                print(size)
            items = Item.objects.all().filter(color__name__in=colors_name).distinct()
            queryset &= items

        # Filter by the size
        sizes_tag = (self.request.GET.get('sizes_tag') or None)
        if sizes_tag:
            sizes_tag = sizes_tag.split(",")[:-1]

            items = Item.objects.all().filter(
                quantities_size__size__tag__in=sizes_tag).distinct()
            queryset &= items

        return queryset
    

# POST an item
class PostItemAPI(generics.CreateAPIView):
    
    serializer_class = PostItemSerializer

    """ @method_decorator(login_required, name='dispatch')
    @method_decorator(user_passes_test(is_sub_seller), name='dispatch') """
    def post(self, request):
        print(request.data)
        serializer = PostItemSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'serializer': serializer.data}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response({'serializer': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Per fare determinate modifiche ad un item (da completare)
class UpdateItemAPI(generics.UpdateAPIView):
  
    serializer_class = UpdateItemSerializer

    """ @method_decorator(login_required, name='dispatch')
    @method_decorator(user_passes_test(is_sub_seller), name='dispatch') """
    def put(self, request, pk):
        serializer = UpdateItemSerializer(data=request.data, context={'item_pk': pk})
        if serializer.is_valid():
            serializer.save()
            return Response({'serializer': serializer.data}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Per eliminare un item
class DeleteItemAPI(APIView):

    def delete(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        if not item:
            return Response({"Message" : "Item not found"}, status=status.HTTP_400_BAD_REQUEST)
        item.delete()
        return Response(status=status.HTTP_200_OK)


# Dato ID categoria ritorna gli item appartenenti ad essa
class GetItemByCategoryAPI(APIView):

    def get(self, request, pk):
        queryset = Item.objects.filter(category=pk)
        serializer = GetItemSerializer(queryset, many=True)
        return Response(serializer.data)


#Per aggiungere una review
class PostItemReviewAPI(APIView):

    serializer_class = PostItemReviewSerializer

    def post(self, request):
        serializer = PostItemReviewSerializer(data=request.data)
        if request.user.is_authenticated:
            if serializer.is_valid():
                serializer.save()
                return Response({'serializer': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'serializer': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


#Lista delle review filtrate dall'id dell'item
class GetItemReviewByItemAPI(APIView):
    
    def get(self, request, pk, format=None):
        
        item = get_object_or_404(Item, pk=pk)
        if not item:
            return Response({"Message" : "Oggetto non presente"}, status=status.HTTP_400_BAD_REQUEST)
        queryset = ItemReview.objects.filter(item = item.id)
        serializer = GetItemReviewSerializer(queryset, many=True)
        return Response(serializer.data)


# GET all the ItemReview
class GetAllItemReviewAPI(APIView):
    
    def get(self, request, format=None):
        
        queryset = ItemReview.objects.all()
        serializer = ItemReviewSerializer(queryset, many=True)
        return Response(serializer.data)


# Lista delle ItemCategory
class GetAllItemCategoryAPI(APIView):
    
    def get(self, request, format=None):

        queryset = ItemCategory.objects.all()
        serializer = GetItemCategorySerializer(queryset, many=True)
        return Response(serializer.data)


# Lista delle ItemQuantitySize
class GetAllItemQuantitySizeAPI(APIView):
    
    def get(self, request, format=None):
        queryset = ItemQuantitySize.objects.all()
        serializer = GetItemQuantitiSizeSerializer(queryset, many=True)
        return Response(serializer.data)


# Lista delle ItemSize
class GetAllItemSizeAPI(APIView):
    
    def get(self, request, format=None):

        queryset = ItemSize.objects.all()
        serializer = GetItemSizeSerializer(queryset, many=True)
        return Response(serializer.data)


#Lista delle ItemColor
class GetAllItemColorAPI(APIView):
    
    def get(self, request, format=None):

        queryset = ItemColor.objects.all()
        serializer = GetItemColorSerializer(queryset, many=True)
        return Response(serializer.data)


#Lista delle ItemImages
class GetAllItemImagesAPI(APIView):
    
    def get(self, request, format=None):

        queryset = ItemImage.objects.all()
        serializer = GetItemImagesSerializer(queryset, many=True)
        return Response(serializer.data)


#
#_________________________API VIEWS END___________________________
#

class ItemView(DetailView):
    model = Item
    template_name = 'item.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ItemView, self).get_context_data(*args, **kwargs)
        context['images'] = self.object.images.all()
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
        from django.core import serializers as asd
        images_json = asd.serialize('json', itemImage)
        qntsz_json = asd.serialize('json', itemQuantitySize)

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
                    print(image)
                    if (ItemImage.objects.filter(image=image).exists()):
                        image_old = ItemImage.objects.get(image=image)
                        image_old.delete()

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


class DeleteItemImageView(View):

    def post(self, request, *args, **kwargs):
        itemimage_name = request.POST.get('itemimage_name', None)
        itemimage = ItemImage.objects.filter(image=itemimage_name)
        itemimage.delete()

        return HttpResponse("eliminato")
