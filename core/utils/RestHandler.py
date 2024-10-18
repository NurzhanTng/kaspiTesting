import aiohttp
import ssl
from core.utils.settings import settings


async def handle_response(response):
    """Обрабатывает ответ от сервера, включая ошибки"""
    if 200 <= response.status < 300:
        # Успешный ответ
        return await response.json()
    else:
        # Обработка ошибок
        try:
            error_message = await response.json()
        except aiohttp.ContentTypeError:
            error_message = await response.text()  # Если тело ответа не JSON
        return {
            'error': f'Status: {response.status}',
            'message': error_message
        }


class RestHandler:
    def __init__(self, verify_ssl: bool = True):
        self.basic_url = settings.api_path
        self.basic_headers = {
            'Content-Type': 'application/json',
        }
        # Создание SSL-контекста на основе параметра
        self.ssl_context = None
        if not verify_ssl:
            self.ssl_context = ssl.create_default_context()
            self.ssl_context.check_hostname = False
            self.ssl_context.verify_mode = ssl.CERT_NONE

    def change_base_url(self, url):
        self.basic_url = url

    async def get(self, url: str, params: dict = None, headers: dict = None):
        try:
            headers = self.merge_headers(headers)
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=self.ssl_context)) as session:
                async with session.get(self.basic_url + url, params=params, headers=headers) as response:
                    return await handle_response(response)
        except aiohttp.ClientError as e:
            return {'error': str(e)}

    async def post(self, url: str, data: dict = None, headers: dict = None):
        try:
            headers = self.merge_headers(headers)
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=self.ssl_context)) as session:
                async with session.post(self.basic_url + url, json=data, headers=headers) as response:
                    return await handle_response(response)
        except aiohttp.ClientError as e:
            return {'error': str(e)}

    async def update(self, url: str, data: dict = None, headers: dict = None):
        try:
            headers = self.merge_headers(headers)
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=self.ssl_context)) as session:
                async with session.put(self.basic_url + url, json=data, headers=headers) as response:
                    return await handle_response(response)
        except aiohttp.ClientError as e:
            return {'error': str(e)}

    async def delete(self, url: str, headers: dict = None):
        try:
            headers = self.merge_headers(headers)
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=self.ssl_context)) as session:
                async with session.delete(self.basic_url + url, headers=headers) as response:
                    return await handle_response(response)
        except aiohttp.ClientError as e:
            return {'error': str(e)}

    def merge_headers(self, custom_headers: dict = None) -> dict:
        """Объединяет базовые заголовки и кастомные заголовки"""
        if custom_headers is None:
            return self.basic_headers
        return {**self.basic_headers, **custom_headers}
