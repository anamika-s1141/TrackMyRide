import os
import json
import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    if not firebase_admin._apps:
        # Create credentials dict from environment variables
        cred_dict = {
            "type": settings.FIREBASE_TYPE,
            "project_id": settings.FIREBASE_PROJECT_ID,
            "private_key_id": settings.FIREBASE_PRIVATE_KEY_ID,
            "private_key": settings.FIREBASE_PRIVATE_KEY.replace('\\n', '\n'),
            "client_email": settings.FIREBASE_CLIENT_EMAIL,
            "client_id": settings.FIREBASE_CLIENT_ID,
            "auth_uri": settings.FIREBASE_AUTH_URI,
            "token_uri": settings.FIREBASE_TOKEN_URI,
            "auth_provider_x509_cert_url": settings.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
            "client_x509_cert_url": settings.FIREBASE_CLIENT_X509_CERT_URL
        }
        
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)

def send_notification(token, title, body, data=None):
    """Send notification to a specific device"""
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            data=data or {},
            token=token
        )
        return messaging.send(message)
    except Exception as e:
        print(f"Error sending notification: {e}")
        return None

def send_multicast_notification(tokens, title, body, data=None):
    """Send notification to multiple devices"""
    try:
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            data=data or {},
            tokens=tokens
        )
        return messaging.send_multicast(message)
    except Exception as e:
        print(f"Error sending multicast notification: {e}")
        return None 