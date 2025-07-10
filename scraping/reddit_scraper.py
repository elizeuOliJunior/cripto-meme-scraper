import praw
import datetime
from firebase.firebase_client import salvar_dados_reddit
from sentiment_analyzer import analyze_sentiment


CLIENT_ID = 'AwzM3Q-xhbLXb1o1Jmpu4w'
CLIENT_SECRET = 'f5Hd9LM1pbQRlR_AD5fNIFJPw06GrA'
USER_AGENT = 'memeCoinScraper_by_No_Anteater_3453'

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
)

def get_subreddit_posts(subreddit_name, limit=100):
    """Coleta posts de um subreddit específico."""
    posts_data = []
    print(f"Coletando posts de r/{subreddit_name}...")
    for submission in reddit.subreddit(subreddit_name).hot(limit=limit):
        post_info = {
            'id': submission.id,
            'title': submission.title,
            'score': submission.score,
            'num_comments': submission.num_comments,
            'url': submission.url,
            'created_utc': datetime.datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
            'selftext': submission.selftext,
            'subreddit': subreddit_name
        }
        sentiment_scores = analyze_sentiment(post_info['title'] + " " + post_info['selftext'])
        post_info.update(sentiment_scores)
        posts_data.append(post_info)
    return posts_data 

def get_submission_comments(submission_id, limit=None):
    """Coleta comentários de um post específico."""
    comments_data = []
    submission = reddit.submission(id=submission_id)
    submission.comments.replace_more(limit=0) 
    print(f"Coletando comentários do post {submission_id}...")
    for comment in submission.comments.list():
        if isinstance(comment, praw.models.Comment): 
            comment_info = {
                'comment_id': comment.id,
                'submission_id': submission_id,
                'author': comment.author.name if comment.author else '[deleted]',
                'body': comment.body,
                'score': comment.score,
                'created_utc': datetime.datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
            }
            sentiment_scores = analyze_sentiment(comment_info['body'])
            comment_info.update(sentiment_scores)
            comments_data.append(comment_info)
    return comments_data 

def scrape_reddit_data(subreddits_to_scrape, posts_limit=50, comments_limit=20):
    print("Iniciando scraping e salvamento no Firebase...")
    for sub in subreddits_to_scrape:
        posts = get_subreddit_posts(sub, limit=posts_limit)
        for post in posts:
            salvar_dados_reddit(post, 'posts')
            comments = get_submission_comments(post['id'], limit=comments_limit)
            for comment in comments:
                salvar_dados_reddit(comment, 'comments')
    print("Scraping do Reddit e salvamento no Firebase concluídos.")

if __name__ == "__main__":
    subreddits_to_scrape = ['CryptoCurrency', 'SatoshiStreetBets', 'dogecoin', 'ShibainuCoin']
    scrape_reddit_data(subreddits_to_scrape)
