import os
from dotenv import load_dotenv
from keycloak import KeycloakAdmin

load_dotenv() # Crucial: This reads the .env file

# What: This connects to Keycloak as an 'Administrator'
keycloak_admin = KeycloakAdmin(
    server_url=os.getenv('KC_SERVER_URL'), # Shared from .env
    username=os.getenv('KC_ADMIN_USER'),   # New!
    password=os.getenv('KC_ADMIN_PASS'),   # New!
    realm_name=os.getenv('KC_REALM'),      # Shared from .env
    verify=True
)

def create_keycloak_user(email, name):
    # 1. Create user in Keycloak
    new_user = keycloak_admin.create_user({
        "email": email,
        "username": email,
        "enabled": True,
        "firstName": name,
    })
    
    # 2. Get the UID that Keycloak just generated
    # This ensures your DB and Keycloak stay perfectly synced
    user_id = keycloak_admin.get_user_id(email)
    return user_id