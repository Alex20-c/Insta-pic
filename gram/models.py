from django.db import models
from django.contrib.auth.models import User
import datetime as dt


class Tag(models.Model):
    """ class to indicate the category of the image"""
    name = models.CharField(max_length=30)


class Profile(models.Model):
    profile_photo = models.ImageField(upload_to='profiles/', null=True)
    bio = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        '''
        Display for profiles in profile table
        '''
        return self.user.username

    @classmethod
    def get_profiles(cls):
        '''
        Fucntion that gets all the profiles in the app
        Return
        '''
        profiles = Profile.objects.all()

        return profiles

    @classmethod
    def search_by_grammer(cls, search_term):
        query = cls.objects.filter(bio__icontains=search_term)
        return query


class Image(models.Model):
    image = models.ImageField(upload_to='photos/', null=True)
    image_name = models.CharField(max_length=30, null=True)
    image_caption = models.TextField(max_length=100, null=True, blank=True)
    likes = models.IntegerField(default=0)
    date_uploaded = models.DateTimeField(auto_now_add=True, null=True)
    profile = models.ForeignKey(Profile, null=True)
    user = models.ForeignKey(User, null=True)

    class Meta:
        ordering = ['-date_uploaded']

    def save_image(self):
        '''Method to save an image in the database'''
        self.save()

    def delete_image(self):
        ''' Method to delete an image from the database'''
        self.delete()

    def __str__(self):
        return self.image_name

    @classmethod
    def get_images(cls):
        '''
        Method that gets all image posts from the database
        Returns:
            images : list of image post objects from the database
        '''
        images = Image.objects.all()
        return images


class Comment(models.Model):
    '''
    Class that defines a Comment on a Post
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Image, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

    @classmethod
    def get_post_comments(cls, post_id):
        ''' Function that gets all the comments belonging to a single post
        Args:
            post_id : specific post
        Returns:
            comments : List of Comment objects for the specified post
        '''
        comments_list = Comment.objects.filter(post=post_id)

        return comments_list


class Like(models.Model):
    '''
    Class that define the likes a post gets
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Image, on_delete=models.CASCADE)
    likes_number = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    @classmethod
    def get_post_likes(cls, post_id):
        '''
        Function that gets the likes belonging to a specified post
        Args:
            post_id : specific post
        Returns:
            post_likes : List of Like objects for the specified post
        '''
        post_likes = Like.objects.filter(post=post_id)

        return post_likes

    @classmethod
    def num_likes(cls, post_id):
        '''
        Function that gets the total number of likes a post hasLegal
        Args:
            post_id : specific post
        Returns:
            found_likes : number of likes a post has
        '''
        post = Like.objects.filter(post=post_id)


class Follow(models.Model):
    '''
    Class that store a User and Profile follow status
    '''
    user = models.ForeignKey(User)
    profile = models.ForeignKey(Profile)

    def __str__(self):
        return self.user.username

    @classmethod
    def get_following(cls, user_id):
        following = Follow.objects.filter(user=user_id).all()
        return following
