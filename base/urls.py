from django.urls import path
from .viewss import tweets
from .viewss import auth
from .viewss import followers
from .viewss import chats
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', auth.register),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', auth.MyTokenObtainPairView.as_view()),
    path('user/', auth.UserViewSet.as_view()),  
    path('user/<int:pk>/', auth.UserViewSet.as_view()),
    path('search-users/', auth.search_users, name='search_users'),
    # <--------------------------- Tweets entry points --------------------------->
    path('page-tweets', tweets.page_tweets, name='page_tweets'),
    path('page-tweets/<int:tweet_id>', tweets.page_tweets, name='page_tweets'),
    path('tweets/', tweets.TweetAPIView.as_view()),   
    path('tweets/<pk>/', tweets.TweetAPIView.as_view()), 
    path('user-posts/', tweets.user_posts, name='user_posts'),
    path('user-posts/<int:user_id>', tweets.user_posts, name='user_posts'),  
    path('tweet-like/', tweets.TweetLikeAPIView.as_view()),   
    path('tweet-like/<int:pk>/', tweets.TweetLikeAPIView.as_view()), 
    path('who-liked-tweet/', tweets.who_liked_tweet),
    path('query-likes/', tweets.queryLikes),
    path('tweet-comment/', tweets.TweetCommentAPIView.as_view()),   
    path('tweet-comment/<int:pk>/', tweets.TweetCommentAPIView.as_view()),
    path('page-comments/', tweets.page_comments, name='page-comments'),
    path('page-comments/<int:tweet_id>', tweets.page_comments, name='page-comments'),
    path('query-comments-likes/', tweets.is_comment_likes),
    path('tweet-comment-like/', tweets.TweetCommentLikeAPIView.as_view()),
    path('tweet-comment-like/<int:pk>/', tweets.TweetCommentLikeAPIView.as_view()),
    path('profile-page-tweets/', tweets.page_profile_tweets, name='page_profile_tweets'),
    # <--------------------------- Followers entry points --------------------------->
    path('followers/', followers.FollowerAPIView.as_view()),
    path('followers/<int:pk>/', followers.FollowerAPIView.as_view()),
    path('query-followers/', followers.is_follower_exists),
    path('followers-following-count/', followers.followers_following_count),
    path('followers-list/', followers.followers_list),
    path('following-tweets/', tweets.following_tweets, name='following_tweets'),
    path('profile_liked_tweets/', tweets.profile_liked_tweets, name='profile_liked_tweets'),
    # <--------------------------------- Chats ------------------------------------>
        # <--------------------------------- Conversation ------------------------------------>
        path('conversation/', chats.ConversationAPIView.as_view()),
        path('conversation/<int:pk>/', chats.ConversationAPIView.as_view()),
        path('is-conversation-exist/', chats.is_conversation_exist ),
        path('find-conversation-id/', chats.find_coverstation_id),
        path('find-user-conversations/', chats.fetch_user_conversations),
        # <--------------------------------- Messages ------------------------------------>
        path('messages/', chats.MessageAPIView.as_view()),
        path('messages/<int:pk>/', chats.MessageAPIView.as_view()),
        path('page-messages/', chats.get_messages_pages, name='page_messages'),
        path('page-messages/<int:conversation_id>/', chats.get_messages_pages, name='page_messages'),
]
