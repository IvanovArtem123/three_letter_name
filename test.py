import requests
from http.cookiejar import CookieJar
import json

URiL = 'https://soul-goodman.space:8443/qgwcqFXkhD6gxZqHlT/login'
data = {
    'username': 'V8Y21-!fvwdhg9G',
    'password': '4216GUYSA-!0@N#hf123'
}

# response = requests.post(URL, json=data)
# print(response.cookies)
URL = 'https://soul-goodman.space:8443/qgwcqFXkhD6gxZqHlT/panel/api/inbounds/addClient'
settings_data = {
    'clients': [
        {
            'id': '06c3c327-c619-4998-9bb3-adaced38c68b',
            'flow': '',
            'email': 'dsfsd213',
            'limitIp': 0,
            'totalGB': 0,
            'expiryTime': 0,
            'enable': True,
            'tgId': '',
            'subId': '86xi6py5uwsgokh1',
            'comment': '',
            'reset': 0
        }
    ]
}
data = {
    "id": 1,
    "settings": json.dumps(settings_data)  # 👈 результат: '{"clients": [{"id": "..."}]}'
}
cookie_jar = requests.cookies.RequestsCookieJar()
cookie_jar.set('3x-ui', 'MTc3NzQ5NDM0MHxEWDhFQVFMX2dBQUJFQUVRQUFCOV80QUFBUVp6ZEhKcGJtY01EQUFLVEU5SFNVNWZWVk5GVWpCbmFYUm9kV0l1WTI5dEwyMW9jMkZ1WVdWcEx6TjRMWFZwTDNZeUwyUmhkR0ZpWVhObEwyMXZaR1ZzTGxWelpYTF9nUU1CQVFSVmMyVnlBZi1DQUFFREFRSkpaQUVFQUFFSVZYTmxjbTVoYldVQkRBQUJDRkJoYzNOM2IzSmtBUXdBQUFCVl80SlNBUUlCRDFZNFdUSXhMU0ZtZG5ka2FHYzVSd0U4SkRKaEpERXdKSGhxY1d4cWR5NVhUR2RKY1VkcVJuRTNRVWt5TjA5elVtTjNTSGh6ZWpnek5VUlpiRzFJU0hWRUwyTnRTbnA1TUhOdlMxUjVBQT09fFfSvZj7GpM-FtoCWhGYygJOpf2beR9t62yLCPlxu4nO', 
                     domain='soul-goodman.space', 
                     path='/')

response = requests.post(URL, json=data, cookies=cookie_jar)
print(response.text)