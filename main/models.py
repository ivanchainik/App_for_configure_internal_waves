from django.db import models


class Document(models.Model):
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True, )


class Value(models.Model):
    font_size = models.IntegerField()
    cutoff_freq = models.FloatField()
    decay_level = models.IntegerField()
