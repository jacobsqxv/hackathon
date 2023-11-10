from .base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

ALLOWED_HOSTS = ["drf-ecommerce-04cca0f2b2a5.herokuapp.com", "localhost", "127.0.0.1", "fox-current-filly.ngrok-free.app"]

FIREBASE_CONFIG = {
    "apiKey": "AIzaSyAlqb5H_c3PprLJeelpoCnU_08DZUcBDk4",
    "authDomain": "test-d486b.firebaseapp.com",
    "databaseURL": "https://test-d486b-default-rtdb.firebaseio.com",
    "projectId": "test-d486b",
    "storageBucket": "test-d486b.appspot.com",
    "messagingSenderId": "493067962671",
    "appId": "1:493067962671:web:1562d1f4b055442151f9da",
    "measurementId": "G-4WEKGNRF2F",
}

FIREBASE_ADMIN_CONFIG = {
    "type": "service_account",
    "databaseURL": "https://test-d486b-default-rtdb.firebaseio.com",
    "project_id": "test-d486b",
    "private_key_id": "58e02186b1eb634b8da62dbf5b6c62daf0e4a10f",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDNPeAL36kfmZcw\nXZSlXlfOkZNYuZlswtUXoex0XcD5TQ6wqEvD9YBZg/UJ1hDhvrmi1S6mJanU+1bG\nP0bcDR+X4m50h2vM70ppMF/3Tpk2iOkz78YYqZJMA/sQ5zps6miclGsrHVLOvoYR\n7o+9kXoT7whRRLh4MeOeBeQV1Ye7tnhSd2VjU1r3oQjv7TgfbpgnkBo5Abh0u/Qm\n+IYDN9vPuBltbKO2bn0o2sSz7bkcc/lvAtJE4zNVlW1Bh1v6eP+yn4EyTTGUB23R\nUkXDyF6Dh3JUoWZhFvpUJSIGY4cximTjbQSfp9zcHRHW9LpEZHcKbkYANehLTe+Y\neLxCzT+dAgMBAAECggEAMXl25qXVqO5nSZtlV6+0TvE8qaij2Vnl8DpyO2LWP8JZ\nhjArg2NMu0dZ7DMUArbtHNly005E8DheJI/gTu9C7GQC6Eg0rkQIle65U2449LJw\nNLrZ79wAjh5viRWUOekPqp8EbnI1Ie0/eFcfgzzsRp3aTWzZYu/zxIX7A2BjxdW5\n2b/HUX3mnA4vh42Q4mHElWLNru3MDmhDJ2CNge/wPgVo4HSsGvs9v/wTNhQM9hwH\nyeQaBD1jTpoFWlnW1CA11+Ced/zmZyytCMcSHAKU16c7C7tYKMnCOn0xuIaBwl8a\nWJTUT6sn0ucO5A9aXuzNEceglb3Yvf8mQKh0TAx+6QKBgQDzZN2G8JfIk+Fnze0Q\nJq5aw/AWWNRXfNZEhZQT4sYNSTpHyGr00sbv4No4YA9/8tR1IGn20xFdbDdFhpP4\nBW/w8HHhawOQvcn3/uwzXzdJOoIv8GyM5oZ46ckl86dbcqgg4iS4jQXRp01wg3tN\nIwTSE8vgXSPvclIF6h1onyWNywKBgQDX3ycO8bEqtqNoY3tWFzzFx9gZG6gQXQqC\njh0ZUVOZNoLkgkVxDuYfQ8JmgO3DSbEudNd5JF8VAy0nPPT95rnh72n24myfs4t3\nOWz+N4G9Y0VSKLqzfjpgvjYQAmWqjGinospnzpUWnQZOy1HIbCesgV3gzVMjmQrh\nvnPgnGo7NwKBgFnZVVHYBSAdPytzwFyi+uA0zq9hMVnukqaO7R/+KgCDlMkk+h7Q\npHGu/r+q7m3cNYPbaGKefh2PskOvL3Zyg2VdTZzaRWGsPh+XcphwQNd+isqppVjK\nTL/cBc5FyPUgOWKSON4L6ScA7LxpPR43nDL07eEwYPCmshLO3vZdMZ7LAoGAC7/S\nkWaoPOnp5PGdMedb4GvrIBq4QAPAYbC4drtNcIZeA2/vtaKY9dSrTQbxafKl2SB0\n5dwL7MnaeEtCDluzfE+aldxnCx4rlhajDwcYYaV4jWs4FjLlnIRdzutCe1DfFViv\n6Yx94tgzErDQR7dTRXlZEbY7MzHOPNEv32bEBWsCgYBH+5vBDKt5R0LwZlUVbLX1\n34jtUe7O7C7UDnHcJ1OrnyLpSD6svbHTv6ZHj8Y0gI4MMFZ7uIVR1uKOpKwliGWp\n2+lF0eK0Ya3J7bLVCzo7gxplZupYVFgqUibtfLZH+8WMeP3fzweblwqO7xmnvUnR\nT4+Jp595nTraINVBWnGO/w==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-sfv1j@test-d486b.iam.gserviceaccount.com",
    "client_id": "101217906450181886509",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-sfv1j%40test-d486b.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com",
}
