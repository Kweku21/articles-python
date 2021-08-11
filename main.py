import re
import time
import requests
import asyncio
import models
from models import Article, MediaSection


async def get_latest_articles():
    responses = make_http_request(url='https://mapping-test.fra1.digitaloceanspaces.com/data/list.json')

    for response in responses:
        asyncio.create_task(get_article_details(article_id=response['id']))


async def get_article_details(article_id):
    response = make_http_request(
        url=f'https://mapping-test.fra1.digitaloceanspaces.com/data/articles/{article_id}.json')

    article = Article(**response)

    # Stripping HTML elements
    formatted_sections = []

    for section in article.sections:

        if type(section) not in [models.MediaSection]:
            section.text = re.compile(r'<[^>]+>').sub('', section.text)

        elif type(section) is models.MediaSection:
            section = await get_article_media(article_id)

        formatted_sections.append(section)

    article.sections = formatted_sections

    print(article)
    print()


async def get_article_media(article_id):
    responses = make_http_request(url=f'https://mapping-test.fra1.digitaloceanspaces.com/data/media/{article_id}.json')

    return [MediaSection(**response) for response in responses]


def make_http_request(url):

    try:
        response = requests.get(url)
        return response.json()
    except requests.ConnectionError as e:
        print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        print(str(e))
    except requests.Timeout as e:
        print("OOPS!! Timeout Error")
        print(str(e))
    except requests.RequestException as e:
        print("OOPS!! General Error")
        print(str(e))
    except KeyboardInterrupt:
        print("Someone closed the program")


if __name__ == '__main__':

    while True:
        print("============================================================")
        print("===================New Articles Alert=======================")
        print("============================================================")
        asyncio.run(get_latest_articles())

        time.sleep(300)
