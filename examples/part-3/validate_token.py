"""Audience validation for an MCP server acting as an OAuth resource server.
The script signs two test tokens with a throwaway key, then validates both."""
import time

import jwt
from cryptography.hazmat.primitives.asymmetric import rsa

RESOURCE = "https://mcp.example.com"
ISSUER = "https://auth.example.com"


def validate(token, public_key):
    return jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        audience=RESOURCE,
        issuer=ISSUER,
        options={"require": ["exp", "aud", "iss"]},
    )


if __name__ == "__main__":
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    claims = {"iss": ISSUER, "sub": "user-17", "exp": int(time.time()) + 300}
    tokens = {
        "issued for this server": jwt.encode({**claims, "aud": RESOURCE}, key, algorithm="RS256"),
        "issued for another API": jwt.encode({**claims, "aud": "https://files.example.com"}, key, algorithm="RS256"),
    }
    for label, token in tokens.items():
        try:
            validate(token, key.public_key())
            print(f"{label}: accepted")
        except jwt.InvalidTokenError as error:
            print(f"{label}: rejected, respond with HTTP 401 ({error})")
