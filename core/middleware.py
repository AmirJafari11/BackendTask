import json
from bs4 import BeautifulSoup

from rest_framework.request import Request
from rest_framework.response import Response


class CustomMiddleware:
    """
        This custom middleware modifies the response.
        The response will be like:
                        {
                            "result":
                            "status":
                            "success":
                            "message":
                        }
    """

    _notMiddleware = ['/api/docs/']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Request) -> Response:

        response = self.get_response(request)
        if request.path in CustomMiddleware._notMiddleware:
            return response
        content_string = response.content.decode('utf-8')

        if not ('application/json' in response.headers['Content-Type']):
            soup = BeautifulSoup(content_string, 'html.parser')
            pre_tag1 = soup.find('div', class_="response-info")
            if pre_tag1 is None:
                return response
            pre_tag2 = pre_tag1.find('pre', class_='prettyprint')
            pre_tag3 = list(pre_tag2.get_text())
            pre_tag4 = pre_tag3[83:]
            pre_tag5 = ''.join(pre_tag4)
            try:
                response_dict = {
                            "result": json.loads(pre_tag5) if response.status_code < 400 else [],
                            "status": response.status_code,
                            "success": True if response.status_code < 400 else False,
                            "message": [] if response.status_code < 400 else json.loads(pre_tag5)
                        }
            except json.JSONDecodeError:
                response_dict = {
                    "result": [],
                    "status": [],
                    "success": [],
                    "message": []
                }
                response.content = bytes(json.dumps(response_dict), 'utf-8')
                response["Content-Type"] = "application/json"
                return response
            else:
                response.content = bytes(json.dumps(response_dict), 'utf-8')
                response["Content-Type"] = "application/json"
                return response

        else:
            response_dict = {
                "result": json.loads(response.content.decode('utf-8')) if response.status_code < 400 else [],
                "status": response.status_code,
                "success": True if response.status_code < 400 else False,
                "message": [] if response.status_code < 400 else json.loads(response.content.decode('utf-8'))
            }
            response.content = bytes(json.dumps(response_dict), 'utf-8')
            response["Content-Type"] = "application/json"
            return response
