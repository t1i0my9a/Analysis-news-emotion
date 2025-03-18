import feedparser
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns

#World news RSS
RSS_FEEDS = {
    "Asia": ["https://www.bbc.com/news/world/asia/rss.xml"],
    "Europe": ["https://www.bbc.com/news/world/europe/rss.xml"],
    "Africa": ["https://www.bbc.com/news/world/africa/rss.xml"],
    "North America": ["https://moxie.foxnews.com/google-publisher/us.xml"],
    "South America": ["https://www.bbc.com/news/world/latin_america/rss.xml"],
    "Oceania": ["https://www.news.com.au/content-feeds/latest-news-national/"]}

#List that store result
continents = []
sentiment_scores = []

for continent, urls in RSS_FEEDS.items():
    print(f"===== {continent} News =====")
    total_sentiment = 0 #emotion amount
    count = 0 #article number

    for url in urls:
        feed = feedparser.parse(url)
        
        #when the article can't find, display error message
        if not feed.entries:
            print(f"There isn't the {continent} article ({url})\n")
            continue
        #analysis emotion
        for entry in feed.entries[:10]: #Get current 10 news
             title = entry.title
             analysis = TextBlob(title)
             sentiment = analysis.sentiment.polarity

             total_sentiment += sentiment
             count += 1

             
             #judge emotion
             if sentiment > 0:
                 mood = "Positive!"
             elif sentiment < 0:
                 mood = "Negative..."
             else:
                 mood = "neutral"

             print(f"Sentiment:{mood}({sentiment:.2f})")#display second decimal point
             print(f"Title:{entry.title}") 
             print("-" * 40)
#Each continent emotion
    if count > 0:
      avg_sentiment = total_sentiment / count
      if avg_sentiment > 0:
          overall_mood = "Approximately positive!"
      elif avg_sentiment < 0:
          overall_mood = "Approximately negative..."
      else:
          overall_mood = "Moderation"
    else:
        avg_sentiment = 0
        overall_mood = "unavailable"

        

    print(f"{continent} Overall Sentiment: {overall_mood} ({avg_sentiment:.2f})\n")#display second decimal point

    #add list
    continents.append(continent)
    sentiment_scores.append(avg_sentiment)

    #visualization
    plt.figure(figsize = (10,5))#decide graph size
    colors = ["blue" if score > 0 else "red" for score in sentiment_scores]
    sns.barplot(x = continents, y = sentiment_scores, hue = continents, palette = colors)#x axis is continents, y axis is sentiment_scores, if the score positive, the color is blue, if the score negetive, the color is red
    
    #x axis labelling
    plt.xlabel("Continent", fontsize = 12)
    #y axis labelling
    plt.ylabel("Average Sentiment Score", fontsize = 12)
    #The overall graph labelling
    plt.title("Analysis emotion of grobal news by continent", fontsize = 16)
    #add 0 line
    plt.axhline(0, color = "black", linewidth = 1)
    plt.savefig("sentiment_analysis.png")#save image
    plt.show()
