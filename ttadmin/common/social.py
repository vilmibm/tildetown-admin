from mastodon import Mastodon
import tweepy

from django.conf import settings

mastodon = Mastodon(
    client_id=settings.MASTO_CLIENT_ID,
    client_secret=settings.MASTO_CLIENT_SECRET,
    access_token=settings.MASTO_ACCESS_TOKEN,
    api_base_url=settings.MASTO_BASE_URL
)

tw_auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
tw_auth.set_acces_token(settings.TWITTER_TOKEN, settings.TWITTER_TOKEN_SECRET)
twitter = tweepy.API(tw_auth)

def post_to_social(qs):
    users = ''
    for townie in qs:
        users += '~{}\n'.format(townie.username)
    users = users.strip()
    if len(qs) != 0:
        message = 'Welcome new users!!!\n\n{}'.format(users)
    else:
        message = 'Welcome new user {}'.format(users)
    mastodon.post(message)
    twitter.update_status(message)

