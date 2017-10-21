## Converts a time to a slot
# @param Time a time object
# @details Converts a time object into the slotnumber of the slot containing the time.
def timeToSlot(time):
	if time is None:
		return 0
	else:
		hour=int(time[0:2])
		minute = int(time[3:5])//30
		slot = hour*2 + minute + 1
		return slot

def slotToTime(slot):
	return ""
