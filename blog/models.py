from django.db import models
from django.contrib.auth.models import User

# Models

class Category(models.Model):
    name = models.CharField(max_length = 30)

    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class Post(models.Model):
    title = models.CharField(max_length = 255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)
    categories = models.ManyToManyField('Category', related_name = 'posts')
    image = models.ImageField(upload_to = 'post_images/', blank = True, null = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

class Comments(models.Model):
    author = models.CharField(max_length = 60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)
    post = models.ForeignKey('Post', on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.author} on '{self.post}'"


class Report(models.Model):
    REASON_CHOICES = [
        ('inappropriate', 'Inappropriate Content'),
        ('spam', 'Spam'),
        ('bullying', 'Bullying'),
        ('other', 'Other'),
        ]
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete = models.CASCADE)
    reason = models.CharField(max_length = 20, choices = REASON_CHOICES)
    details = models.TextField(blank = True)
    created_on = models.DateTimeField(auto_now_add = True)
    resolved = models.BooleanField(default = False)

    def __str__ (self):
        return f'{self.post} reported by: {self.reported_by}'
