from django.db import models

class UserProfile(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    face_image_base64 = models.TextField(blank=True, null=True) 

class TempImage(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image_path = models.FilePathField(path=f'/path/to/user/data/', match=".*\.(jpg|jpeg|png)$")

class gallery(models.Model):
    image = models.ImageField()

class tb_client(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.TextField()
    face_id = models.BinaryField()