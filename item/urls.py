from django.urls import path
from item.views import (
    ItemView,
    AddView,
    DeleteView,
    UpdateView,
)


app_name = 'item'
urlpatterns = [
    path('item/<pk>/', ItemView.as_view(), name='item'),
    path('add/', AddView.as_view(), name='add'),
    path('delete/<pk>/', DeleteView.as_view(), name='delete'),
    path('update/<pk>/', UpdateView.as_view(), name='update'),
]
