from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.validators import MinLengthValidator

# Create your models here.

class Author(models.Model):

    def __str__(self):
        return self.display_name or str(self.user)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    display_name = models.CharField(max_length=32, null=True, unique=True, blank=True, validators=[MinLengthValidator(3, 'Your name must be least 3 characters')])
    slug = models.SlugField(null=True, unique=True)
    about_me = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='addme',default='default.png')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        return super().save(*args, **kwargs)