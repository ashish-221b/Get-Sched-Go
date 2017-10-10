from django.contrib import admin

# Register your models here.
from .models import dailyStats

# Your dailyStats get registered with the admin and can be viewed in admin page
class dailyStatsAdmin(admin.ModelAdmin):
	class Meta:
		model = dailyStats

admin.site.register(dailyStats,dailyStatsAdmin)