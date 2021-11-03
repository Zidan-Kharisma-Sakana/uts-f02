from django.contrib import admin

# Register your models here.
from .models import DM, Pesan
admin.site.register(Pesan)
admin.site.register(DM)