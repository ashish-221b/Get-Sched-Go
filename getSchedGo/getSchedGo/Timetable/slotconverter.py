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
def slotInterval(A):
	s1,s2,d=A
	s1=int(s1)
	s2=int(s2)
	k = (s1-1)%2
	k1 = (s2-1)%2
	mins = str((k)*30)
	hour = str((s1-1)//2)
	mins_e = str(((k1+1)%2)*30)
	hour_e = str((s2//2)%24)
	return (d,hour+":"+mins+":"+"00",hour_e+":"+mins_e+":"+"00")
