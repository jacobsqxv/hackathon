from django.urls import path
from . import views

urlpatterns = [
    path("", views.apiOverview, name="api-overview"),
    # users
    path("register/", views.create_user, name="register"),
    path("signin/", views.sign_in_user, name="signin"),
    path("user/<str:user_id>/", views.user_profile, name="user-profile"),
    path("user/update/<str:user_id>/", views.update_user, name="update-user"),
    path("user/delete/<str:user_id>/", views.delete_user, name="delete-user"),
    # products
    path("products/", views.product_list, name="products"),
    path("products/add/", views.add_product, name="add-product"),
    path("products/<str:product_id>/", views.product_details, name="user-details"),
    # cart
    path("cart/<str:cart_id>/", views.cart_list, name="cart"),
    path("cart/add/", views.create_cart, name="add-to-cart"),
    path("cart/update/<str:cart_id>/<str:item_id>/", views.update_cart_item, name="update-cart-item"),
    path("cart/delete/<str:cart_id>/<str:item_id>/", views.delete_cart_item, name="delete-cart-item"),
    # orders
    path("orders/", views.order_list, name="orders"),
    path("orders/add/", views.place_order, name="create-order"),
    path("orders/delete/<str:order_id>/", views.delete_order, name="delete-order"),
]
