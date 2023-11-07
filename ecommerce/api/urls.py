from django.urls import path
from . import views

urlpatterns = [
    path("", views.apiOverview, name="api-overview"),
    # users
    path("user/create/", views.add_user, name="create-user"),
    path("user/<str:pk>/", views.user_profile, name="user-profile"),
    path("user/update/<str:pk>/", views.update_user, name="update-user"),
    path("user/delete/<str:pk>/", views.delete_user, name="delete-user"),
    # products
    path("products/", views.product_list, name="products"),
    path("products/add/", views.add_product, name="add-product"),
    path("products/<str:pk>/", views.product_details, name="user-details"),
    path("products/update/<str:pk>/", views.update_product, name="update-product"),
    path("products/delete/<str:pk>/", views.delete_product, name="delete-product"),
    # cart
    path("cart/", views.cart_list, name="cart"),
    path("cart/add/", views.add_to_cart, name="add-to-cart"),
    path("cart/update/<str:pk>/", views.update_cart, name="update-cart"),
    path("cart/delete/<str:pk>/", views.delete_cart, name="delete-cart"),
    # orders
    path("orders/", views.order_list, name="orders"),
    path("orders/add/", views.place_order, name="create-order"),
    path("orders/delete/<str:pk>/", views.delete_cart, name="delete-order"),
]
