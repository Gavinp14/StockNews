from newsapi import NewsApiClient
from textblob import TextBlob

APIKEY = 'e866390d81d8425b8dc75b4837d0aafa'

# Init
newsapi = NewsApiClient(api_key=APIKEY)

# Specify the company you want to fetch news about
company_name = 'OceanGate'

# /v2/everything
all_articles = newsapi.get_everything(q=company_name,
                                      from_param='2024-09-04',
                                      to='2024-10-04',
                                      language='en',
                                      sort_by='relevancy',
                                      )

# Check for errors in all_articles
if all_articles['status'] == 'ok':
    print(f"Articles about {company_name} from October 3 to October 4, 2024:")
    
    # Variables to accumulate sentiment data
    total_sentiment = 0
    total_articles = len(all_articles['articles'])
    good_count = 0
    bad_count = 0
    neutral_count = 0
    
    for article in all_articles['articles']:
        title = article['title']
        description = article['description'] or ''  # Use empty string if description is None
        
        # Combine title and description for analysis
        article_text = f"{title} {description}"
        
        # Perform sentiment analysis
        analysis = TextBlob(article_text)
        sentiment = analysis.sentiment.polarity  # Polarity ranges from -1 (negative) to 1 (positive)
        
        # Determine if the sentiment is good or bad
        if sentiment > 0:
            sentiment_label = 'Good'
            good_count += 1
        elif sentiment < 0:
            sentiment_label = 'Bad'
            bad_count += 1
        else:
            sentiment_label = 'Neutral'
            neutral_count += 1
        
        # Accumulate total sentiment
        total_sentiment += sentiment
        
        # Print article title and sentiment
        print(f"- {title} (Source: {article['source']['name']}) - Sentiment: {sentiment_label} (Polarity: {sentiment})")
    
    # Calculate average polarity and percentages
    average_polarity = total_sentiment / total_articles if total_articles > 0 else 0
    total_sentiment_count = good_count + bad_count + neutral_count
    good_percentage = (good_count / total_sentiment_count * 100) if total_sentiment_count > 0 else 0
    bad_percentage = (bad_count / total_sentiment_count * 100) if total_sentiment_count > 0 else 0
    neutral_percentage = (neutral_count / total_sentiment_count * 100) if total_sentiment_count > 0 else 0
    
    # Print the summary
    print("\nSummary:")
    print(f"Average Polarity: {average_polarity:.2f}")
    print(f"Good Articles: {good_count} ({good_percentage:.2f}%)")
    print(f"Bad Articles: {bad_count} ({bad_percentage:.2f}%)")
    print(f"Neutral Articles: {neutral_count} ({neutral_percentage:.2f}%)")
else:
    print("Error fetching all articles:", all_articles['message'])
