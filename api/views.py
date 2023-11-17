from settings import production
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .serializers import *
import pyrebase, firebase_admin
from firebase_admin import credentials, auth, db

# firebase connection
firebase = pyrebase.initialize_app(production.FIREBASE_CONFIG)
cred = credentials.Certificate(production.FIREBASE_ADMIN_CONFIG)
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://test-d486b-default-rtdb.firebaseio.com",
    },
)
authe = firebase.auth()
database = firebase.database()

django_request = HttpRequest()


# list of endpoints
@api_view()
@permission_classes([AllowAny])
def apiOverview(request):
    api_urls = {
        "Register": "/register/",
        "Sign In": "/signin/",
        "Profile": "/user/<str:user_id>/",
        "Update": "/user/<str:user_id>/",
        "Delete": "/user/<str:user_id>/",
        "Products": "/products/",
        "Add": "/products/add/",
        "View": "/products/<str:product_id>/",
        "Cart": "/cart/<str:cart_id>/",
        "Add Item to Cart": "/cart/update/<str:cart_id>/<str:item_id>/",
        "Delete Cart Items": "/cart/delete/<str:cart_id>/<str:item_id>/",
        "Orders List": "/orders/",
        "Add Order": "/orders/add",
        "Delete Order": "/orders/delete/<str:order_id>/",
    }
    return Response(api_urls)


# Create
# create user
@api_view(["POST"])
@permission_classes([AllowAny])
def create_user(request, format=None):
    data = request.data
    email = data.get("email")
    password = data.get("password")
    try:
        user = auth.create_user(
            email=email,
            password=password,
        )
        users = db.reference("users")
        user_data = {
            "user_id": user.uid,
            "email": email,
            "username": data.get("username", ""),
            "first_name": data.get("first_name", ""),
        }
        users.child(user.uid).set(user_data)
        return Response({"user_id": user.uid}, status=201)
    except Exception as e:
        return Response({"error": "Failed to create user: " + str(e)}, status=400)


# sign in user
@api_view(["POST"])
@permission_classes([AllowAny])
def sign_in_user(request, format=None):
    data = request.data
    email = data.get("email")
    password = data.get("password")
    try:
        user = authe.sign_in_with_email_and_password(
            email=email,
            password=password,
        )
        auth_token = user["idToken"]
        response = Response({"auth_token": auth_token}, status=200)
        response["Authorization"] = f"{auth_token}"
        print(response)
        return response
    except Exception as e:
        return Response({"error": "Failed to sign in: " + str(e)}, status=400)


# add a product
@api_view(["POST"])
@permission_classes([AllowAny])
def add_product(request):
    try:
        node_serializer = ProductSerializer(data=request.data)
        if node_serializer.is_valid():
            entry_data = node_serializer.validated_data

            ref = database.child("products")
            new_entry = ref.push(entry_data)
            new_entry_id = new_entry["name"]

            # Update the entry in Firebase with the ID
            db.reference("products").child(new_entry_id).update(
                {"product_id": new_entry_id}
            )
            response_data = {
                "entry": new_entry_id,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(node_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        response_data = {
            "error": f"Failed to add product: " + str(e),
        }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


# add item to cart
@api_view()
@permission_classes([AllowAny])
def add_to_cart(request):
    try:
        node_serializer = CartSerializer(data=request.data)
        if node_serializer.is_valid():
            entry_data = node_serializer.validated_data

            ref = database.child("cart")
            new_entry = ref.push(entry_data)
            new_entry_id = new_entry["name"]

            # Update the entry in Firebase with the ID
            db.reference("cart").child(new_entry_id).update({"cart_id": new_entry_id})
            response_data = {
                "entry": new_entry_id,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(node_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        response_data = {
            "error": f"Failed to add to cart: " + str(e),
        }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


# update entry information
@api_view()
@permission_classes([IsAuthenticated])
def update_entry(request, key, child_node, serializer):
    product_info = database.child(child_node).child(key).get().val()
    if product_info is None:
        return Response({"message": "Product not found"}, status=404)

    node_serializer = serializer(data=request.data)
    print(request.data)
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
@api_view()
@permission_classes([AllowAny])
def item_list(request, child_node, node_serializer):
    try:
        item_info = database.child(child_node).get().val()
        items = []

        if item_info:
            for item_key, item_data in item_info.items():
                if isinstance(item_data, dict):
                    items.append(item_data)

            item_serializer = node_serializer(data=items, many=True)
            if item_serializer.is_valid():
                return Response(item_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    item_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            response_data = {
                "message": f"{child_node} is empty: {str(e)}",
            }
            return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        response_data = {
            "error": f"Failed to retrieve entries in {child_node}: {str(e)}",
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


# view detailed information
@api_view()
@permission_classes([AllowAny])
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
            "error": f"Failed to retrieve details about entry in {child_node}: "
            + str(e),
        }
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# delete record
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_item(request, key, child_node):
    try:
        database.child(child_node).child(key).remove()
        return Response("Item deleted successfully!")
    except Exception as e:
        return Response(
            "Error deleting item: " + str(e), status=status.HTTP_400_BAD_REQUEST
        )


# login user
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request, format=None):
    data = request.data
    email = data.get("email")
    password = data.get("password")

    try:
        user = authe.sign_in_with_email_and_password(email, password)

        return Response({"user_id": user.uid}, status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


# view user profile
@api_view()
@permission_classes([IsAuthenticated])
def user_profile(request, user_id):
    django_request.request = request
    django_request.method = "GET"
    return item_details(django_request, user_id, "users")


# update user
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    django_request.request = request
    django_request.method = "GET"
    return update_entry(django_request, user_id, "users", UserSerializer)


# delete user
@api_view()
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    django_request.request = request
    django_request.method = "GET"
    return delete_item(django_request, user_id, "users")


# product details
@api_view()
@permission_classes([AllowAny])
def product_details(request, product_id):
    django_request.request = request
    django_request.method = "GET"
    return item_details(django_request, product_id, "products")


# product list
@api_view()
@permission_classes([AllowAny])
def product_list(request):
    django_request.request = request
    django_request.method = "GET"
    response = item_list(django_request, "products", ProductSerializer)
    return response


# cart list
@api_view()
@permission_classes([AllowAny])
def cart_list(request, cart_id):
    try:
        # Retrieve cart details
        cart_details = database.child("cart").child(cart_id).get().val()

        if cart_details and "cartItems" in cart_details:
            cart_items = cart_details["cartItems"]

            items = []
            for item_id, item_data in cart_items.items():
                product_id = item_data.get("product_id")
                product_details = (
                    database.child("products").child(product_id).get().val()
                )

                if product_details:
                    item_info = {
                        "itemname": product_details.get("name", ""),
                        "itemprice": product_details.get("price", ""),
                        "itemquantity": item_data.get("itemquantity", ""),
                    }
                    items.append(item_info)

            item_serializer = CartSerializer(data=items, many=True)
            if item_serializer.is_valid():
                return Response(item_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    item_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            response_data = {
                "message": f"Cart with ID {cart_id} not found or does not have cartItems.",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        response_data = {
            "error": f"Failed to retrieve cart items: {str(e)}",
        }
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Update item in the cart
@api_view(["PUT"])
@permission_classes([AllowAny])
def update_cart_item(request, cart_id, item_id):
    product_id = request.data.get("product_id")
    new_quantity = request.data.get("quantity", 1)

    # Update the quantity of the specified item in the cart
    cart_item_ref = (
        database.child("cart").child(cart_id).child("cartItems").child(item_id)
    )
    cart_item_ref.update({"product_id": product_id, "itemquantity": new_quantity})

    cart_item_details = cart_item_ref.get().val()

    response_data = {
        "cart_id": {
            "items": {
                f"{item_id}": {
                    "itemID": cart_item_details.get("product_id", ""),
                    "itemquantity": cart_item_details.get("itemquantity", ""),
                }
            },
        }
    }

    return Response(response_data, status=status.HTTP_200_OK)


# Delete item from the cart
@api_view(["DELETE"])
@permission_classes([AllowAny])
def delete_cart_item(request, cart_id, item_id):
    # Delete the specified item from the cart
    cart_item_ref = (
        database.child("cart").child(cart_id).child("cartItems").child(item_id)
    )
    cart_item_ref.remove()

    response_data = {
        "message": "Item deleted successfully",
    }

    return Response(response_data, status=status.HTTP_204_NO_CONTENT)


# Orders
# place order
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def place_order(request):
    try:
        node_serializer = OrderSerializer(data=request.data)
        if node_serializer.is_valid():
            entry_data = node_serializer.validated_data

            ref = database.child("order")
            new_entry = ref.push(entry_data)
            new_entry_id = new_entry["name"]

            # Update the entry in Firebase with the ID
            db.reference("order").child(new_entry_id).update({"id": new_entry_id})
            response_data = {
                "entry": new_entry_id,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(node_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        response_data = {
            "error": f"Failed to add order: " + str(e),
        }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


# order list
@api_view()
@permission_classes([IsAuthenticated])
def order_list(request):
    django_request.request = request
    django_request.method = "POST"
    return item_list(request, "orders", OrderSerializer)


# delete order
@api_view()
@permission_classes([IsAuthenticated])
def delete_order(request, order_id):
    django_request.request = request
    django_request.method = "POST"
    return delete_item(request, order_id, "orders")


# add item to cart
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_cart(request):
    user_id = str(request.user.uid)
    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity", 1)

    # Create a new cart entry with user_id
    cart_data = {"userID": user_id, "cartItems": {}}
    cart_ref = database.child("cart").push(cart_data)
    cart_id = cart_ref["name"]

    # Create a new cart_item entry
    cart_item_data = {"itemID": product_id, "itemquantity": quantity}
    cart_item_ref = (
        database.child("cart").child(cart_id).child("cartItems").push(cart_item_data)
    )
    cart_item_id = product_id

    # Retrieve cart_item details
    cart_item_details = (
        database.child("cart")
        .child(cart_id)
        .child("cartItems")
        .child(cart_item_id)
        .get()
        .val()
    )

    response_data = {
        "cart_id": {
            "items": {
                f"{cart_item_id}": {
                    "itemID": cart_item_details.get("itemID", ""),
                    "itemquantity": cart_item_details.get("itemquantity", ""),
                }
            },
            "user_id": user_id,
        }
    }
    return Response(response_data, status=status.HTTP_201_CREATED)
