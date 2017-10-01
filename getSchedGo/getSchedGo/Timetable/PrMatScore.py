"""
making a proirity matrix so that event has a time and a activity type with it and we return a score.

Let me have two matrix
"""
# eventDict = {'Official Classes':0, 'Study Acads':1, 'Extra Study':2, 'ExtraCurriculars':3,'Misc.':4 }
eventDict = {'A':0, 'B':1, 'C':2, 'D':3,'E':4 }

# Priorityarray = [[4,2],[3,5]]
#let only two slot and matrix is like ----
# There are 288 slot let's convert it to 48
PriorityMat=[[500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500 , 500],[45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 40 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50 , 50],[43 , 43 , 43 , 43 , 43 , 43 , 43 , 43 , 43 , 43 , 43 , 43 , 43 , 43 , 43 , 43 , 43 , 43 , 43 , 43 , 43 , 43 , 43 , 43 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 37 , 23 , 23 , 23 , 23 , 23 , 23 , 23 , 23 , 23 , 23 , 23 , 23 , 23 , 23 , 23 , 23 , 23 , 23 , 23 , 23 , 23 , 23 , 23 , 23 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 38 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 19 , 19 , 19 , 19 , 19 , 19 , 19 , 19 , 19 , 19 , 19 , 19 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45 , 45],[20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 12 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 33 , 17 , 17 , 17 , 17 , 17 , 17 , 17 , 17 , 17 , 17 , 17 , 17 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11 , 11],[15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 30 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 25 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 35 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 15]]
def scoreCalc(eventType,slotNumber):
	eventindex = eventDict[eventType]
	score = PriorityMat[eventindex][slotNumber]
	return score