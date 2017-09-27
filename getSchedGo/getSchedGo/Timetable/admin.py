from django.contrib import admin

#Register your models here.
from .models import DailySched, Event, Slots

class DailySchedAdmin(admin.ModelAdmin):
	class Meta:
		model = DailySched
class SlotsAdmin(admin.ModelAdmin):
	class Meta:
		model = Slots
class EventAdmin(admin.ModelAdmin):
	class Meta:
		model = Event
admin.site.register(Slots,SlotsAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(DailySched,DailySchedAdmin)
