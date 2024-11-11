from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class gallery(models.Model):
    image = models.ImageField()

class ClientProfile(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254, unique=True)
    face_id = models.TextField(blank=True, null=True) 
    password = models.CharField(max_length=128) 
    last_login = models.DateField()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def update_face_id(self, face_id):
        self.face_id = face_id
        super().save(update_fields=['face_id'])

    def save(self, *args, **kwargs):
        try:
            validate_password(self.password)
        except ValidationError as e:
            raise ValidationError({"password": e.messages})

        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'tb_client'