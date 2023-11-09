from settings import production
from rest_framework import authentication, status
from rest_framework.response import Response
import firebase_admin as admin
import firebase_admin.auth as auth
import pyrebase
from firebase_admin import credentials, db

# firebase connection
# firebase = pyrebase.initialize_app(production.FIREBASE_CONFIG)
cred = credentials.Certificate(production.FIREBASE_ADMIN_CONFIG)
admin.initialize_app(
    cred,
    {
        "databaseURL": "https://test-d486b-default-rtdb.firebaseio.com",
    },
)

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return None
        
        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token["uid"]
        except:
            return None
        
        try:
            user = db.reference("users").child(uid).get()
            return user
        except:
            return Response(status.HTTP_404_NOT_FOUND)
