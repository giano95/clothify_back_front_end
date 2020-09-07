from django.urls import path
from order.views import (
    GetOrderAPI,
    AddOrderItemAPI,
    DeleteOrderItemAPI,
    #_____API VIEWS END_____
    OrderView,
    AddOrderItemView,
    UpdateOrderItemView,
)



app_name = 'order'
urlpatterns = [
    path('api/delete/<pk>/', DeleteOrderItemAPI.as_view()),
    path('api/add_order_item/', AddOrderItemAPI.as_view()),
    path('api/order/', GetOrderAPI.as_view()),
    #_____API VIEWS END_____
    path('order/', OrderView.as_view(), name='order'),
    path('add_order_item/<pk>/<str:sz>/<q>/',
         AddOrderItemView.as_view(), name='add_order_item'),
    path('update_order_item/<pk>/<q>/',
         UpdateOrderItemView.as_view(), name='update_order_item'),
]
