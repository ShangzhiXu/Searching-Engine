from django.db import models

class News(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=10000)


class word(models.Model):
    text = models.CharField(max_length=3, primary_key=True)



