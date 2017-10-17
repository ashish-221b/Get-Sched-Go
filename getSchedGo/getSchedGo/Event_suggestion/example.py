
import http.client ## 
import requests
import json
import re
from .models import suggestion
from profiles.models import profile

## Method for scheduling match
# @param userprofile
# @details It extracts the list of football matches from the API endpoint
# football-data.org/fixtures for the upcoming week.It then filters the matches 
# to get the matches for famous clubs like FC Barcelona, Real Madrid etc.Then it
# create an instance of suggestion model out of each of these matches and save them 
# to the database.
def matcheschedule(userprofile):
	dict= {}
	list= ['FC Barcelona', 'Real Madrid CF', 'Manchester City FC', 'Manchester United FC',
	'Chelsea FC', 'Paris Saint-Germain', 'Juventus Turin','Club Atlético de Madrid','Liverpool FC','FC Bayern München']
	connection = http.client.HTTPConnection('api.football-data.org')
	headers = { 'X-Auth-Token': 'bcfa111e2227403a9491066e8a033df4', 'X-Response-Control': 'minified' }
	connection.request('GET', '/v1/competitions', None, headers )
	response = json.loads(connection.getresponse().read().decode())
	for match in response:
		dict[match['id']]= match['caption']

	print(dict)
	# list =["1. Bundesliga 2017/18", "Premier League 2017/18", "Serie A 2017/18"]


	connection1 = http.client.HTTPConnection('api.football-data.org')
	headers1 = { 'X-Auth-Token': 'bcfa111e2227403a9491066e8a033df4', 'X-Response-Control': 'minified' }
	connection1.request('GET', '/v1/fixtures', None, headers1 )
	response1 = json.loads(connection1.getresponse().read().decode())
	fixture= response1['fixtures']
	suggestion.objects.all().delete()
	for match in fixture:
		if str(match['homeTeamName']) in list or str(match['awayTeamName']) in list:
			s= match['date']
			q= suggestion(UserProfile=userprofile,StartDate=s[0:10],StartTime=s[11:17],Hometeam=match['homeTeamName'],Awayteam=match['awayTeamName'],League=dict[match['competitionId']])
		
			q.save()
		





	
# fixtures= response['fixtures']

# # for match in fixtures:
# # 	if match['homeTeamName'] in list:
# # 		print( match['hometeamName'] ,match['date'])
# # 	elif match['awayTeamName'] in list:
# # 		print(match['awayTeamName'],match['date'])




# for match in fixtures:
	
# 	print(match['date'],match['homeTeamName'],"\t",match['awayTeamName'])