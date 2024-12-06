import requests
from bs4 import BeautifulSoup

# URL страницы
urls = ["https://travel.yandex.ru/journal/arhangelskaya-oblast/",
        "https://www.kp.ru/russia/arhangelsk/dostoprimechatelnosti/?ysclid=m4cnvuyibd964033673"]
    
def parse_from_web(url):
    response = requests.get(url)

    if response.status_code == 200:
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        tag = soup.body

        parse_text = ''
        for row in tag.strings:
            parse_text += row
        return parse_text
    else:
        return ''

result_string = ''
for url in urls:
    result_string += parse_from_web(url)