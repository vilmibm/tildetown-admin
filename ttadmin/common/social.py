import re

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

def split_posts_by_length(text, length):
    pattern = '.{,%d}(?:\s|$)' % length - 1
    chunks = re.findall(pattern, text)
    posts = []
    post = ''
    for chunk in chunks:
        if len(post + chunk) <= length:
            post += chunk
        else:
            posts.append(post)
            post = chunk
    if post:
        posts.append(post)
    return posts


def post_to_mastodon(message):
    posts = split_posts_by_length(message, 500)
    status_info = None
    for post in posts:
        if status_info:
            status_info = mastodon.status_post(post, in_reply_to_id=status_info['id'])
        else:
            status_info = mastodon.status_post(post)


def post_to_twitter(message):
    posts = split_posts_by_length(message, 280)
    status_info = None
    for post in posts:
        if status_info:
            status_info = twitter.update_status(post, in_reply_to_status_id=status_info.id)
        else:
            status_info = twitter.update_status(post)


def post_users_to_social(qs):
    users = ''
    for townie in qs:
        users += '~{}\n'.format(townie.username)
    users = users.strip()
    if len(qs) > 1:
        message = 'Welcome new users!!!\n\n{}'.format(users)
    else:
        message = 'Welcome new user {}!'.format(users)
    post_to_mastodon(message)
    post_to_twitter(message)

def post_single_user_social(username):
    message = 'Welcome new user ~{}!'.format(username)
    post_to_mastodon(message)
    post_to_twitter(message)

