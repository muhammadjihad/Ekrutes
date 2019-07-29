from django.contrib import admin
from .models import (
    AccountProfile,
    AccountStatus
)

admin.site.register(AccountProfile)
admin.site.register(AccountStatus)
# Register your models here.
