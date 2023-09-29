from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image

# <----------------------------------------------- User Model ------------------------------------------------------->

class CustomUser(AbstractUser):
    is_verified = models.BooleanField(default=False)
    display_name = models.CharField(max_length=20, null=False, blank=False)
    profile_image = models.ImageField(null=True, blank=True, default='defaultProfile.jpg', upload_to='profiles/')
    bio = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Override the save method to resize the image before saving it.
        super().save(*args, **kwargs)

        # Check if the profile image exists and resize it if necessary.
        if self.profile_image and hasattr(self.profile_image, 'path'):
            img_path = self.profile_image.path
            try:
                with Image.open(img_path) as img:
                    # Resize the image to exactly 225x225 pixels.
                    img = img.resize((225, 225), Image.ANTIALIAS)  # Use Image.ANTIALIAS for better quality resizing.
                    img.save(img_path, quality=100)  # Set quality to 100 for maximum quality.
            except Exception as e:
                # Handle the exception if any error occurs during image processing.
                print(f"Error resizing image: {str(e)}")

# <----------------------------------------------- Followers Model ---------------------------------------------->

class Followers(models.Model):
    id = models.AutoField(primary_key=True)
    from_user_id = models.ForeignKey( 
        CustomUser, on_delete=models.CASCADE, related_name='following'
    )
    to_user_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='follower' 
    )
    created_time =  models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('from_user_id', 'to_user_id')

    @classmethod
    def follower_exists(cls, from_user_id, to_user_id):
        return cls.objects.filter(from_user_id=from_user_id, to_user_id=to_user_id).exists()

# <----------------------------------------------- Tweets Model ---------------------------------------------->

class Tweets(models.Model):
    id = models.AutoField(primary_key=True)
    created_time = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE
    )
    comments = models.IntegerField(default=0)
    edit = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    text = models.CharField(max_length=40 , null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='tweets/')

    def save(self, *args, **kwargs):
        # Override the save method to resize the image before saving it.
        super().save(*args, **kwargs)

        # Check if the profile image exists and resize it if necessary.
        if self.image and hasattr(self.image, 'path'):
            img_path = self.image.path

            try:
                with Image.open(img_path) as img:
                    # Resize the image to exactly 225x225 pixels.
                    img = img.resize((225, 225), Image.ANTIALIAS)  # Use Image.ANTIALIAS for better quality resizing.
                    img.save(img_path, quality=100)  # Set quality to 100 for maximum quality.
            except Exception as e:
                # Handle the exception if any error occurs during image processing.
                print(f"Error resizing image: {str(e)}")

# <----------------------------------------------- Tweets Like Model ---------------------------------------------->

class TweetLike(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE
    )
    tweet_id = models.ForeignKey(
        Tweets, on_delete=models.CASCADE, related_name='like'
    )
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_id', 'tweet_id')
    
    @classmethod
    def like_exists(cls, user_id, tweet_id):
        return cls.objects.filter(user_id=user_id, tweet_id=tweet_id).exists()
    
# <----------------------------------------------- Tweet Comments Model ---------------------------------------------->

class TweetComment(models.Model):
    id = models.AutoField(primary_key=True)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    text = models.CharField(max_length=40 , null=True, blank=True)
    edit = models.BooleanField(default=False)
    user_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE
    )
    tweet_id = models.ForeignKey(
        Tweets, on_delete=models.CASCADE, related_name='tweet_comment'
    )
    created_time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to='comments/')

# <----------------------------------------------- Tweets Comment Like Model ---------------------------------------------->    

class LikeComment(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE
    )
    comment_id = models.ForeignKey(
        TweetComment, on_delete=models.CASCADE, related_name='liked_comment'
    )
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_id', 'comment_id')
    
    @classmethod
    def like_exists(cls, user_id, comment_id):
        return cls.objects.filter(user_id=user_id, comment_id=comment_id).exists()
    
# <----------------------------------------------- Chats Models ---------------------------------------------->    
    
class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='conversations_as_user1')
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='conversations_as_user2')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.user1} and {self.user2} ({self.id})"

    class Meta:
        unique_together = ('user1', 'user2')


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to='messages/')
    

    def __str__(self):
        recipient = self.conversation_id.user2
        con_id = self.conversation_id.id
        return f'{self.sender_id} to {recipient}: {self.text}. Conversation_id({con_id})'
    
    def save(self, *args, **kwargs):
        # Override the save method to resize the image before saving it.
        super().save(*args, **kwargs)

        # Check if the profile image exists and resize it if necessary.
        if self.image and hasattr(self.image, 'path'):
            img_path = self.image.path

            try:
                with Image.open(img_path) as img:
                    # Resize the image to exactly 225x225 pixels.
                    img = img.resize((225, 225), Image.ANTIALIAS)  # Use Image.ANTIALIAS for better quality resizing.
                    img.save(img_path, quality=100)  # Set quality to 100 for maximum quality.
            except Exception as e:
                # Handle the exception if any error occurs during image processing.
                print(f"Error resizing image: {str(e)}")