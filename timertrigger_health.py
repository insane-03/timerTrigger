import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

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
            titles = article.find_all(['h2', 'h3'])
            title = ' '.join(title.text.strip() for title in titles)
            summary = article.find('p').text.strip()
            link = article.find('a')['href']

            top_news.append({
                'newspaper': newspaper['name'],
                'title': title,
                'summary': summary,
                'link': link
            })

    return top_news


def store_in_mongodb(articles):
    client = MongoClient(
        'mongodb+srv://admin:admin@cluster29543.knkltc6.mongodb.net/')
    db = client['health_news']
    collection = db['articles']
    collection.insert_many(articles)


# Example usage
top_health_news = get_top_health_news()
store_in_mongodb(top_health_news)
print(f"Stored top 5 health news stories.")
# Print the results

# Main function to fetch news stories from multiple sources and store in MongoDB
for news in top_health_news:
    print(f"Newspaper: {news['newspaper']}")
    print(f"Title: {news['title']}")
    print(f"Summary: {news['summary']}")
    print(f"Link: {news['link']}")
    print("---------------------")


if __name__ == "__main__":
    print("HI FUNCTION TIRGGER")
    def handler():
        get_top_health_news()
