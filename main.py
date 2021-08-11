import requests


def get_latest_articles():
    response = requests.get('https://mapping-test.fra1.digitaloceanspaces.com/data/list.json')
    print(response.json())


def get_article_details(article_id):
    response = requests.get(f'https://mapping-test.fra1.digitaloceanspaces.com/data/articles/{article_id}.json')
    print(response.json())


if __name__ == '__main__':
    get_latest_articles()
    get_article_details(7793136)
