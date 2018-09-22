import requests, uuid, datetime
from httmock import all_requests, urlmatch, response

class MockOrder:

    @all_requests
    def mock_order_response(self, url, request):
        content = {
                    "client_id": str(uuid.uuid4()),
                    "created_at": str(datetime.datetime.now()),
                    "id": "f262b0b6-be59-11e8-9e8b-e24b8e248ee6",
                    "location": "Bukoto",
                    "menu_id": str(uuid.uuid4()),
                    "quantity": 2,
                    "status": "pending"
                }
        status_code= 200
        header = {'content-type': 'application/json'}

        return response(status_code, content, header)