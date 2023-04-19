import praw
from typing import List

class RedditAPI:
    def __init__(self, client_id: str, client_secret: str, user_agent: str) -> None:
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent)
    
    def get_posts(self, subreddit: str, post_type: str, duration: str, page: int, limit: int = 5) -> List[praw.models.Submission]:
        if post_type == 'top':
            posts = self.reddit.subreddit(subreddit).top(duration, limit=limit, params={'page': page})
        elif post_type == 'best':
            posts = self.reddit.subreddit(subreddit).best(limit=limit, params={'page': page})
        elif post_type == 'new':
            posts = self.reddit.subreddit(subreddit).new(limit=limit, params={'page': page})
        else:
            raise ValueError("Invalid post type")
        
        return list(posts)
    
    def get_post(self, post_id: str) -> praw.models.Submission:
        post = self.reddit.submission(id=post_id)
        return post
        
    def get_comments(self, post_id: str, comment_sort: str, limit: int = None) -> List[praw.models.Comment]:
        comments = []
        submission = self.get_post(post_id)
        submission.comment_sort = comment_sort
        if limit and limit <= submission.num_comments:
            submission.comments.replace_more(limit=limit)
        else:
            submission.comments.replace_more()
        for comment in submission.comments.list():
            if comment.body != '[deleted]':
                comments.append(comment)
            if limit and len(comments) == limit:
                break
            elif limit and len(comments) < limit and len(comments) == len(submission.comments.list()):
                # If we haven't reached the limit but have fetched all comments, fetch more comments from Reddit API
                submission.comments.replace_more()
        return submission, comments

