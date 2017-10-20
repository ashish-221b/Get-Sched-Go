from django.contrib import admin

# Register your models here.
from .models import coursedetail
## registers coursedetail model to be changed by admin in case of errors
class courseAdmin(admin.ModelAdmin):
	class Meta:
		model = coursedetail

admin.site.register(coursedetail,courseAdmin)