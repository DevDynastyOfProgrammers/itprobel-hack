import requests
from bs4 import BeautifulSoup

# URL страницы
url = "https://travel.yandex.ru/journal/arhangelskaya-oblast/"

# Отправляем GET-запрос на страницу
response = requests.get(url)

# Проверяем, что запрос выполнен успешно
if response.status_code == 200:
    # Устанавливаем правильную кодировку
    response.encoding = response.apparent_encoding

    # Создаем объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим все теги <p>
    paragraphs = soup.find_all('p')

    # Извлекаем текст из каждого параграфа и объединяем их в одну строку
    paragraph_texts = [para.get_text(strip=True) for para in paragraphs]
    result_string = " ".join(paragraph_texts)  # Объединяем тексты с пробелами

    # # Если надо записать результат в файл
    # with open("output.txt", "w", encoding="utf-8") as file:
    #     file.write(result_string)
    #
    # # Если надо вывести результат на экран
    print(paragraphs)
else:
    print(f"Ошибка при запросе страницы: {response.status_code}")
