from django.db import models
from django.contrib.auth.models import User


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

GENRES = (
    ('blog', "Blog"),
    ('politics', 'Politics'),
    ('food', 'Food'),
    ('fiction', 'Fiction'),
    ('speech', 'Speech'),
    ('lifestyle', 'LifeStyle'),
    ('sports', 'Sports'),
    ('diy', 'DIY'),
    ('fitness', 'Fitness'),
    ('travel', 'Travel'),
    ('fashion', 'Fashion'),
    ('tech', 'Tech'),
    ('games', 'Games'),
    ('movie_shows', 'Movie_shows')
    )

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    genre = models.CharField( max_length=30,choices=GENRES, default='blog')
    content = models.TextField()
    Description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    tags = models.CharField(max_length=200)
    img = models.ImageField(upload_to = "images/") 

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("post_detail", kwargs={"slug": str(self.slug), "genre": str(self.genre)})



class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)



# class Registrationdata(models.Model):
#     name = models.CharField(max_length = 30)
#     password = models.CharField(max_length = 30)
#     def __str__(self):
#         return self.name


# class Login(models.Model):
#     name = models.CharField(max_length = 30)
#     password = models.CharField(max_length = 30)
#     def __str__(self):
#         return self.name