import requests
import datetime
from httmock import all_requests, urlmatch, response

class MockOrder:

    @all_requests
    def mock_order_response(self, url, request):
        content = {
                    "client_id": 54321,
                    "created_at": str(datetime.datetime.now()),
                    "id": "12345",
                    "location": "Bukoto",
                    "menu_id": 45455,
                    "quantity": 2,
                    "status": "completed"
                }
        status_code= 200
        header = {'content-type': 'application/json'}

        return response(status_code, content, header)