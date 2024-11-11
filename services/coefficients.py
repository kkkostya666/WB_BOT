from services.abs import BaseRequestHandler


class CheckCoef(BaseRequestHandler):
    @staticmethod
    def check_coef(auth_token, warehouseIDs=None):
        headers = {
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        base_url = 'https://supplies-api.wildberries.ru/api/v1/acceptance/coefficients'
        url = f"{base_url}?warehouseIDs={warehouseIDs}" if warehouseIDs else base_url

        response = CheckCoef.send_get_request(url, headers)

        if 'error' in response:
            return response
        print(response)
        return response
