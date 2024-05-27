from django.db import models

# Create your models here.

class PageView(models.Model):
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.count)