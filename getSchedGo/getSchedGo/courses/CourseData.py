import csv
import collections
from .models import coursedetail
## Method for extracting Course Details from .csv provided by asc
# @details It traverses over whole csv file using csv package of python.
# Extracts all the slots relating to a particular course and stores them in coursedetail model
# hereby generating a list of all courses running in the institute and saving them in the database 
# To stop discrepancy only first course is taken in case of multiple names
def UpdateCourse():
    ## List of all official slots in institute
    LookupTable = ['1A','1B','1C','2A','2B','2C','3A','3B','3C','4A','4B','4C',
    '5A', '5B', '6A', '6B', '7A', '7B', '8A', '8B', '9A', '9B', '10A', '10B',
     '11A', '11B', '12A', '12B', '13A', '13B', '14A', '14B', '15A', '15B',
     'X1','X2','X3','XC','XD','L1','L2','L3','L4','LX']
    ## List of slots that clash in iitb academic time-table
    ClashList = [(0,24),(1,25),(3,26),(4,27),(6,28),(7,29),(9,30),(10,31),(12,32),(13,33)]
    with open('data.csv') as courseFile:
        reader = csv.DictReader(courseFile)
        uni = collections.OrderedDict()
        for row in reader:
            if(row['Data']!=""):
                result = map(lambda s1: row['Data'].count(s1), LookupTable)
                result = list(result)
                for a,b in ClashList:
                    result[a]=result[a]-result[b]
                i=0
                slot = []
                for x in result:
                    if x > 0:
                        slot.append(LookupTable[i])
                    i=i+1
                if slot:
                    if row['Course Code'] not in uni:
                        uni[row['Course Code']] = slot
        coursedetail.objects.all().delete()
        for i in uni:
            st = ''
            for j in uni[i]:
                st = st + j + ' '
            q = coursedetail(code=i,name=i,Slot = st)
            q.save()
