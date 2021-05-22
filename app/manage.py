"""Manage ENCRYPTION."""
import os
from decouple import config
from zeep import Client
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA1
import rsa
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import base64

MDA_USERNAME = config("MDA_USERNAME")
MDA_PASSWORD = config("MDA_PASSWORD")
SOAP_WSDL_URL = config("SOAP_WSDL_URL")

URA_PUBLIC_KEY = open("./app/certs/URA.crt", "rb")
MDA_PRIVATE_KEY = open("./app/certs/ACMIS-key.pem", "rb")
MDA_PUBLIC_KEY = open("./app/certs/ACMIS-cert.txt", "rb")


class Encryption:
    """Class to manipulate Encryption."""

    def __init__(self):
        self.MDA_PASSWORD = MDA_PASSWORD
        self.MDA_USERNAME = MDA_USERNAME
        self.SOAP_WSDL_URL = SOAP_WSDL_URL
        self.URA_PUBLIC_KEY = URA_PUBLIC_KEY.read()
        self.MDA_PRIVATE_KEY = MDA_PRIVATE_KEY.read()
        self.MDA_PUBLIC_KEY = MDA_PUBLIC_KEY.read()

    def encryptCredentials(self):
        """Encrypt Concatenated username and password."""

        concatenatedUsernamePassword = (self.MDA_USERNAME + self.MDA_PASSWORD).encode(
            "utf-8"
        )
        publicKey = RSA.import_key(self.URA_PUBLIC_KEY)
        # cipher = PKCS1_OAEP.new(publicKey)
        cipherText = rsa.encrypt(concatenatedUsernamePassword, publicKey)
        encryptedCredentials = base64.b64encode(cipherText)

        return encryptedCredentials

    def getEncryptionSignature(self, encryptCredentials):
        """Sign Encrypted Credentials."""

        privateKey = RSA.import_key(self.MDA_PRIVATE_KEY)
        hashedCredential = SHA1.new(encryptCredentials)
        sign = PKCS1_v1_5.new(privateKey).sign(hashedCredential)
        signature = sign

        return signature
