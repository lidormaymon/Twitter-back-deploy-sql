from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,  TweetLike, Tweets, TweetComment, LikeComment, Followers, Conversation, Message

admin.site.register(CustomUser)
admin.site.register(Followers)
admin.site.register(Tweets)
admin.site.register(TweetLike)
admin.site.register(TweetComment)
admin.site.register(LikeComment)
admin.site.register(Conversation)
admin.site.register(Message)


