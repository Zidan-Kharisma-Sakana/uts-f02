
from django.contrib import admin
from . import models
# TODO Register Friend model here
admin.site.register(models.Profile)
admin.site.register(models.UserStatus)
admin.site.register(models.Invitation)