from abc import ABC

import requests


class BaseRequestHandler(ABC):

    @staticmethod
    def send_post_request(url, headers, data=None):
        print(f"Sending POST request to {url} with headers: {headers} and data: {data}")
        try:
            response = requests.post(url, data=data, headers=headers)
            print(response.raise_for_status())
            return response.json()
        except requests.RequestException as e:
            print(f"Request exception: {e}")
            return {"error": True, "message": f"Произошла ошибка: {str(e)}"}
        except ValueError as ve:
            print(f"Value error: {ve}")
            return {"error": True, "message": f"Некорректный формат ответа от сервера: {str(ve)}"}

    @staticmethod
    def send_patch_request(url, headers, data=None):
        print(f"Sending PATCH request to {url} with headers: {headers} and data: {data}")
        try:
            response = requests.patch(url, data=data, headers=headers)
            print(response.raise_for_status())
            return response.json()
        except requests.RequestException as e:
            print(f"Request exception: {e}")
            return {"error": True, "message": f"Произошла ошибка: {str(e)}"}
        except ValueError as ve:
            print(f"Value error: {ve}")
            return {"error": True, "message": f"Некорректный формат ответа от сервера: {str(ve)}"}

    @staticmethod
    def send_get_request(url, headers, data=None):
        print(f"Sending GET request to {url} with headers: {headers} and data: {data}")
        try:
            response = requests.get(url, data=data, headers=headers)
            print(response.raise_for_status())
            return response.json()
        except requests.RequestException as e:
            print(f"Request exception: {e}")
            return {"error": True, "message": f"Произошла ошибка: {str(e)}"}
        except ValueError as ve:
            print(f"Value error: {ve}")
            return {"error": True, "message": f"Некорректный формат ответа от сервера: {str(ve)}"}