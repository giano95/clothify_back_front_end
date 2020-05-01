from django.urls import path
from item.views import (
    ItemView,
    AddView,
)


app_name = 'item'
urlpatterns = [
    path('item/<pk>/', ItemView.as_view(), name='item'),
    path('add/', AddView.as_view(), name='add'),
]
