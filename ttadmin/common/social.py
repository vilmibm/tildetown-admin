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
tw_auth.set_access_token(settings.TWITTER_TOKEN, settings.TWITTER_TOKEN_SECRET)
twitter = tweepy.API(tw_auth)

def post_to_mastodon(qs):
    posts = []
    if len(qs) > 1:
        welcome = 'Welcome new user '
    else:
        welcome  = 'Welcome new users!!!\n\n'
    message = welcome
    for townie in qs:
        if len(message + townie.username) + 1 > 500:
            posts.append(message.strip())
            message = welcome + '~{}\n'.format(townie.username)
        else:
            message += '~{}\n'.format(townie.username)
    posts.append(message.strip())
    for post in posts:
        mastodon.post(post)

def post_to_twitter(qs):
    posts = []
    if len(qs) > 1:
        welcome = 'Welcome new user '
    else:
        welcome = 'Welcome new users!!!\n\n'
    message = welcome
    for townie in qs:
        if len(message + townie.username) + 1 > 140:
            posts.append(message.strip())
            message = welcome + '~{}\n'.format(townie.username)
        else:
            message += '~{}\n'.format(townie.username)
    posts.append(message.strip())
    for post in posts:
        twitter.update_status(post)

def post_to_social(qs):
    post_to_twitter(qs)
    post_to_mastodon(qs)

