from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Produto(models.Model):
    sku = models.CharField(max_length=20)
    descricao = models.CharField(max_length=200)
    url = models.URLField()
    habilitado = models.CharField(max_length=3)
    buybox = models.CharField(max_length=3)
    menorpreco = models.CharField(max_length=50)
    loja = models.CharField(max_length=50)
    site = models.CharField(max_length=50)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.sku