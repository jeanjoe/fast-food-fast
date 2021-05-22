"""PRN PAYMENT API endpoints."""
from OpenSSL.crypto import *
from flask import Flask, jsonify
from zeep import Client, Settings
import json

from app.manage import Encryption

app = Flask(__name__)
encryption = Encryption()
settings = Settings(strict=True, xml_huge_tree=True)


@app.route("/", methods=["GET"])
def index():
    """API start route."""
    return jsonify({"response": "Works!"}), 200


@app.route("/api/v1/payment-prn/create", methods=["POST"])
def get_prn():
    """GET PAYMENT PRN"""
    return jsonify({"response": "Works!"}), 200


@app.route("/api/v1/payment-prn/cancel", methods=["DELETE"])
def cancel_prn():
    """CANCEL PAYMENT PRN"""

    return jsonify({"data": "Cancel Success"}), 201


@app.route("/api/v1/payment-prn/check-status", methods=["POST"])
def check_prn():
    """CHECK PAYMENT PRN STATUS"""
    try:

        encryptedCredential = encryption.encryptCredentials()
        signature = encryption.getEncryptionSignature(encryptedCredential)

        request_data = {
            "strPRN": "2210000022848",
            "concatenatedUsernamePasswordSignature": signature,
            "encryptedConcatenatedUsernamePassword": encryptedCredential.decode(
                "utf-8"
            ),
            "userName": encryption.MDA_USERNAME,
        }
        print(request_data)

        response = Client(
            wsdl="http://196.10.228.48/MDAPaymentService/PaymentServices.svc?wsdl",
            settings=settings,
        )
        print("kettfyt")
        response.service.CheckPRNStatus(**request_data)
        print(request_data)
        print(response)

        return (
            jsonify({"response": response}),
            200,
        )
    except Exception as error:
        print(error)
        return jsonify({"message": "Error occurred", "error": str(error)}), 400
