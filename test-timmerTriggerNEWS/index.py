import requests
from os import environ
from bs4 import BeautifulSoup
# cd=environ['mongoCD']
from pymongo import MongoClient
import time as t
import logging 
# Function to fetch the top health news stories from a given newspaper


def get_top_health_news():
    newspapers = [
        {
            'name': 'NEW YORK TIMES NEWS',
            'url': 'https://www.nytimes.com/international/section/health'
        },
        {
            'name': 'FOX NEWS',
            'url': 'https://www.foxnews.com/health'
        }
    ]

    top_news = []

    for newspaper in newspapers:
        response = requests.get(newspaper['url'])
        soup = BeautifulSoup(response.text, 'html.parser')

        # Limit to the top 5 articles
        news_articles = soup.find_all('article')[:3]

        for article in news_articles:
            titles = article.find_all(['h2', 'h3']) if article.find_all(['h2', 'h3']) else None
            title = ' '.join(title.text.strip() for title in titles)
            summary =  article.find('p').text.strip() if article.find('p') else None
            image = article.find('img')['src'] if article.find('img') else None
            link = article.find('a')['href'] if article.find('a')['href'] else None

            top_news.append({
                'newspaper': newspaper['name'],
                'title': title,
                'summary': summary,
                'link': link,
                'image': image,
                'time': t.localtime()
            })

    return top_news


def store_in_mongodb(articles):
    try:
        client = MongoClient("mongodb+srv://admin:admin@cluster29543.knkltc6.mongodb.net/")
        db = client['health_news']
        collection = db['articles']
        collection.insert_many(articles)
    except Exception as e:
        logging.info(e)


# Example usage
top_health_news = get_top_health_news()
store_in_mongodb(top_health_news)
logging.info(f"Stored top 5 health news stories.")
# Print the results

# Main function to fetch news stories from multiple sources and store in MongoDB
for news in top_health_news:
    logging.info(f"Newspaper: {news['newspaper']}")
    logging.info(f"Title: {news['title']}")
    logging.info(f"Summary: {news['summary']}")
    logging.info(f"Link: {news['link']}")
    logging.info(f"image: {news['image']}")
    logging.info(f"time: {t.localtime()}")
    logging.info("---------------------")


if __name__ == "__main__":
    print("HI FUNCTION TIRGGER")
    get_top_health_news()
