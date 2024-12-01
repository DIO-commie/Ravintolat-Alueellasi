from django.contrib import admin

# Register your models here.
# ravintolat/admin.py
from django.contrib import admin
from .models import Ravintola, Arvostelu, Profiili

admin.site.register(Ravintola)
admin.site.register(Arvostelu)
admin.site.register(Profiili)
