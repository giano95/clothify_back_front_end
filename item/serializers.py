from rest_framework import serializers
from django.db import models
from item.models import (
    Item,
    ItemCategory,
    ItemReview,
    ItemImage,
    ItemColor,
    ItemSize,
    ItemQuantitySize,
    ItemLabel,
    LOREM_IPSUM
)
from core.models import User



class GetItemQuantitiSizeSerializer(serializers.ModelSerializer):
    size = serializers.StringRelatedField()
    class Meta:
        model = ItemQuantitySize
        fields = '__all__'

class GetItemCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemCategory
        fields = '__all__'

class GetItemColorSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()
    class Meta:
        model = ItemColor
        fields = '__all__'

class GetItemSerializer(serializers.ModelSerializer):
    quantities_size = GetItemQuantitiSizeSerializer(many=True)
    color = GetItemColorSerializer(many=True)
    
    class Meta:
        model = Item
        fields = '__all__'


class GetItemSizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemSize
        fields = '__all__'

class GetItemImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemImage
        fields = '__all__'



class GetItemReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = ItemReview
        fields = '__all__'


class PostItemQuantitySizeSerializer(serializers.ModelSerializer):

    size = serializers.PrimaryKeyRelatedField(queryset=ItemSize.objects.all(), default=None)

    class Meta:
        model = ItemQuantitySize
        fields = ['size', 'quantity']


class PostItemColorSerializer(serializers.PrimaryKeyRelatedField, serializers.ModelSerializer):

    class Meta:
        model = ItemColor
        fields = ['name']


class PostItemSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)

    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    name = serializers.CharField(max_length=100)
    price = serializers.FloatField()
    category = serializers.PrimaryKeyRelatedField(queryset=ItemCategory.objects.all())
    description = serializers.CharField(max_length=1000, default=LOREM_IPSUM)
    img = serializers.ImageField()
    images_0 = serializers.ImageField(required=False, allow_null=True)
    images_1 = serializers.ImageField(required=False, allow_null=True)
    images_2 = serializers.ImageField(required=False, allow_null=True)
    color = PostItemColorSerializer(many=True, queryset=ItemColor.objects.all())
    quantity_size_0 = PostItemQuantitySizeSerializer(required=False, allow_null=True)
    quantity_size_1 = PostItemQuantitySizeSerializer(required=False, allow_null=True)
    quantity_size_2 = PostItemQuantitySizeSerializer(required=False, allow_null=True)
    quantity_size_3 = PostItemQuantitySizeSerializer(required=False, allow_null=True)
    quantity_size_4 = PostItemQuantitySizeSerializer(required=False, allow_null=True)
    quantity_size_5 = PostItemQuantitySizeSerializer(required=False, allow_null=True)
    #label = ItemLabelSerializer(allow_null=True, required=False, queryset=ItemLabel.objects.all())
    #not_discounted_price = serializers.FloatField(required=False, allow_null=True)



    def create(self, validated_data):
        
        color = validated_data.pop('color')

        images = []
        if 'images_0' in validated_data.keys():
            images_0 = ItemImage.objects.create(image=validated_data.pop('images_0'))
            images.append(images_0)
        if 'images_1' in validated_data.keys():
            images_1 = ItemImage.objects.create(image=validated_data.pop('images_1'))
            images.append(images_1)
        if 'images_2' in validated_data.keys():
            images_2 = ItemImage.objects.create(image=validated_data.pop('images_2'))
            images.append(images_2)
        quantity_size_0 = validated_data.pop('quantity_size_0')
        quantity_size_1 = validated_data.pop('quantity_size_1')
        quantity_size_2 = validated_data.pop('quantity_size_2')
        quantity_size_3 = validated_data.pop('quantity_size_3')
        quantity_size_4 = validated_data.pop('quantity_size_4')
        quantity_size_5 = validated_data.pop('quantity_size_5')
        
        
        item = Item.objects.create(**validated_data)

        item.color.set(color)

        item.images.set(images)

        quantities_size = []
        if quantity_size_0:
            quantity_size_0 = ItemQuantitySize.objects.create(
                size=quantity_size_0['size'],
                quantity=quantity_size_0['quantity'])
            quantities_size.append(quantity_size_0)
        if quantity_size_1:
            quantity_size_1 = ItemQuantitySize.objects.create(
                size=quantity_size_1['size'],
                quantity=quantity_size_1['quantity'])
            quantities_size.append(quantity_size_1)
        if quantity_size_2:
            quantity_size_2 = ItemQuantitySize.objects.create(
                size=quantity_size_2['size'],
                quantity=quantity_size_2['quantity'])
            quantities_size.append(quantity_size_2)
        if quantity_size_3:
            quantity_size_3 = ItemQuantitySize.objects.create(
                size=quantity_size_3['size'],
                quantity=quantity_size_3['quantity'])
            quantities_size.append(quantity_size_3)
        if quantity_size_4:
            quantity_size_4 = ItemQuantitySize.objects.create(
                size=quantity_size_4['size'],
                quantity=quantity_size_4['quantity'])
            quantities_size.append(quantity_size_4)
        if quantity_size_5:
            quantity_size_5 = ItemQuantitySize.objects.create(
                size=quantity_size_5['size'],
                quantity=quantity_size_5['quantity'])
            quantities_size.append(quantity_size_5)
        item.quantities_size.set(quantities_size)

        item.save()

        return item


class UpdateItemSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=100, required=False, allow_null=True)
    price = serializers.FloatField(required=False, allow_null=True)
    category = serializers.PrimaryKeyRelatedField(queryset=ItemCategory.objects.all(), required=False, allow_null=True)
    description = serializers.CharField(max_length=1000, required=False, allow_null=True)
    img = serializers.ImageField(required=False, allow_null=True)
    images_0 = serializers.ImageField(required=False, allow_null=True)
    images_1 = serializers.ImageField(required=False, allow_null=True)
    images_2 = serializers.ImageField(required=False, allow_null=True)
    color = PostItemColorSerializer(many=True, queryset=ItemColor.objects.all(), required=False, allow_null=True)
    quantity_size_0 = PostItemQuantitySizeSerializer(required=False, allow_null=True)
    quantity_size_1 = PostItemQuantitySizeSerializer(required=False, allow_null=True)
    quantity_size_2 = PostItemQuantitySizeSerializer(required=False, allow_null=True)
    quantity_size_3 = PostItemQuantitySizeSerializer(required=False, allow_null=True)
    quantity_size_4 = PostItemQuantitySizeSerializer(required=False, allow_null=True)
    quantity_size_5 = PostItemQuantitySizeSerializer(required=False, allow_null=True)
    #label = ItemLabelSerializer(allow_null=True, required=False, queryset=ItemLabel.objects.all())
    #not_discounted_price = serializers.FloatField(required=False, allow_null=True)



    def create(self, validated_data):
        

        # IDK why it automatically add a color field even if in the request.data it's not present
        if len(validated_data.get('color')) == 0:
            validated_data.pop('color')
        
        item = Item.objects.get(pk=self.context.get("item_pk"))

        print(validated_data)
        if 'name' in validated_data.keys():
            item.name = validated_data.pop('name')
        if 'price' in validated_data.keys():
            item.price  = validated_data.pop('price')
        if 'category' in validated_data.keys():
            item.category = validated_data.pop('category')
        if 'description' in validated_data.keys():
            item.description = validated_data.pop('description')
        if 'img' in validated_data.keys():
            item.img = validated_data.pop('img')
        images = []
        if 'images_0' in validated_data.keys():
            try:
                ItemImage.objects.filter(id=item.images.all()[0].id).delete() # delete the old img instances
            except:
                pass
            images_0 = ItemImage.objects.create(image=validated_data.pop('images_0'))
            images.append(images_0)
        if 'images_1' in validated_data.keys():
            try:
                ItemImage.objects.filter(id=item.images.all()[1].id).delete() # delete the old img instances
            except:
                pass
            images_1 = ItemImage.objects.create(image=validated_data.pop('images_1'))
            images.append(images_1)
        if 'images_2' in validated_data.keys():
            try:
                ItemImage.objects.filter(id=item.images.all()[2].id).delete() # delete the old img instances
            except:
                pass
            images_2 = ItemImage.objects.create(image=validated_data.pop('images_2'))
            images.append(images_2)
        if len(images) > 0: # otherwise it will save an empty image even if nothing is passed
            item.images.set(images)
        if 'color' in validated_data.keys():
            item.color.set(validated_data.pop('color'))
        quantities_size = []
        if 'quantity_size_0' in validated_data.keys():
            try:
                ItemQuantitySize.objects.filter(id=item.quantities_size.all()[0].id).delete() # delete the old quantities size instances
            except:
                pass
            quantity_size_0 = validated_data.pop('quantity_size_0')
            quantity_size_0 = ItemQuantitySize.objects.create(size=quantity_size_0['size'], quantity=quantity_size_0['quantity'])
            quantities_size.append(quantity_size_0)
        if 'quantity_size_1' in validated_data.keys():
            try:
                ItemQuantitySize.objects.filter(id=item.quantities_size.all()[1].id).delete() # delete the old quantities size instances
            except:
                pass
            quantity_size_1 = validated_data.pop('quantity_size_1')
            quantity_size_1 = ItemQuantitySize.objects.create(size=quantity_size_1['size'], quantity=quantity_size_1['quantity'])
            quantities_size.append(quantity_size_1)
        if 'quantity_size_2' in validated_data.keys():
            try:
                ItemQuantitySize.objects.filter(id=item.quantities_size.all()[2].id).delete() # delete the old quantities size instances
            except:
                pass
            quantity_size_2 = validated_data.pop('quantity_size_2')
            quantity_size_2 = ItemQuantitySize.objects.create(size=quantity_size_2['size'], quantity=quantity_size_2['quantity'])
            quantities_size.append(quantity_size_2)
        if 'quantity_size_3' in validated_data.keys():
            try:
                ItemQuantitySize.objects.filter(id=item.quantities_size.all()[3].id).delete() # delete the old quantities size instances
            except:
                pass
            quantity_size_3 = validated_data.pop('quantity_size_3')
            quantity_size_3 = ItemQuantitySize.objects.create(size=quantity_size_3['size'], quantity=quantity_size_3['quantity'])
            quantities_size.append(quantity_size_3)
        if 'quantity_size_4' in validated_data.keys():
            try:
                ItemQuantitySize.objects.filter(id=item.quantities_size.all()[5].id).delete() # delete the old quantities size instances
            except:
                pass
            quantity_size_4 = validated_data.pop('quantity_size_4')
            quantity_size_4 = ItemQuantitySize.objects.create(size=quantity_size_4['size'], quantity=quantity_size_4['quantity'])
            quantities_size.append(quantity_size_4)
        if 'quantity_size_5' in validated_data.keys():
            try:
                ItemQuantitySize.objects.filter(id=item.quantities_size.all()[5].id).delete() # delete the old quantities size instances
            except:
                pass
            quantity_size_5 = validated_data.pop('quantity_size_5')
            quantity_size_5 = ItemQuantitySize.objects.create(size=quantity_size_5['size'], quantity=quantity_size_5['quantity'])
            quantities_size.append(quantity_size_5)
        if len(quantities_size) > 0: # otherwise it will save an empty quantity_sizes even if nothing is passed
            item.quantities_size.set(quantities_size)

        item.save()

        return item


class PostItemReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemReview
        fields = '__all__'
