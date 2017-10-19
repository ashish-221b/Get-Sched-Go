from .models import *
import collections
def getDuration(Type,Id):
    targetEvents = Event.objects.filter(CreatorType=Type,CreatorId=Id)
    DurationData = []
    for eve in targetEvents:
        DurationData.extend(eve.Duration)
    counter = collections.Counter(DurationData)
    sums = 0
    for d in DurationData:
        sums = sums + int(d)
    mean = round((sums/float(len(DurationData))),2)
    return (DurationData,counter,mean)
