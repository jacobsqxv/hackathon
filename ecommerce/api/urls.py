from django.urls import path
from . import views

urlpatterns = [
    path("", views.apiOverview, name="api-overview"),
    # users
    path("user/add/", views.create_user, name="create-user"),
    path("user/<str:user_id>/", views.user_profile, name="user-profile"),
    path("user/update/<str:user_id>/", views.update_user, name="update-user"),
    path("user/delete/<str:user_id>/", views.delete_user, name="delete-user"),
    # products
    path("products/", views.product_list, name="products"),
    path("products/add/", views.add_product, name="add-product"),
    path("products/<str:product_id>/", views.product_details, name="user-details"),
    # cart
    path("cart/", views.cart_list, name="cart"),
    path("cart/add/", views.add_to_cart, name="add-to-cart"),
    path("cart/delete/<str:cart_id>/", views.delete_cart, name="delete-cart"),
    # orders
    path("orders/", views.order_list, name="orders"),
    path("orders/add/", views.place_order, name="create-order"),
    path("orders/delete/<str:order_id>/", views.delete_cart, name="delete-order"),
]
