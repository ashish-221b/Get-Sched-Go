from django.contrib import admin

# Register your models here.
from .models import dailyStats

## dailyStats get registered with the admin and can be viewed in admin page and used to do editing if necessary
# mainly helpful in development phase. Will be removed during beta release
class dailyStatsAdmin(admin.ModelAdmin):
	class Meta:
		model = dailyStats

admin.site.register(dailyStats,dailyStatsAdmin)