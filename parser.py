import requests
from bs4 import BeautifulSoup

# URL страницы
def get_links(query):
    url = f'https://www.google.com/search?q={query}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = []
    for item in soup.find_all('h3'):
        parent = item.find_parent('a')
        if parent and 'href' in parent.attrs:
            url = parent['href']
            border = url.find('&sa')
            # print(url[7:border])
            links.append(url[7:border])

    return links[:10]  # Возвращаем первые n ссылок

user_query = "туристические места Архангельская область"
urls = get_links(user_query)
# for url in urls:
#     print(url)

# "https://www.tourister.ru/responses/id_43115"
# urls = ["https://travel.yandex.ru/journal/arhangelskaya-oblast/",
#         "https://www.kp.ru/russia/arhangelsk/dostoprimechatelnosti/?ysclid=m4cnvuyibd964033673",]
    
def parse_from_web(url):
    response = requests.get(url)

    if response.status_code == 200:
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        tag = soup.body

        if tag == None:
            return ''

        parse_text = ''
        for row in tag.strings:
            parse_text += row
        return parse_text
    else:
        return ''

def get_urls_places():
    pass

def get_urls_review():
    pass

result_string = ''
for url in urls:
    result_string += parse_from_web(url)
# print(result_string)
