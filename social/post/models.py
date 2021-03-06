import os
import random
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


def file_name(filename):
    basename = os.path.basename(filename)
    name, ext = os.path.splitext(basename)
    return name, ext


def image_upload(instance, filename):
    name, ext = file_name(filename)
    secondaryName = random.randint(1, 100000)
    finalName = "{name}{secondaryName}".format(
        name=name, secondaryName=secondaryName)
    imageName = "{finalName}{ext}".format(finalName=finalName, ext=ext)
    return "{username}/posts/image/{imageName}".format(username=instance, imageName=imageName)


class Post(models.Model):
    user = models.ForeignKey(User, related_name="post",
                             on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    image = models.ImageField(upload_to=image_upload, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('feed:postDetails', kwargs={"id": self.id})
