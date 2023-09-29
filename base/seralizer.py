from rest_framework import serializers
from .models import  CustomUser, Followers,  TweetLike, Tweets, TweetComment, LikeComment, Message, Conversation

class CustomUserSerializer(serializers.ModelSerializer):
    # Add a custom 'password' field to handle write operations
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def update(self, instance, validated_data):
        # Update the user's attributes (excluding 'password')
        for attr, value in validated_data.items():
            if attr != 'password':
                setattr(instance, attr, value)

        # Handle password update
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance

class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = '__all__'


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweets
        fields = '__all__'

class TweetLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetLike
        fields = '__all__'

class TweetCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetComment
        fields = '__all__'

class TweetLikeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeComment
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'