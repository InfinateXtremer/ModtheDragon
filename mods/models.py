from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from django.core.validators import MinLengthValidator, FileExtensionValidator
from mptt.models import MPTTModel, TreeForeignKey

from datetime import datetime, timezone
from io import BytesIO
from PIL import Image

from users.models import *

# Create your models here.

def limit_image(image_field, maximum_size = 512, discard_alpha = True):
    filename = "%s.webp" % '.'.join(image_field.name.split('.')[:-1])

    image = Image.open(image_field)

    scale = 1
    scale = min(scale, maximum_size / image.width)
    scale = min(scale, maximum_size / image.height)
    scaled_size = tuple([int(x * scale) for x in image.size])
    
    if discard_alpha and image.mode in ('RGBA', 'LA'):
        alpha_replace = Image.new(image.mode[:-1], scaled_size, '#000')
        alpha_replace.paste(image, (0, 0, scaled_size[0], scaled_size[1]), image.split()[-1])
        image = alpha_replace
    elif scale < 1:
        image = image.resize(scaled_size)
    
    image_io = BytesIO()
    image.save(image_io, format='WEBP', save_all=True)

    image_field.save(filename, ContentFile(image_io.getvalue()), save=False)

def get_game_path(game):
    return "%s/" % (game.slug)

def get_game_icon_path(game, filename):
    return get_game_path(game) + "icon/%s" % (filename)

class Game(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    icon = models.ImageField(null=True, blank=True, upload_to=get_game_icon_path)
    slug = models.SlugField(null=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

def get_game_background_path(background, filename):
    return get_game_path(background.game) + "background/%s" % (filename)

class GameBackground(models.Model):
    
    def __str__(self):
        return self.background.url
    
    game = models.ForeignKey(Game, on_delete = models.CASCADE)
    background = models.ImageField(upload_to=get_game_background_path)
    artist = models.CharField(max_length=30, blank=False, null=False)

    def save(self, *args, **kwargs):
        if self.background:
            limit_image(self.background, 1920)

        super().save(*args, **kwargs)

class Tag(MPTTModel):

    def __str__(self):
        return self.name

    name = models.CharField(max_length = 32, unique = True)
    parent = TreeForeignKey('self', on_delete = models.CASCADE, null=True, blank=True, related_name='children')
    admin = models.BooleanField(default = False)
    
    class MPTTMeta:
        order_insertion_by = ['name']
    


def get_mod_path(instance, filename):
    return get_game_path(instance.game) + "mod/%s/%s/%s" % (instance.author.user.username, instance.slug, filename)

class Mod(models.Model):
    
    def __str__(self):
        return self.title
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    slug = models.SlugField(null=True, unique=True)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, null=False, editable=False)
    description = models.TextField(null=False, blank=True)
    version = models.CharField(max_length=8, validators=[MinLengthValidator(1, 'Please add version information.')])
    featured = models.BooleanField(default = False)
    tags = models.ManyToManyField(Tag)
    hidden = models.BooleanField(default = False)
    downloads = models.PositiveBigIntegerField(default = 0, editable = False)
    thumbnail = models.ImageField(upload_to = get_mod_path)
    dependencies = models.ManyToManyField('self',symmetrical=False,blank=True)
    file = models.FileField(upload_to=get_mod_path, unique=True, validators=[FileExtensionValidator(allowed_extensions=['zip', 'pak'])])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        if self.thumbnail:
            limit_image(self.thumbnail, 512, False)

        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("view_mod", kwargs={'game_slug': self.game.slug, "id_slug": self.slug or self.id, "author_name": self.author.slug})
    
    def get_if_updated_after_week(self):
        timedelta = self.date_updated - datetime.now(timezone.utc)
        return timedelta.days < -7


class ModPack(models.Model):
    
    def __str__(self):
        return self.title
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.TextField()
    mods = models.ManyToManyField(Mod)

