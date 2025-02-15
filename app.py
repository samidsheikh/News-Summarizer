from flask import Flask, render_template, request, redirect, url_for
from newsapi import NewsApiClient
from newspaper import Article
from langchain_groq import ChatGroq
from langchain import PromptTemplate
from langchain.chains import LLMChain
from pymongo import MongoClient
from datetime import datetime, timedelta

app = Flask(__name__, static_folder="static")

# 🔹 Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["news_db"]
history_collection = db["news_history"]
top_news_collection = db["top_news"]

# 🔹 News API Initialize
NEWS_API_KEY = '7bc761d6c7e344de812f86a88a51e6d1'  # Replace with a valid API key
newsapi = NewsApiClient(api_key=NEWS_API_KEY )

# 🔹 LLaMA 3.1 Model Initialize
llm = ChatGroq(
    temperature=0,
    groq_api_key='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',
    model_name="llama3-70b-8192"
)

# 🔹 Prompt Templates
summary_template =  '''Summarize this news article: {topic}. and do not give any title like "Here is a summary of the news article:"'''
summary_prompt = PromptTemplate(input_variables=["topic"], template=summary_template)
summary_chain = LLMChain(llm=llm, prompt=summary_prompt)

sentiment_template = '''Classify sentiment of this news as: good, bad, or average - {topic}.
give only sentiment word do not include any other words in the output'''
sentiment_prompt = PromptTemplate(input_variables=["topic"], template=sentiment_template)
sentiment_chain = LLMChain(llm=llm, prompt=sentiment_prompt)

ner_template = '''Extract named entities from this news: {topic}.
directly give named entities of person,organisation and location.
 give the output in bullet points. and print one entity in one line and give the type of entity in brackets after the entity
 remove title line like:"Here are the named entities extracted from the news:","Here is the output:"
 and if the entity is related to cricket then give players name with their team '''
ner_prompt = PromptTemplate(input_variables=["topic"], template=ner_template)
ner_chain = LLMChain(llm=llm, prompt=ner_prompt)

related_template = '''Classify this news into a category (Technology, Politics, Sports, etc.): {topic}.give only category name do not include any other words in the output'''
related_prompt = PromptTemplate(input_variables=["topic"], template=related_template)
related_chain = LLMChain(llm=llm, prompt=related_prompt)

# 🔹 Helper Functions
def get_summary(news_text):
    return summary_chain.run(news_text).strip()

def get_sentiment(news_text):
    return sentiment_chain.run(news_text).strip().lower()

def get_named_entities(news_text):
    return ner_chain.run(news_text).strip()

def get_related_topic(news_text):
    return related_chain.run(news_text).strip()

def get_top_news():
    try:
        yesterday_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        today_date = datetime.today().strftime('%Y-%m-%d')

        # Fetch news from NewsAPI
        articles = newsapi.get_everything(q='India', language='en', from_param=yesterday_date, to=today_date, sort_by='publishedAt', page_size=10)

        if not articles or 'articles' not in articles or len(articles['articles']) == 0:
            print("No articles found for today.")
            return []

        # Prepare the news list
        news_list = []
        for article in articles['articles']:
            news_text = article['title'] + " " + (article['description'] or "")
            sentiment = get_sentiment(news_text)
            ner = get_named_entities(news_text)
            related_topic = get_related_topic(news_text)

            news_list.append({
                'title': article['title'],
                'url': article['url'],
                'sentiment': sentiment,
                'ner': ner,
                'related_topic': related_topic
            })

        # Store in MongoDB if today's news is not already stored
        existing_news = top_news_collection.find_one({"date": today_date})
        if not existing_news:
            top_news_collection.insert_one({"date": today_date, "news_list": news_list})

        return news_list

    except Exception as e:
        print(f"Error fetching news: {e}")
        return []


# 🔹 Web Scraping for Direct URL
def scrape_news(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except:
        return "Error fetching the article."

# 🔹 Routes
@app.route('/')
def index():
    news_list = get_top_news()  # Fetch top 10 news
    return render_template('index.html', news_list=news_list)

@app.route('/scrape_news', methods=['POST'])
def scrape_news_route():
    url = request.form['news_url']
    full_news = scrape_news(url)
    summary = get_summary(full_news)
    sentiment = get_sentiment(full_news)
    ner = get_named_entities(full_news)
    related_topic = get_related_topic(full_news)

    # Save to MongoDB
    history_collection.insert_one({
        "url": url,
        "summary": summary,
        "sentiment": sentiment,
        "ner": ner,
        "related_topic": related_topic,
        "date": datetime.utcnow()
    })

    return render_template('news_detail.html', summary=summary, sentiment=sentiment, ner=ner, related_topic=related_topic, url=url)

@app.route('/history')
def history():
    history_data = list(history_collection.find().sort("date", -1))
    return render_template('history.html', history_data=history_data)

@app.route('/news')
def news_detail():
    url = request.args.get('url')
    full_news = scrape_news(url)
    summary = get_summary(full_news)
    sentiment = get_sentiment(full_news)
    ner = get_named_entities(full_news)
    related_topic = get_related_topic(full_news)

    return render_template('news_detail.html', summary=summary, sentiment=sentiment, ner=ner, related_topic=related_topic, url=url)

# 🔹 Process Pasted Text
@app.route('/process_text', methods=['POST'])
def process_text():
    news_text = request.form['news_text']
    summary = get_summary(news_text)
    sentiment = get_sentiment(news_text)
    ner = get_named_entities(news_text)
    related_topic = get_related_topic(news_text)

    # Store the searched text analysis in MongoDB
    history_collection.insert_one({
        "url": None,  # No URL, since this is manually pasted text
        "searched_text": news_text,
        "summary": summary,
        "sentiment": sentiment,
        "ner": ner,
        "related_topic": related_topic,
        "date": datetime.utcnow()
    })

    return redirect(url_for('text_analysis', summary=summary, sentiment=sentiment, ner=ner, related_topic=related_topic))


@app.route('/text_analysis')
def text_analysis():
    summary = request.args.get('summary', 'No summary available.')
    sentiment = request.args.get('sentiment', 'N/A')
    ner = request.args.get('ner', 'No named entities found.')
    related_topic = request.args.get('related_topic', 'N/A')

    return render_template('text_analysis.html', summary=summary, sentiment=sentiment, ner=ner, related_topic=related_topic)


if __name__ == '__main__':
    app.run(debug=True)
