from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from base64 import urlsafe_b64encode
import json

def generate_vapid_keys():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )

    private_key_b64 = urlsafe_b64encode(private_bytes).decode('utf-8')
    public_key_b64 = urlsafe_b64encode(public_bytes).decode('utf-8')

    keys = {
        'private_key': private_key_b64,
        'public_key': public_key_b64
    }

    with open('vapid_keys.json', 'w') as f:
        json.dump(keys, f, indent=2)

    print("VAPID keys generated and saved to vapid_keys.json:")
    print(f"Public Key: {public_key_b64}")
    print(f"Private Key: {private_key_b64}")

if __name__ == '__main__':
    generate_vapid_keys() 