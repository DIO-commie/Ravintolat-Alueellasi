from django.db import models

# Create your models here.
# ravintolat/models.py
from django.db import models
from django.contrib.auth.models import User

class Ravintola(models.Model):
    nimi = models.CharField(max_length=100)
    osoite = models.CharField(max_length=200)
    puhelin = models.CharField(max_length=20, blank=True)
    hinta_taso = models.IntegerField(help_text="Hinta-taso (1-5)")
    korkea_taso = models.BooleanField(default=False)
    # Lisää tarvittavat kentät

    def __str__(self):
        return self.nimi

class Arvostelu(models.Model):
    ravintola = models.ForeignKey(Ravintola, related_name='arvostelut', on_delete=models.CASCADE)
    kayttaja = models.ForeignKey(User, on_delete=models.CASCADE)
    tähdet = models.IntegerField()
    kommentti = models.TextField(blank=True)
    luotu = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.kayttaja.username} - {self.ravintola.nimi} - {self.tähdet} tähteä"

class Profiili(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    suosikit = models.ManyToManyField(Ravintola, related_name='suosikit')
    # Voit lisätä listoja eri tarpeisiin

    def __str__(self):
        return f"{self.user.username} profiili"
