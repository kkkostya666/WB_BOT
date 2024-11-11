from services.abs import BaseRequestHandler


class CheckState(BaseRequestHandler):
    @staticmethod
    def check_sales(auth_token, dateFrom):
        headers = {
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = CheckState.send_get_request(
            f'https://statistics-api.wildberries.ru/api/v1/supplier/sales?dateFrom={dateFrom}', headers)

        if 'error' in response:
            return response
        print(response)
        return response

    @staticmethod
    def check_order(auth_token, dateFrom):
        headers = {
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = CheckState.send_get_request(
            f'https://statistics-api.wildberries.ru/api/v1/supplier/orders?dateFrom={dateFrom}', headers)

        if 'error' in response:
            return response
        print(response)
        return response
