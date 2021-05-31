import tweepy

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
hashtag = '#transengland21'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

latest = 1
for tweet in tweepy.Cursor(api.search, q='hashtag', since_id=latest).items():
    latest = max(latest, tweet.id)
    print(tweet.id, tweet.author.screen_name, tweet.created_at,
          tweet.entities['media'][0]['url'] if 'media' in tweet.entities else tweet.text)
