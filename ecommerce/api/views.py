from django.conf import settings
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status, permissions
from .serializers import *
import pyrebase

# firebase connection
firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
authe = firebase.auth()
database = firebase.database()

# list of endpoints
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        
        'Create User':'/user/create/',
        'User Profile':'/user/<str:pk>/',
        'Update User':'/user/<str:pk>/',
        'Delete User':'/user/<str:pk>/',
        'Product List':'/products/',
        'Add Product':'/products/add/',
        'View Product':'/products/<str:pk>/',
        'Update Product':'/products/update/<str:pk>/',
        'Delete Product':'/products/delete/<str:pk>/',
        'Cart':'/cart/',
        'Add Item to Cart':'/cart/add',
        'Update Cart':'/cart/update/<str:pk>/',
        'Delete Cart Items':'/cart/delete/<str:pk>/',
        'Orders List':'/orders/',
        'Add Order':'/orders/add',
        'Delete Order':'/orders/delete/<str:pk>/',
    }
    return Response(api_urls)

# create entry
@api_view(['POST'])
def create_entry(request, child_node, serializer):
    try:
        node_serializer = serializer(data=request.data)
        
        if node_serializer.is_valid():
            entry_data = node_serializer.validated_data
            new_entry = database.child(child_node).push(entry_data)

            response_data = {
                "message": f"Entry created successfully in '{child_node}'",
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(node_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        response_data = {
                "error": f"Failed to create entry in '{child_node}': " + str(e),
            }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

# update entry information
@api_view(['POST'])
def update_entry(request, key, child_node, serializer):
    product_info = database.child(child_node).child(key).get().val()
    if product_info is None:
        return Response({"message": "Product not found"}, status=404)

    node_serializer = serializer(data=request.data)

    if node_serializer.is_valid():
        data = node_serializer.validated_data
        database.child(child_node).child(key).update(data)
        response_data = {
            "message": f"Entry in {child_node} updated successfully",
        }
        return Response(response_data, status=200)
    else:
        return Response(node_serializer.errors, status=400)

# list of items
@api_view(['GET'])
def item_list(request, child_node, node_serializer):
    try:
        item_info = database.child(child_node).get()

        items = []
        if item_info.each():
            for item in item_info.each():
                item_info = item.val()
                if item_info is not None:
                    items.append(item_info)
                print(item.key())
            item_serializer = node_serializer(items, many=True)
            return Response(item_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        response_data = {
                "error": f'Failed to retrieve entries in {child_node}: ' + str(e),
            }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

# view detailed information
@api_view(['GET'])
def item_details(request, key, child_node):
    try:
        object_detail = database.child(child_node).child(key).get().val()
        if object_detail is not None:
            return Response(object_detail, status=status.HTTP_200_OK)
        else:
            response_data = {
                "message": f"Details not found for entry in {child_node}",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        response_data = {
                "error": f'Failed to retrieve details about entry in {child_node}: ' + str(e),
            }
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# delete record
@api_view(['DELETE'])
def delete_item(request, key, child_node):
    try:
        database.child(child_node).child(key).remove()
        return Response('Item deleted successfully!')
    except Exception as e:
        return Response('Error deleting item: ' + str(e), status=status.HTTP_400_BAD_REQUEST)

# login user
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request, format=None):
    data = request.data
    email = data.get('email')
    password = data.get('password')

    try:
        user = authe.sign_in_with_email_and_password(email, password)

        return Response({'user_id': user['localId']}, status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User
# add a user
@api_view(['POST'])
def add_user(request):
    return create_entry(request, 'users', UserSerializer) 

# view user profile
@api_view(['GET'])
def user_profile(request, user_id):
    return item_details(request, user_id, 'users')

# update user
@api_view(['GET'])
def update_user(request, user_id):
    return update_entry(request, user_id, 'users', UserSerializer)

# delete user
@api_view(['GET'])
def delete_user(request, user_id):
    return delete_item(request, user_id, 'users')


# Products
# add a product
@api_view(['POST'])
def add_product(request):
    return create_entry(request, 'product', ProductSerializer) 

# product details
@api_view(['GET'])
def product_details(request, product_id):
    return item_details(request, product_id, 'products')

# product list
@api_view(['GET'])
def product_list(request):
    return item_list(request, 'products', ProductSerializer)

# update product info
@api_view(['GET'])
def update_product(request, product_id):
    return update_entry(request, product_id, 'products', ProductSerializer)

# delete product
@api_view(['GET'])
def delete_product(request, product_id):
    return delete_item(request, product_id, 'products')


# Cart
# add item to cart
@api_view(['POST'])
def add_to_cart(request):
    return create_entry(request, 'cart', ProductSerializer) 

# cart list
@api_view(['GET'])
def cart_list(request):
    return item_list(request, 'cart', CartSerializer)

# update cart
@api_view(['GET'])
def update_cart(request, cart_id):
    return update_entry(request, cart_id, 'cart', CartSerializer)

# delete cart
@api_view(['GET'])
def delete_cart(request, cart_id):
    return delete_item(request, cart_id, 'cart')


# Orders
# place order
@api_view(['POST'])
def place_order(request):
    return create_entry(request, 'orders', OrderSerializer) 

# order list
@api_view(['GET'])
def order_list(request):
    return item_list(request, 'orders', OrderSerializer)

# delete order
@api_view(['GET'])
def delete_order(request, order_id):
    return delete_item(request, order_id, 'orders')









    

# user profile  



