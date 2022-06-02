
from io import BytesIO
from PIL import Image
from django.db import models
from django.core.files import File
from django.contrib.auth.models import User
from django.utils.text import slugify
from numpy import product

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True)
    slug = models.SlugField(max_length=200,blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'
    
    def save(self, *args, **kwargs):
       self.slug=slugify(self.name)
       super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.CharField(max_length=200)
    time_added=models.DateTimeField(auto_now_add=True)
    items_in_stock=models.IntegerField(default=1)
    class Meta:
        ordering=("name",)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

        
    def save(self, *args, **kwargs):
       self.slug=slugify(self.name)
       super(Product, self).save(*args, **kwargs) # Call the real save() method

class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    image = models.ImageField(upload_to="productimages/", blank=True, null=True)
    thumbnail=models.ImageField(upload_to="productimages/",blank=True,null=True)

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000'+ self.image.url
        return ""
    def get_thumbnail(self):
        if self.thumbnail:
            return "http://127.0.0.1:8000"  + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail=self.make_thumbnail(self.image)
                self.save()
                return "http://127.0.0.1:8000"  + self.thumbnail.url
            else:
                return ""
    
    def make_thumbnail(self,image,size=[300,200]):
        img=Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io=BytesIO()
        img.save(thumb_io,'JPEG',quality=75)

        thumbnail=File(thumb_io,name=image.name)

        return thumbnail
    def save(self, *args, **kwargs):
       self.thumbnail=self.make_thumbnail(self.image)
       super(ProductImage, self).save(*args, **kwargs) # Call the real save() method