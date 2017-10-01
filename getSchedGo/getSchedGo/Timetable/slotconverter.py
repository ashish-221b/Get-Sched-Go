def timeToSlot(time):
	hour=int(time[0:2])
	minute = int(time[3:5])//5
	slot = hour*12 + minute + 1
	return slot

def slotToTime(slot):
	return ""