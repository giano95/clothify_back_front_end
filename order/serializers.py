from rest_framework import serializers
from order.models import *
from django.db import models
from item.serializers import GetItemSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    item = GetItemSerializer()
    item_size = serializers.StringRelatedField()
    class Meta:
        model = OrderItem
        fields = '__all__'

class AddOrderItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderItem
        fields = ('user', 'item', 'quantity', 'item_size')

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    order_items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'

    """ def to_representation(self, instance):
        representation['order_items'] = OrderItemSerializer(instance.order_items).data """