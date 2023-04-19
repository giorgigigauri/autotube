from reddit import RedditAPI
from dotenv import load_dotenv
import os
from utils.CreateMovie import CreateMovie, GetDaySuffix

load_dotenv()

reddit = RedditAPI(os.getenv('client_id'), os.getenv('client_secret'), os.getenv('user_agent'))

subreddit = 'Controversial'
post_type = 'top'
duration = 'all'
page = 1
limit = 1

posts = reddit.get_posts(subreddit=subreddit, post_type=post_type, duration=duration, page=page, limit=limit)

for post in posts:
    # Get comments for the post
    submission, comments = reddit.get_comments(post.id, comment_sort='top', limit=4)
    print(f'Title: {submission.title}')
    print(f'Author: {submission.author.name}')
    print(f'URL: {submission.url}')
    print(f'Score: {submission.score}')
    print(f'Number of comments: {submission.num_comments}')
    print(f'Created at: {submission.created_utc}')
    for comment in comments:
        if comment.author is None:
            comment.author = 'None'
        print(f'Comment: {comment.body}')
        print(f'Author: {comment.author.name}')
        print(f'Score: {comment.score}')
        print('---------------------------')

CreateMovie.CreateMP4(submission.title, comments[0].body)