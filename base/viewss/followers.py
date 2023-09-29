from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..seralizer import  FollowersSerializer
from ..models import CustomUser,  Followers

@api_view(['POST'])
def is_follower_exists(request):
    from_user_id = request.data.get('from_user_id')
    to_user_id = request.data.get('to_user_id')

    if from_user_id is not None and to_user_id is not None:
        follower_exists = Followers.follower_exists(from_user_id=from_user_id, to_user_id= to_user_id)

        if follower_exists:
            like_id = Followers.objects.get(from_user_id=from_user_id, to_user_id=to_user_id).id
            response_data = {
                'from_user_id': from_user_id,
                'to_user_id': to_user_id,
                'follower_exists': follower_exists,
                'like_id': like_id,
            }
        else:
            response_data = {
                'from_user_id': from_user_id,
                'to_user_id': to_user_id,
                'follower_exists': follower_exists,
            }

        return Response(response_data)
    else:
        return Response({'error': 'from_user_id and to_user_id are required.'}, status=400)
    
@api_view(['POST'])
def followers_following_count(request):
    user_id = request.data['user_id']

    try:
        user = CustomUser.objects.get(pk=user_id)
        followers_count = user.follower.count()  # Count the number of followers for the user
        following_count = user.following.count()  # Count the number of users the user is following

        return Response({
            'followers_count': followers_count,
            'following_count': following_count,
        })
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    
@api_view(['POST'])
def followers_list(request):
    user_id = request.data.get('user_id')

    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    followers = Followers.objects.filter(to_user_id=user)
    following = Followers.objects.filter(from_user_id=user)

    followers_serializer = FollowersSerializer(followers, many=True)
    following_serializer = FollowersSerializer(following, many=True)

    followers_user_ids = [follower['from_user_id'] for follower in followers_serializer.data]
    following_user_ids = [followed['to_user_id'] for followed in following_serializer.data]


    return Response({
        'followers': [{'user_id': follower_id} for follower_id in followers_user_ids],
        'following': [{'user_id': following_id} for following_id in following_user_ids],
    })

class FollowerAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            follower = Followers.objects.get(pk=pk)
            serializer = FollowersSerializer(follower)
            return Response(serializer.data)
        followers = Followers.objects.all()
        serializer = FollowersSerializer(followers, many=True)
        return Response(serializer.data)

    @permission_classes([IsAuthenticated])
    def post(self, request):
        serializer = FollowersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        follower = Followers.objects.get(pk=pk)
        follower.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)