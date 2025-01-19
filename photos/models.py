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
    accept_terms = models.BooleanField(default=False)

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
        managed = False

# Model for tb_colors
class Color(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
            return self.name 
    class Meta:
        db_table = 'tb_colors'
        managed = False

# Model for tb_gender
class Gender(models.Model):
    id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
            return self.gender 
    class Meta:
        db_table = 'tb_gender'
        managed = False

# Model for tb_productcategories
class ProductCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
            return self.name 
    class Meta:
        db_table = 'tb_productcategories'
        managed = False

# Model for tb_productsubcategories
class ProductSubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey(
        ProductCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="subcategories",
        db_column="id_category"
    )

    def __str__(self):
            return self.name 

    class Meta:
        db_table = 'tb_productsubcategories'
        managed = False

# Model for tb_articletype
class ArticleType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    subcategory = models.ForeignKey(
        ProductSubCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="article_types",
        db_column="id_subcategory"
    )

    def __str__(self):
            return self.name 

    class Meta:
        db_table = 'tb_articletype'
        managed = False

# Model for tb_seasons
class Season(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
            return self.name 

    class Meta:
        db_table = 'tb_seasons'
        managed = False

# Model for tb_usagetype
class UsageType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
            return self.name 

    class Meta:
        db_table = 'tb_usagetype'
        managed = False

# Model for tb_imageproduct
class ImageProduct(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.CharField(max_length=255, blank=True, null=True)
    usage_type = models.ForeignKey(
        UsageType, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="image_products_by_usage_type",
        db_column="id_usagetype"
    )
    gender = models.ForeignKey(
        Gender, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="image_products_by_gender",
        db_column="id_gender"
    )
    season = models.ForeignKey(
        Season, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="image_products_by_season",
        db_column="id_season"
    )
    color = models.ForeignKey(
        Color, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="image_products_by_color",
        db_column="id_color"
    )
    article_type = models.ForeignKey(
        ArticleType, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="image_products_by_article_type",
        db_column="id_articletype"
    )
    client = models.ForeignKey(
        ClientProfile, 
        on_delete=models.CASCADE, 
        related_name="image_products_by_client",
        db_column="id_client"
    )

    class Meta:
        db_table = 'tb_imageproduct'
        managed = False
