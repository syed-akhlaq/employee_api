import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

# 1. Configuration
# WHY: We wrap the raw string in PEM headers so the 'jose' library recognizes it as an RSA key.
RAW_PUBLIC_KEY = os.getenv("KC_PUBLIC_KEY", "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvJl8ACnUiRkuQ8LUydXzz3RhwWiSqWRBmnL7RHNJJqONgxI6/C8ZyZZ1irG7hjvmS6/05nnh936Ec6W65URtu20b2TvMtlS8qR2JZ29FN01vbs0XaDv51bTAYd0TpjgtQ1HUO7/aIMv8WOr3QNqO915KW6ACn2/wMRrg+r52PAuptpyjX8QcxA/gZpFn1x6joraSam0iZzGo1ny9laFymosiS2EskBGX0QMqQorbncFYp+/4/T75mRJVrnJB25tK3LeQYy83l/47uU423R9rZYTm0RzgCiSMLISeD2TaJw/nASIeNHwiamuBNPVYSlcVaF1WKFiscCn1vJD/b2VmPQIDAQAB")

KEYCLOAK_PUBLIC_KEY = f"-----BEGIN PUBLIC KEY-----\n{RAW_PUBLIC_KEY}\n-----END PUBLIC KEY-----"

# WHAT: HTTPBearer
# WHY: This tells FastAPI Swagger UI to show an "Authorize" button that expects a "Bearer <token>"
security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    WHAT IT DOES:
    1. Extracts the token from the Authorization header.
    2. Decodes it using Keycloak's Public Key.
    3. Verifies that the token hasn't been tampered with and isn't expired.
    """
    token = credentials.credentials

    try:
        # WHY: 'jwt.decode' performs the cryptographic check. 
        # If the token was not signed by your Keycloak, this will fail.
        payload = jwt.decode(
            token, 
            KEYCLOAK_PUBLIC_KEY, 
            algorithms=["RS256"],
            options={
                "verify_aud": False, # Keycloak tokens often have 'account' as audience
                "verify_exp": True   # VERY IMPORTANT: Ensures expired tokens are rejected
            } 
        )
        
        # WHAT: Returns the payload (claims)
        # WHY: This allows your routes to know WHO is calling (e.g., payload['preferred_username'])
        return payload

    except JWTError as e:
        # WHY: If verification fails, we return a 401 Unauthorized error.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )