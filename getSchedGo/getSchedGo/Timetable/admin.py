from django.contrib import admin

#Register your models here.
from .models import *

class DailySchedAdmin(admin.ModelAdmin):
	class Meta:
		model = DailySched
class SlotsAdmin(admin.ModelAdmin):
	class Meta:
		model = Slots
class EventAdmin(admin.ModelAdmin):
	class Meta:
		model = Event
class InstructorAssignmentAdmin(admin.ModelAdmin):
	class Meta:
		model = InstructorAssignment
class InstructorClassAdmin(admin.ModelAdmin):
	class Meta:
		model = InstructorClass
class InstructorExamAdmin(admin.ModelAdmin):
	class Meta:
		model = InstructorExam

admin.site.register(Slots,SlotsAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(DailySched,DailySchedAdmin)
admin.site.register(InstructorExam,InstructorExamAdmin)
admin.site.register(InstructorClass,InstructorClassAdmin)
admin.site.register(InstructorAssignment,InstructorAssignmentAdmin)
