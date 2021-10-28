import requests

import sys
from bs4 import BeautifulSoup

host = "https://stackoverflow.com"
post_list = []


def get_posts(url, max_depth=0):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/94.0.4606.81 Safari/537.36'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    bs = BeautifulSoup(response.text, "html.parser")
    posts = bs.select('a[class="question-hyperlink"]')

    post_list.extend(posts)
    print('#', end="")

    if max_depth > 0:
        max_depth -= 1
        for link in posts:
            get_posts(host + link.get('href'), max_depth)


def write_to_file(line):
    with open('links.txt', 'a') as file:
        file.write(line + "\n")


get_posts('https://stackoverflow.com/questions', 1)

args = sys.argv
print_in_file = False
if len(args) > 1:
    print_in_file = args[1] == "-file" if True else False

for post_link in post_list:
    link_text = host + post_link.get('href')
    if print_in_file:
        write_to_file(link_text)
    else:
        print(link_text)

print(f'Parsed {len(post_list)} links')