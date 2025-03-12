from django.db import models

# Create your models here.

class PageView(models.Model):
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.count)
    
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(max_length=1024, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_count = models.IntegerField(default=0)  # New field to store order count

    def __str__(self):
        return self.name



# class OrderCount(models.Model):
#     count = models.IntegerField(default=0)
#     last_updated = models.DateTimeField(auto_now=True)