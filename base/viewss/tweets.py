from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..seralizer import  TweetSerializer, TweetCommentSerializer, TweetLikeCommentSerializer, TweetLikeSerializer
from ..models import CustomUser, Tweets, TweetLike, TweetComment, LikeComment, Followers

# <--------------------------------- Tweets ------------------------------------>

@api_view(['GET'])
def page_tweets(request):
    try:
        page = int(request.GET.get('page', 1)) 
        tweets_per_page = 10
        start_index = (page - 1) * tweets_per_page
        end_index = start_index + tweets_per_page

        tweets = Tweets.objects.all().order_by('-created_time')[start_index:end_index]
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def page_profile_tweets(request):
    page = int(request.GET.get('page', 1)) 
    
    tweets_per_page = 10
    start_index = (page - 1) * tweets_per_page
    end_index = start_index + tweets_per_page

    user_id = request.GET.get('user_id')  # Get the user ID from the URL parameter

    # Retrieve the user's tweets
    user_tweets = Tweets.objects.filter(user_id=user_id).order_by('-created_time')[start_index:end_index]
    serializer = TweetSerializer(user_tweets, many= True)
    return Response(serializer.data)

@api_view(['POST'])
def user_posts( request):
    user_id = request.data['user_id']

    try:
        user = CustomUser.objects.get(pk=user_id)
        post_count = Tweets.objects.filter(user_id=user).count()
        return Response({'post_count':post_count})
    except CustomUser.DoesNotExist:
        return Response({'error':'User not found'}, status=404) 
    
@api_view(['GET'])
def profile_liked_tweets(request):
    page_number = int(request.GET.get('page', 1))
    user_id = request.GET.get('user_id')



    liked_tweet_ids = TweetLike.objects.filter(user_id=user_id).values_list('tweet_id', flat=True)

    tweets_per_page = 10
    start_index = (page_number - 1) * tweets_per_page
    end_index = start_index + tweets_per_page

    paginated_liked_tweets = Tweets.objects.filter(id__in=liked_tweet_ids).order_by('-created_time')[start_index:end_index]

    serializer = TweetSerializer(paginated_liked_tweets, many=True)



    return Response(serializer.data, status=200)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def following_tweets(request):
    page_number = int(request.GET.get('page', 1)) 
    user_id = request.GET.get('user_id')

    try:
        browsing_user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    following_users = Followers.objects.filter(from_user_id=browsing_user).values_list('to_user_id', flat=True)

    tweets_per_page = 10
    start_index = (page_number - 1) * tweets_per_page
    end_index = start_index + tweets_per_page

    following_tweets = Tweets.objects.filter(user_id__in=following_users).order_by('-created_time')[start_index:end_index]

    serializer = TweetSerializer(following_tweets, many=True)
    return Response(serializer.data)


class TweetAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            tweets = Tweets.objects.get(pk=pk)
            serializer = TweetSerializer(tweets)
            return Response(serializer.data)
        tweets = Tweets.objects.all()
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data)
    


    def post(self, request):
        serializer = TweetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request, pk):
        print(request)
        tweet = Tweets.objects.get(pk=pk)
        serializer = TweetSerializer(tweet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        tweet = Tweets.objects.get(pk=pk)
        tweet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# <---------------------------------Tweet Likes ------------------------------------>

@api_view(['POST'])
def queryLikes(request):
    user_id = request.data.get('user_id')
    tweet_id = request.data.get('tweet_id')

    if user_id is not None and tweet_id is not None:
        like_exists = TweetLike.like_exists(user_id=user_id, tweet_id=tweet_id)

        if like_exists:
            like_id = TweetLike.objects.get(user_id=user_id, tweet_id=tweet_id).id
            response_data = {
                'user_id': user_id,
                'tweet_id': tweet_id,
                'like_exists': like_exists,
                'like_id': like_id,
            }
        else:
            response_data = {
                'user_id': user_id,
                'tweet_id': tweet_id,
                'like_exists': like_exists,
            }

        return Response(response_data)
    else:
        return Response({'error': 'user_id and tweet_id are required.'}, status=400)

@api_view(['POST'])
def who_liked_tweet(request):
    tweet_id = request.data.get('tweet_id')

    if tweet_id is not None:
        tweet_exists = Tweets.objects.filter(id=tweet_id).exists
        if tweet_exists:
            likes = TweetLike.objects.filter(tweet_id=tweet_id)
            likes_serializer = TweetLikeSerializer(likes, many=True)
            likes_user_id = [like for like in likes_serializer.data]

            return Response({
                'likes':likes_user_id
            })
    else:
        return Response({'Error':'tweet_is is required.'}, status=400)


class TweetLikeAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            like = TweetLike.objects.get(pk=pk)
            serializer = TweetSerializer(like)
            return Response(serializer.data)
        likes = TweetLike.objects.all()
        serializer = TweetLikeSerializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TweetLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        like = TweetLike.objects.get(pk=pk)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# <---------------------------Tweet Comments ---------------------------------------->

@api_view(['GET'])
def page_comments(request, tweet_id):
    page = request.GET.get('page', 1)
    try:
        page = int(page)
    except ValueError:
        page = 1

    tweets_per_page = 10
    start_index = (page - 1) * tweets_per_page
    end_index = start_index + tweets_per_page

    comments = TweetComment.objects.filter(tweet_id=tweet_id).order_by('-likes', '-created_time')[start_index:end_index]
    serializer = TweetCommentSerializer(comments, many=True)
    return Response(serializer.data)

class TweetCommentAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            comment = TweetComment.objects.get(pk=pk)
            serializer = TweetCommentSerializer(comment)
            return Response(serializer.data)
        comments = TweetComment.objects.all()
        serializer = TweetCommentSerializer(comments, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = TweetCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        print(request)
        comment = TweetComment.objects.get(pk=pk)
        serializer = TweetCommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = TweetComment.objects.get(pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# <------------------------------------------- Tweet Comment Likes ------------------------------------------>

@api_view(['POST'])
def is_comment_likes(request):
    user_id = request.data.get('user_id')
    comment_id = request.data.get('comment_id')

    if user_id is not None and comment_id is not None:
        like_exists = LikeComment.like_exists(user_id=user_id, comment_id= comment_id)

        if like_exists:
            like_id = LikeComment.objects.get(user_id=user_id, comment_id=comment_id).id
            response_data = {
                'user_id': user_id,
                'comment_id': comment_id,
                'like_exists': like_exists,
                'like_id': like_id,
            }
        else:
            response_data = {
                'user_id': user_id,
                'comment_id': comment_id,
                'like_exists': like_exists,
            }

        return Response(response_data)
    else:
        return Response({'error': 'user_id and comment_id are required.'}, status=400)


class TweetCommentLikeAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            like = LikeComment.objects.get(pk=pk)
            serializer = TweetLikeCommentSerializer(like)
            return Response(serializer.data)
        likes = LikeComment.objects.all()
        serializer = TweetLikeCommentSerializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TweetLikeCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        like = LikeComment.objects.get(pk=pk)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)