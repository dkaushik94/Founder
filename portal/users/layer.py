# -*- coding: utf-8 -*-
import jwt
import os
from portal.settings import RSA_KEY_PATH

from datetime import timedelta, datetime

try:
    from Crypto.PublicKey import RSA
except:
    raise Exception("pycrytpo library not installed. "
                    "Run `pip install -r requirements.txt`")

# The PyJWT library can optionally use PyCrypto for RSA256 signing, instead of
#   the 'cryptography' module. We'll use PyCrypto to minimize required external
#   dependencies.
from jwt.contrib.algorithms.pycrypto import RSAAlgorithm
try:
    jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))
except ValueError:
    pass  # You have cryptography module installed, so we'll use it instead

PROVIDER_ID = 'layer:///providers/095ee69c-8174-11e6-86b6-c7b7000000b4'
KEY_ID = 'layer:///keys/ed51dfa0-8325-11e6-b789-02d35d0d7409'

if not (PROVIDER_ID and KEY_ID and RSA_KEY_PATH):
    raise Exception("You must provide PROVIDER_ID, KEY_ID, and "
                    "RSA_KEY_PATH in %s" % __file__)


def generate_identity_token(user_id, nonce, avatar_url):
    """Creates Layer Identity Token
    :Parameter user_id:   Your (the Provider) ID that represents the user.
    :Type user_id: string
    :Parameter nonce:     The nonce returned by the Layer SDK.
    :Type nonce: string
    """
    jwt_token = jwt.encode(
        payload={
            # String - The Provider ID found in the Layer Dashboard
            "iss": PROVIDER_ID,
            # String - Provider's internal ID for the authenticating user
            "prn": user_id,
            # Integer - Time of Token Issuance in RFC 3339 seconds
            "iat": datetime.now(),
            # Integer - Token Expiration in RFC 3339 seconds; set to 2 minutes
            "exp": datetime.utcnow() + timedelta(seconds=120),
            "nce": nonce,    # The nonce obtained via the Layer client SDK.
            "avatar_url": avatar_url,
        },
        key=_read_rsa_private_key(),
        headers={
            "typ": "JWT",   # String - Expresses a MIME Type of application/JWT
            # String - Expresses the type of algorithm used to sign the token;
            # must be RS256
            "alg": 'RS256',
            # String - Express a Content Type of Layer External Identity Token,
            # version 1
            "cty": "layer-eit;v=1",
            # String - Private Key associated with "layer.pem", found in the
            # Layer Dashboard
            "kid": KEY_ID
        },
        algorithm='RS256'
    )

    return jwt_token.decode("utf8")


def _read_rsa_private_key(file_path=RSA_KEY_PATH):
    """Reads an RSA private key and returns it in the PEM format.
    :Parameter file_path: The path to the key file.
        Path can be absolute or relative. Defaults to value of `RSA_KEY_PATH`
    :Type file_path: string
    :Raise IOError:
        When the key file is not found.
    """
    root = os.path.dirname(__file__)
    location = os.path.join(root, file_path)
    if not os.path.isfile(location):
        raise IOError(
            "File (%s) not found. Update `RSA_KEY_PATH` "
            "to the proper path to your private key." % location)

    with open(location, 'r') as rsa_private_key_file:
        rsa_private_key = RSA.importKey(rsa_private_key_file.read())

    # return the key in PEM (textual) format
    return rsa_private_key.exportKey().decode("utf8")