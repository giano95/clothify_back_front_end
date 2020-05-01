from django.urls import path
from order.views import (
    OrderView,
    AddOrderItemView,
    UpdateOrderItemView
)


app_name = 'order'
urlpatterns = [
    path('order/', OrderView.as_view(), name='order'),
    path('add_order_item/<pk>/', AddOrderItemView.as_view(), name='add_order_item'),
    path('update_order_item/<pk>/<q>/',
         UpdateOrderItemView.as_view(), name='update_order_item'),
]
