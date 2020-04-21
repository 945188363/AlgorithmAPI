from django.db import models

# Create your models here.


class jokes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    content = models.TextField()
    createTime = models.DateTimeField(auto_now=True)
    updateTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'jokes'
        ordering = ['id']