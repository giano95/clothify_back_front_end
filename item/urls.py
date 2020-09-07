from django.urls import path
from item.views import (
    GetAllItemsAPI,
    GetItemByIdAPI,
    GetQueryItemAPI,
    PostItemAPI,
    UpdateItemAPI,
    DeleteItemAPI,
    GetItemByCategoryAPI,
    PostItemReviewAPI,
    GetItemReviewByItemAPI,
    GetAllItemReviewAPI,
    GetAllItemCategoryAPI,
    GetAllItemQuantitySizeAPI,
    GetAllItemSizeAPI,
    GetAllItemColorAPI,
    GetAllItemImagesAPI,
    #_____API VIEWS END_____
    ItemView,
    AddView,
    DeleteView,
    UpdateView,
    DeleteItemImageView
)


app_name = 'item'
urlpatterns = [
    path('api/items/', GetAllItemsAPI.as_view()),
    path('api/item/<pk>', GetItemByIdAPI.as_view()),
    path('api/item_query/', GetQueryItemAPI.as_view()),
    path('api/item/add/', PostItemAPI.as_view()),
    path('api/update/<pk>/', UpdateItemAPI.as_view()),
    path('api/delete/<pk>/', DeleteItemAPI.as_view()),
    path('api/item_category/<pk>/', GetItemByCategoryAPI.as_view()),
    path('api/add_review/', PostItemReviewAPI.as_view()),
    path('api/item_reviews/<pk>/', GetItemReviewByItemAPI.as_view()),
    path('api/item_reviews_all/', GetAllItemReviewAPI.as_view()),
    path('api/item_categories/', GetAllItemCategoryAPI.as_view()),
    path('api/item_quantitysize/', GetAllItemQuantitySizeAPI.as_view()),
    path('api/item_sizes/', GetAllItemSizeAPI.as_view()),
    path('api/item_colors/', GetAllItemColorAPI.as_view()),
    path('api/item_images/', GetAllItemImagesAPI.as_view()),
    #_____API VIEWS END_____
    path('item/<pk>/', ItemView.as_view(), name='item'),
    path('add/', AddView.as_view(), name='add'),
    path('delete/<pk>/', DeleteView.as_view(), name='delete'),
    path('update/<pk>/', UpdateView.as_view(), name='update'),
    path('delete_itemimage/', DeleteItemImageView.as_view(), name='delete_itemimage'),
]
