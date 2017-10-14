from django.contrib import admin

# Register your models here.
from .models import coursedetail

class courseAdmin(admin.ModelAdmin):
	class Meta:
		model = coursedetail

admin.site.register(coursedetail,courseAdmin)