from django.contrib import admin

# Register your models here.
from .models import profile

## Your profile get registered with the admin and can be viewed in admin page
class profileAdmin(admin.ModelAdmin):
	class Meta:
		model = profile

admin.site.register(profile,profileAdmin)
