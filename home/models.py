from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    body=models.TextField()
    slug=models.SlugField(max_length=30)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-updated',)

    def __str__(self):
        return f'{self.slug}-{self.updated}'

    def get_absolute_url(self):
        return reverse('home:post_detail',args=[self.id,self.slug])

class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_comment')
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_comment')
    reply=models.ForeignKey('self',on_delete=models.CASCADE,related_name='reply_comment',blank=True,null=True)
    is_reply=models.BooleanField(default=False)
    body=models.TextField(max_length=400)
    created=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return  f'{self.user} - {self.body[:30]} - {self.created}'
