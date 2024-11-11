from services.abs import BaseRequestHandler


class CheckToken(BaseRequestHandler):
    @staticmethod
    def update_commission(auth_token):
        headers = {
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = CheckToken.send_get_request(f'https://common-api.wildberries.ru/ping', headers)

        if 'error' in response:
            return response
        print(response)
        return response
