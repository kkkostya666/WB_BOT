from services.abs import BaseRequestHandler


class CheckStocks(BaseRequestHandler):
    @staticmethod
    def check_stocks_get(auth_token, dateFrom):
        headers = {
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = CheckStocks.send_get_request(
            f'https://statistics-api.wildberries.ru/api/v1/supplier/stocks?dateFrom={dateFrom}', headers)

        if 'error' in response:
            return response
        print(response)
        return response
