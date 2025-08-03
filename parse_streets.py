import requests
from bs4 import BeautifulSoup

def fetch_streets():
    url = "https://www.kayan.ru/ulicy"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    streets_divs = soup.select('div.streets-name a')

    streets = []
    for a in streets_divs:
        href = a['href']
        name_raw = a.text.strip()
        # Убираем "ул." или "улица" в конце, если есть
        name = name_raw.replace('ул.', '').replace('улица', '').strip()
        # Кол-во новостроек пока ставим 0
        newbuild_count = 0
        streets.append((name, href, newbuild_count))

    return streets

def generate_html(streets):
    html_blocks = []
    for name, href, count in streets:
        block = f'''
<a href="{href}" class="block p-3 hover:bg-gray-50 rounded-md transition">
    <div class="flex justify-between items-center">
        <span class="font-medium">{name}</span>
        <span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">{count} новостроек</span>
    </div>
</a>
'''
        html_blocks.append(block)
    return '\n'.join(html_blocks)

def save_to_file(html_content, filename='streets.html'):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

def main():
    streets = fetch_streets()
    html = generate_html(streets)
    save_to_file(html)
    print(f"Готово! Сохранено в файл streets.html с {len(streets)} улицами.")

if __name__ == '__main__':
    main()
