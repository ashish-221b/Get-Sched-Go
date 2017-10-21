from django.contrib import admin

# Register your models here.
from .models import profile,FeedBack

## Your profile get registered with the admin and can be viewed in admin page
class profileAdmin(admin.ModelAdmin):
	class Meta:
		model = profile
class FeedBackAdmin(admin.ModelAdmin):
	class Meta:
		model = FeedBack
admin.site.register(profile,profileAdmin)
admin.site.register(FeedBack,FeedBackAdmin)