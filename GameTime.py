# -*- coding: cp1252 -*-

## --------------------------------------------------------------------------------------
## Import Modules
## --------------------------------------------------------------------------------------
from datetime import datetime
import time
import os
from bs4 import BeautifulSoup
import urllib2
## http://home.wlu.edu/~lambertk/breezypythongui/

debug = 0

## ----------------------------------------------------------------------------
## Global Constants
## ----------------------------------------------------------------------------
CheckBaseURL = "https://dl.dropboxusercontent.com/u/5739973/NHL/Builds/"
CheckVerURL = "checkverpy.txt"

TeamLineUpBaseURL = "http://www2.dailyfaceoff.com/teams/lines/"


TeamStatCount = 25
TeamStats = ["Rank","GP","W","L","OT","P","ROW","HROW","RROW","P%","G/G",
	"GA/G","5-5 F/A","PP%","PK%","S/G","SA/G","Sc 1%","Tr 1st%","Ld 1%",
	"Ld 2%","OS%","OSB%","FO%"]

PlayerStatCount = 14
PlayerStats = ["Num", "Pos", "Name", "GP", "G", "A", "P", "+/-", "PIM",
	"PP", "SH", "GW", "S", "S%"]

GoalieStatCount = 16
GoalieStats = ["Num", "Name", "GPI", "GS", "Min", "GAA", "W", "L", "OT", "SO",
	"SA", "GA", "SV%", "G", "A", "PIM"]

SpecialFields = ["nameabbr", "redditname", "redditicon", "redditabbr"]

TableHeader = [":--:", ":--:", ":--:", ":--:", ":--:", ":--:", ":--:", ":--:",
	":--:", ":--:", ":--:", ":--:", ":--:", ":--:", ":--:", ":--:", ":--:",
	":--:", ":--:", ":--:", ":--:", ":--:", ":--:"]

InjuryURL = "http://www.tsn.ca/nhl/injuries/"
InjuryFields = [ "Player", "Date", "Status", "Injury" ]

"""
TeamNames = ["Penguins", "Devils", "Rangers", "Islanders", "Flyers",
	"Blackhawks", "RedWings", "Blues", "BlueJackets", "Predators", "Canadiens",
	"Bruins", "Senators", "MapleLeafs", "Sabres", "Canucks", "Wild", "Oilers",
	"Flames", "Avalanche", "Ducks", "Kings", "Stars", "Sharks", "Coyotes", "Jets",
	"Hurricanes", "Capitals", "Lightning", "Panthers"]
TeamCities = [u"Pittsburgh", u"New Jersey", u"NY Rangers", u"NY Islanders",
	u"Philadelphia", u"Chicago", u"Detroit", u"St. Louis", u"Columbus",
	u"Nashville", u"Montréal", u"Boston", u"Ottawa", u"Toronto", u"Buffalo",
	u"Vancouver", u"Minnesota", u"Edmonton", u"Calgary", u"Colorado",
	u"Anaheim", u"Los Angeles", u"Dallas", u"San Jose", u"Arizona",
	u"Winnipeg", u"Carolina", u"Washington", u"Tampa Bay", u"Florida"]
TeamLong = ["Pittsburgh Penguins", "New Jersey Devils", "New York Rangers",
	"New York Islanders", "Philadelphia Flyers", "Chicago Blackhawks",
	"Detroit Red Wings", "St. Louis Blues", "Columbus Blue Jackets",
	"Nashville Predators", "Montreal Canadiens", "Boston Bruins",
	"Ottawa Senators", "Toronto Maple Leafs", "Buffalo Sabres",
	"Vancouver Canucks", "Minnesota Wild", "Edmonton Oilers",
	"Calgary Flames", "Colorado Avalanche", "Anaheim Ducks",
	"Los Angeles Kings", "Dallas Stars", "San Jose Sharks", "Arizona Coyotes",
	"Winnipeg Jets", "Carolina Hurricanes", "Washington Capitals",
	"Tampa Bay Lightning", "Florida Panthers"]
TeamNamesAbbr = ["PIT", "NJD", "NYR", "NYI", "PHI", "CHI", "DET", "STL",
	"CBJ", "NSH", "MTL", "BOS", "OTT", "TOR", "BUF", "VAN", "MIN", "EDM", "CGY",
	"COL", "ANA", "LAK", "DAL", "SJS", "ARI", "WPG", "CAR", "WSH", "TBL", "FLA"]
TeamReddits = ["/r/penguins", "/r/devils", "/r/rangers", "/r/newyorkislanders",
	"/r/flyers", "/r/hawks", "/r/detroitredwings", "/r/stlouisblues",
	"/r/bluejackets", "/r/predators", "/r/habs", "/r/bostonbruins",
	"/r/ottawasenators", "/r/leafs", "/r/sabres", "/r/canucks",
	"/r/wildhockey", "/r/edmontonoilers", "/r/calgaryflames",
	"/r/coloradoavalanche", "/r/anaheimducks", "/r/losangeleskings",
	"/r/dallasstars", "/r/sanjosesharks", "/r/coyotes", "/r/winnipegjets",
	"/r/canes", "/r/caps", "/r/tampabaylightning", "/r/floridapanthers"]
TeamArenas = ["Consol Energy Center", "Prudential Center",
	"Madison Square Garden", "Nassau Veterans Memorial Coliseum",
	"Wells Fargo Center", "United Center", "Joe Louis Arena",
	"Scottrade Center", "Nationwide Arena", "Bridgestone Arena", "Bell Centre",
	"TD Garden", "Canadian Tire Centre", "Air Canada Centre",
	"First Niagara Center", "Rogers Arena", "Xcel Energy Center",
	"Rexall Place", "Scotiabank Saddledome", "Pepsi Center", "Honda Center",
	"Staples Center", "American Airlines Center", "SAP Center",
	"Gila River Arena", "MTS Centre", "PNC Arena", "Verizon Center",
	"Amalie Arena", "BB&T Center"]
TeamArenaPlace = ["Pittsburgh, PA, USA", "Newark, NJ, USA",
	"New York, NY, USA", "Long Island, NY, USA", "Philadelphia, PA, USA",
	"Chicago, IL, USA", "Detroit, MI, USA", "St Louis, MO, USA",
	"Columbus, OH, USA", "Nashville, TN, USA", "Montreal, QC, CAN",
	"Boston, MA, USA", "Ottawa, ON, CAN", "Toronto, ON, CAN",
	"Buffalo, NY, USA", "Vancouver, BC, CAN", "St Paul, MN, USA",
	"Edmonton, AB, CAN", "Calgary, AB, CAN", "Denver, CO, USA",
	"Anaheim, CA, USA", "Los Angeles, CA, USA", "Dallas, TX, USA",
	"San Jose, CA, USA", "Glendale, AZ, USA", "Winnipeg, MB, CAN",
	"Raleigh, NC, USA", "Washington, DC, USA", "Tampa, FL, USA",
	"Sunrise, FL, USA"]
TeamTimeZone = ["ET", "ET", "ET", "ET", "ET", "CT", "ET", "CT", "ET", "CT",
	"ET", "ET", "ET", "ET", "ET", "PT", "CT", "MT", "MT", "MT", "PT", "PT",
	"CT", "PT", "MT", "CT", "ET", "ET", "ET", "ET"]
TeamNHL = ["Pittsburgh", "New Jersey", "NY Rangers", "NY Islanders",
	"Philadelphia", "Chicago", "Detroit", "St Louis", "Columbus", "Nashville",
	"Montreal", "Boston", "Ottawa", "Toronto", "Buffalo", "Vancouver",
	"Minnesota", "Edmonton", "Calgary", "Colorado", "Anaheim", "Los Angeles",
	"Dallas", "San Jose", "Arizona", "Winnipeg", "Carolina", "Washington",
	"Tampa Bay", "Florida"]
TeamTSN = ["Pittsburgh", "New Jersey", "NY Rangers", "NY Islanders",
	"Philadelphia", "Chicago", "Detroit", "St. Louis", "Columbus", "Nashville",
	"Montreal", "Boston", "Ottawa", "Toronto", "Buffalo", "Vancouver",
	"Minnesota", "Edmonton", "Calgary", "Colorado", "Anaheim", "Los Angeles",
	"Dallas", "San Jose", "Arizona", "Winnipeg", "Carolina", "Washington",
	"Tampa Bay", "Florida"]
"""

	
team_dicts = {
	'Avalanche': {
		'Abbr': 'COL',
        'Arena': 'Pepsi Center',
        'ArenaPlace': 'Denver, CO, USA',
        'City': u'Colorado',
		'LineupURL': "20/colorado-avalanche",
        'Long': 'Colorado Avalanche',
        'NHL': 'Colorado',
        'Name': 'Avalanche',
        'Subreddit': '/r/coloradoavalanche',
        'TSN': 'Colorado',
        'TimeZone': 'MT'},
	'Blackhawks': {
		'Abbr': 'CHI',
        'Arena': 'United Center',
        'ArenaPlace': 'Chicago, IL, USA',
        'City': u'Chicago',
		'LineupURL': "19/chicago-blackhawks",
        'Long': 'Chicago Blackhawks',
        'NHL': 'Chicago',
        'Name': 'Blackhawks',
        'Subreddit': '/r/hawks',
        'TSN': 'Chicago',
        'TimeZone': 'CT'},
	'BlueJackets': {
		'Abbr': 'CBJ',
        'Arena': 'Nationwide Arena',
        'ArenaPlace': 'Columbus, OH, USA',
        'City': u'Columbus',
		'LineupURL': "21/columbus-blue-jackets",
        'Long': 'Columbus Blue Jackets',
        'NHL': 'Columbus',
        'Name': 'BlueJackets',
        'Subreddit': '/r/bluejackets',
        'TSN': 'Columbus',
        'TimeZone': 'ET'},
	'Blues': {
		'Abbr': 'STL',
        'Arena': 'Scottrade Center',
        'ArenaPlace': 'St Louis, MO, USA',
        'City': u'St. Louis',
		'LineupURL' : "38/st-louis-blues",
        'Long': 'St. Louis Blues',
        'NHL': 'St Louis',
        'Name': 'Blues',
        'Subreddit': '/r/stlouisblues',
        'TSN': 'St. Louis',
        'TimeZone': 'CT'},
	'Bruins': {
		'Abbr': 'BOS',
        'Arena': 'TD Garden',
        'ArenaPlace': 'Boston, MA, USA',
        'City': u'Boston',
		'LineupURL': "15/boston-bruins/",
        'Long': 'Boston Bruins',
        'NHL': 'Boston',
        'Name': 'Bruins',
        'Subreddit': '/r/bostonbruins',
        'TSN': 'Boston',
        'TimeZone': 'ET'},
	'Canadiens': {
		'Abbr': 'MTL',
        'Arena': 'Bell Centre',
        'ArenaPlace': 'Montreal, QC, CAN',
        'City': u'Montr\xc3\xa9al',
		'LineupURL': "28/montreal-canadiens",
        'Long': 'Montreal Canadiens',
        'NHL': 'Montreal',
        'Name': 'Canadiens',
        'Subreddit': '/r/habs',
        'TSN': 'Montreal',
        'TimeZone': 'ET'},
	'Canucks': {
		'Abbr': 'VAN',
        'Arena': 'Rogers Arena',
        'ArenaPlace': 'Vancouver, BC, CAN',
        'City': u'Vancouver',
		'LineupURL': "41/vancouver-canucks",
        'Long': 'Vancouver Canucks',
        'NHL': 'Vancouver',
        'Name': 'Canucks',
        'Subreddit': '/r/canucks',
        'TSN': 'Vancouver',
        'TimeZone': 'PT'},
	'Capitals': {
		'Abbr': 'WSH',
        'Arena': 'Verizon Center',
        'ArenaPlace': 'Washington, DC, USA',
        'City': u'Washington',
		'LineupURL': "42/washington-capitals",
        'Long': 'Washington Capitals',
        'NHL': 'Washington',
        'Name': 'Capitals',
        'Subreddit': '/r/caps',
        'TSN': 'Washington',
        'TimeZone': 'ET'},
	'Coyotes': {
		'Abbr': 'ARI',
        'Arena': 'Gila River Arena',
        'ArenaPlace': 'Glendale, AZ, USA',
        'City': u'Arizona',
		'LineupURL': "35/arizona-coyotes",
        'Long': 'Arizona Coyotes',
        'NHL': 'Arizona',
        'Name': 'Coyotes',
        'Subreddit': '/r/coyotes',
        'TSN': 'Arizona',
        'TimeZone': 'MT'},
	'Devils': {
		'Abbr': 'NJD',
        'Arena': 'Prudential Center',
        'ArenaPlace': 'Newark, NJ, USA',
        'City': u'New Jersey',
		'LineupURL' : "30/new-jersey-devils",
        'Long': 'New Jersey Devils',
        'NHL': 'New Jersey',
        'Name': 'Devils',
        'Subreddit': '/r/devils',
        'TSN': 'New Jersey',
        'TimeZone': 'ET'},
	'Ducks': {
		'Abbr': 'ANA',
        'Arena': 'Honda Center',
        'ArenaPlace': 'Anaheim, CA, USA',
        'City': u'Anaheim',
		'LineupURL': "13/anaheim-ducks/",
        'Long': 'Anaheim Ducks',
        'NHL': 'Anaheim',
        'Name': 'Ducks',
        'Subreddit': '/r/anaheimducks',
        'TSN': 'Anaheim',
        'TimeZone': 'PT'},
	'Flames': {
		'Abbr': 'CGY',
        'Arena': 'Scotiabank Saddledome',
        'ArenaPlace': 'Calgary, AB, CAN',
        'City': u'Calgary',
		'LineupURL': "17/calgary-flames",
        'Long': 'Calgary Flames',
        'NHL': 'Calgary',
        'Name': 'Flames',
        'Subreddit': '/r/calgaryflames',
        'TSN': 'Calgary',
        'TimeZone': 'MT'},
	'Flyers': {
		'Abbr': 'PHI',
        'Arena': 'Wells Fargo Center',
        'ArenaPlace': 'Philadelphia, PA, USA',
        'City': u'Philadelphia',
		'LineupURL': "34/philadelphia-flyers",
        'Long': 'Philadelphia Flyers',
        'NHL': 'Philadelphia',
        'Name': 'Flyers',
        'Subreddit': '/r/flyers',
        'TSN': 'Philadelphia',
        'TimeZone': 'ET'},
	'Hurricanes': {
		'Abbr': 'CAR',
        'Arena': 'PNC Arena',
        'ArenaPlace': 'Raleigh, NC, USA',
        'City': u'Carolina',
		'LineupURL': "18/carolina-hurricanes",
        'Long': 'Carolina Hurricanes',
        'NHL': 'Carolina',
        'Name': 'Hurricanes',
        'Subreddit': '/r/canes',
        'TSN': 'Carolina',
        'TimeZone': 'ET'},
	'Islanders': {
		'Abbr': 'NYI',
        'Arena': 'Nassau Veterans Memorial Coliseum',
        'ArenaPlace': 'Long Island, NY, USA',
        'City': u'NY Islanders',
		'LineupURL': "31/new-york-islanders",
        'Long': 'New York Islanders',
        'NHL': 'NY Islanders',
        'Name': 'Islanders',
        'Subreddit': '/r/newyorkislanders',
        'TSN': 'NY Islanders',
        'TimeZone': 'ET'},
	'Jets': {
		'Abbr': 'WPG',
        'Arena': 'MTS Centre',
        'ArenaPlace': 'Winnipeg, MB, CAN',
        'City': u'Winnipeg',
		'LineupURL': "14/winnipeg-jets",
        'Long': 'Winnipeg Jets',
        'NHL': 'Winnipeg',
        'Name': 'Jets',
        'Subreddit': '/r/winnipegjets',
        'TSN': 'Winnipeg',
        'TimeZone': 'CT'},
	'Kings': {
		'Abbr': 'LAK',
        'Arena': 'Staples Center',
        'ArenaPlace': 'Los Angeles, CA, USA',
        'City': u'Los Angeles',
		'LineupURL': "26/los-angeles-kings",
        'Long': 'Los Angeles Kings',
        'NHL': 'Los Angeles',
        'Name': 'Kings',
        'Subreddit': '/r/losangeleskings',
        'TSN': 'Los Angeles',
        'TimeZone': 'PT'},
	'Lightning': {
		'Abbr': 'TBL',
        'Arena': 'Amalie Arena',
        'ArenaPlace': 'Tampa, FL, USA',
        'City': u'Tampa Bay',
		'LineupURL': "39/tampa-bay-lightning",
        'Long': 'Tampa Bay Lightning',
        'NHL': 'Tampa Bay',
        'Name': 'Lightning',
        'Subreddit': '/r/tampabaylightning',
        'TSN': 'Tampa Bay',
        'TimeZone': 'ET'},
	'MapleLeafs': {
		'Abbr': 'TOR',
        'Arena': 'Air Canada Centre',
        'ArenaPlace': 'Toronto, ON, CAN',
        'City': u'Toronto',
		'LineupURL': "40/toronto-maple-leafs",
        'Long': 'Toronto Maple Leafs',
        'NHL': 'Toronto',
        'Name': 'MapleLeafs',
        'Subreddit': '/r/leafs',
        'TSN': 'Toronto',
        'TimeZone': 'ET'},
	'Oilers': {
		'Abbr': 'EDM',
        'Arena': 'Rexall Place',
        'ArenaPlace': 'Edmonton, AB, CAN',
        'City': u'Edmonton',
		'LineupURL': "24/edmonton-oilers",
        'Long': 'Edmonton Oilers',
        'NHL': 'Edmonton',
        'Name': 'Oilers',
        'Subreddit': '/r/edmontonoilers',
        'TSN': 'Edmonton',
        'TimeZone': 'MT'},
	'Panthers': {
		'Abbr': 'FLA',
        'Arena': 'BB&T Center',
        'ArenaPlace': 'Sunrise, FL, USA',
        'City': u'Florida',
		'LineupURL': "25/florida-panthers",
        'Long': 'Florida Panthers',
        'NHL': 'Florida',
        'Name': 'Panthers',
        'Subreddit': '/r/floridapanthers',
        'TSN': 'Florida',
        'TimeZone': 'ET'},
	'Penguins': {
		'Abbr': 'PIT',
        'Arena': 'Consol Energy Center',
        'ArenaPlace': 'Pittsburgh, PA, USA',
        'City': u'Pittsburgh',
        'Long': 'Pittsburgh Penguins',
		'LineupURL' : "36/pittsburgh-penguins", 
        'NHL': 'Pittsburgh',
        'Name': 'Penguins',
        'Subreddit': '/r/penguins',
        'TSN': 'Pittsburgh',
        'TimeZone': 'ET'},
	'Predators': {
		'Abbr': 'NSH',
        'Arena': 'Bridgestone Arena',
        'ArenaPlace': 'Nashville, TN, USA',
        'City': u'Nashville',
		'LineupURL': "29/nashville-predators",
        'Long': 'Nashville Predators',
        'NHL': 'Nashville',
        'Name': 'Predators',
        'Subreddit': '/r/predators',
        'TSN': 'Nashville',
        'TimeZone': 'CT'},
	'Rangers': {
		'Abbr': 'NYR',
        'Arena': 'Madison Square Garden',
        'ArenaPlace': 'New York, NY, USA',
        'City': u'NY Rangers',
		'LineupURL': "32/new-york-rangers",
        'Long': 'New York Rangers',
        'NHL': 'NY Rangers',
        'Name': 'Rangers',
        'Subreddit': '/r/rangers',
        'TSN': 'NY Rangers',
        'TimeZone': 'ET'},
	'RedWings': {
		'Abbr': 'DET',
        'Arena': 'Joe Louis Arena',
        'ArenaPlace': 'Detroit, MI, USA',
        'City': u'Detroit',
		'LineupURL' : "23/detroit-red-wings",
        'Long': 'Detroit Red Wings',
        'NHL': 'Detroit',
        'Name': 'RedWings',
        'Subreddit': '/r/detroitredwings',
        'TSN': 'Detroit',
        'TimeZone': 'ET'},
	'Sabres': {
		'Abbr': 'BUF',
        'Arena': 'First Niagara Center',
        'ArenaPlace': 'Buffalo, NY, USA',
        'City': u'Buffalo',
		'LineupURL': "16/buffalo-sabres/",
        'Long': 'Buffalo Sabres',
        'NHL': 'Buffalo',
        'Name': 'Sabres',
        'Subreddit': '/r/sabres',
        'TSN': 'Buffalo',
        'TimeZone': 'ET'},
	'Senators': {
		'Abbr': 'OTT',
        'Arena': 'Canadian Tire Centre',
        'ArenaPlace': 'Ottawa, ON, CAN',
        'City': u'Ottawa',
		'LineupURL': "33/ottawa-senators",
        'Long': 'Ottawa Senators',
        'NHL': 'Ottawa',
        'Name': 'Senators',
        'Subreddit': '/r/ottawasenators',
        'TSN': 'Ottawa',
        'TimeZone': 'ET'},
	'Sharks': {
		'Abbr': 'SJS',
        'Arena': 'SAP Center',
        'ArenaPlace': 'San Jose, CA, USA',
        'City': u'San Jose',
		'LineupURL': "37/san-jose-sharks",
        'Long': 'San Jose Sharks',
        'NHL': 'San Jose',
        'Name': 'Sharks',
        'Subreddit': '/r/sanjosesharks',
        'TSN': 'San Jose',
        'TimeZone': 'PT'},
	'Stars': {
		'Abbr': 'DAL',
        'Arena': 'American Airlines Center',
        'ArenaPlace': 'Dallas, TX, USA',
        'City': u'Dallas',
		'LineupURL': "22/dallas-stars", 
        'Long': 'Dallas Stars',
        'NHL': 'Dallas',
        'Name': 'Stars',
        'Subreddit': '/r/dallasstars',
        'TSN': 'Dallas',
        'TimeZone': 'CT'},
	'Wild': {
		'Abbr': 'MIN',
        'Arena': 'Xcel Energy Center',
        'ArenaPlace': 'St Paul, MN, USA',
        'City': u'Minnesota',
		'LineupURL': "27/minnesota-wild",
        'Long': 'Minnesota Wild',
        'NHL': 'Minnesota',
        'Name': 'Wild',
        'Subreddit': '/r/wildhockey',
        'TSN': 'Minnesota',
        'TimeZone': 'CT'}}


## --------------------------------------------------------------------------------------
## Global Variables
## --------------------------------------------------------------------------------------

#Dictionary for holding team schedules [ date, visitor, home, time(et), network/results ]
schedule = {}
team_stats = {}
team_players = {}
team_goalies = {}
team_injuries = {}
today_games = []
GT_Settings = {}
lineups_forwards = {}
lineups_defense = {}
lineups_goalies = {}


## --------------------------------------------------------------------------------------
## Get Team Schedule
## --------------------------------------------------------------------------------------
def get_team_schedule(team_name):
    schedule_file = cache_directory + "\\" + team_name + "-schedule.html"
    if os.path.exists(schedule_file):
        print "Reading cached team file for " + team_name + "...\r"
        with open(schedule_file, "r") as cache_file:
            page = cache_file.read()

    else:
        print "Downloading schedule for " + team_name + "...\r"
        w = urllib2.urlopen('http://{}.nhl.com/club/schedule.htm'.format(team_name.lower()))
        page = w.read()
        w.close()

        with open(schedule_file, "w") as cache_file:
            cache_file.write(page)

    soup = BeautifulSoup(page)

    for data in soup.find_all('table', 'data'):
        if not 'Preseason' in data.find('div', 'moduleHeader').text:
            schedule[team_name.lower()] = []
        
            for tr in data.findAll('tr', { 'class': [ 'rwEven', 'rwOdd' ]}):
                temp_sched = [td.text.replace('\n','').replace('\t','').replace(u'\xa0','').strip() for td in tr.findAll('td')]
                try:
                    temp_sched[0] = datetime.strptime(temp_sched[0],'%a, %d %b %Y')
                except:
                    temp_sched[0] = datetime.strptime(temp_sched[0],'%a %b %d, %Y')
                temp_sched.pop()
                schedule[team_name.lower()].append(temp_sched)

## --------------------------------------------------------------------------------------
## Get Team Injuries
## --------------------------------------------------------------------------------------
def get_team_injuries():
    if os.path.exists(InjuriesFile):
        print "Reading cached injury data...\r"
        with open(InjuriesFile, "r") as cache_file:
            page = cache_file.read()

    else:
        print "Downloading injuries data...\r"
        w = urllib2.urlopen(InjuryURL)
        page = w.read()
        w.close()

        with open(InjuriesFile, "w") as cache_file:
            cache_file.write(page)

    soup = BeautifulSoup(page)

    data = soup.find('table')
    for tr in data.find_all('tr'):
        if not "Status" in tr.text:
            if tr.find('h3'):
                teamname = tr.find('h3').text
                print teamname
                if not team_injuries.has_key(teamname):
                    team_injuries[teamname] = {}
            elif tr.has_attr('class'):
                if 'bg1' in tr.attrs['class'] or 'bg2' in tr.attrs['class']:
                    player = [td.text.replace(u'\xa0', ' ') for td in tr.find_all(['td', 'th'])]
                    print player
                    team_injuries[teamname][player[0]] = [player[x] for x in range(1,4)]

## --------------------------------------------------------------------------------------
## Get Team Injuries
## --------------------------------------------------------------------------------------
def get_team_stats():
    if os.path.exists(StandingsFile):
        print "Reading cached standings...\r"
        with open(StandingsFile, "r") as cache_file:
            page = cache_file.read()

    else:
        print "Downloading league standings...\r"
        w = urllib2.urlopen("http://www.nhl.com/ice/teamstats.htm?fetchKey=20142ALLSAAAll&sort=points&viewName=summary")
        page = w.read()
        w.close()

        with open(StandingsFile, "w") as cache_file:
            cache_file.write(page)

    soup = BeautifulSoup(page)

    tables = soup.findAll('tbody')
    for tr in tables[1].findAll('tr'):
        temp_array = [td.text for td in tr.findAll('td')]
        team = temp_array.pop(1)
        team_stats[team.lower()] = temp_array

## --------------------------------------------------------------------------------------
## Get Team Players
## --------------------------------------------------------------------------------------
def get_team_players(team_name):
    players_file = cache_directory + "\\" + team_name + "-players.html"
    if os.path.exists(players_file):
        print "Reading cached team file for " + team_name + "...\r"
        with open(players_file, "r") as cache_file:
            page = cache_file.read()

    else:
        print "Downloading players for " + team_name + "...\r"
        w = urllib2.urlopen('http://{}.nhl.com/club/stats.htm'.format(team_name.lower()))
        page = w.read()
        w.close()

        with open(players_file, "w") as cache_file:
            cache_file.write(page)

    soup = BeautifulSoup(page)

    team_players[team_name.lower()] = []
    team_goalies[team_name.lower()] = []

    tables = soup.findAll('table', {'class' : 'data'})
    for tr in tables[0].findAll('tr', { 'class' : ['rwEven', 'rwOdd']}):
        temp_player = [td.text for td in tr.findAll('td')]
        team_players[team_name.lower()].append(temp_player)

    for tr in tables[1].findAll('tr', { 'class' : ['rwEven', 'rwOdd']}):
        temp_goalie = [td.text for td in tr.findAll('td')]
        team_goalies[team_name.lower()].append(temp_goalie)

## --------------------------------------------------------------------------------------
## Scrape today's schedule
## --------------------------------------------------------------------------------------
def get_today_schedule():
    global today_games
    global game_count

    game_count = 0

    if os.path.exists(ScheduleFile):
        print "Reading cached schedule...\r"
        with open(ScheduleFile, "r") as cache_file:
            page = cache_file.read()
        
    else:
        print "Downloading today's schedule...\r"
        w = urllib2.urlopen('http://www.nhl.com/ice/schedulebyday.htm?date=' + datetime.now().strftime("%m/%d/%Y"))
        page = w.read()
        w.close()

        with open(ScheduleFile, "w") as cache_file:
            cache_file.write(page)

    soup = BeautifulSoup(page)
    today_games = []

    #Check to see if the schedule is for today
    contentBlock = soup.find("div", { "class" : "contentBlock"})
    h3 = contentBlock.find("h3").text
    page_date = time.strptime(''.join(h3.splitlines()), "%A %B %d, %Y")

    if page_date == time.strptime(datetime.now().strftime("%m/%d/%Y"), "%m/%d/%Y"):
        #The only <tbody> tag in the page is the schedule table
        data_table = soup.find('tbody')
        for tr in data_table.findAll('tr'):
            #Look for upcoming games
            if tr.find('div', { "class" : "skedStartTimeLocal" }):
                local_time = tr.find('div', { "class" : "skedStartTimeLocal" }).text

                lst = [td.text for td in tr]
                #Fix Montreal's name
                home_team = lst[1].replace(u'\xe9',u'e')
                away_team = lst[0].replace(u'\xe9',u'e')
                network = lst[3]
                # home team, away team, local time, poster, comment object, est datetime
                game_count += 1
                today_games.append({ "game_num" : game_count,
                                    "home_team" : home_team,
                                    "away_team" : away_team,
                                    "local_time" : local_time,
                                    "network" : network
                                    })

## --------------------------------------------------------------------------------------
## Check team lines
## --------------------------------------------------------------------------------------
def get_team_lines(team_name):
    lines_file = cache_directory + "\\" + team_name + "-lines.html"
    if os.path.exists(lines_file):
        print "Reading cached team file for " + team_name + "...\r"
        with open(lines_file, "r") as cache_file:
            page = cache_file.read()
    else:
        print "Downloading players for " + team_name + "...\r"
        w = urllib2.urlopen(TeamLineUpBaseURL + team_dicts[team_name]['LineupURL'])
        page = w.read()
        w.close()

        with open(lines_file, "w") as cache_file:
            cache_file.write(page)

    soup = BeautifulSoup(page)

    player_list = soup.find_all('table', { 'class' : 'playerlist' })

    forwards = []
    defense = []
    goalies = []

    ## Forwards
    for tr in player_list[0].find_all('tr'):
        forwards.append([td.text.replace('\n','') for td in tr.find_all('td') if len(td)])

    for tr in player_list[1].find_all('tr'):
        if not tr.find('th'):
            defense.append([td.text.replace('\n','') for td in tr.find_all('td') if len(td)])

    for tr in player_list[4].find_all('tr'):
        if not tr.find('th'):
            for td in tr.find_all('td'):
                goalies.append(td.text.replace('\n',''))

    lineups_forwards[team_name] = forwards
    lineups_defense[team_name] = defense
    lineups_goalies[team_name] = goalies


## --------------------------------------------------------------------------------------
## Check file dates
## --------------------------------------------------------------------------------------
def check_filedates():
    print "Checking cached data...\r"
    t1 = time.localtime()

    if os.path.exists(ScheduleFile):
        t2 = os.path.getmtime(ScheduleFile)
        if ((time.mktime(t1) - t2) / 60) > 60:
            os.remove(ScheduleFile)
            print "Deleting schedule file...\r"
        elif debug == 1:
            print "Schedule file life in minutes: " + str((time.mktime(t1) - t2) / 60) + "\r"

    if os.path.exists(AllPlayersFile):
        t2 = os.path.getmtime(AllPlayersFile)
        if ((time.mktime(t1) - t2) / 60) > 60:
            os.remove(AllPlayersFile)
            print "Deleting players file...\r"
        elif debug == 1:
            print "Players file life in minutes: " + str((time.mktime(t1) - t2) / 60) + "\r"

    if os.path.exists(AllGoaliesFile):
        t2 = os.path.getmtime(AllGoaliesFile)
        if ((time.mktime(t1) - t2) / 60) > 60:
            os.remove(AllGoaliesFile)
            print "Deleting goalies file...\r"
        elif debug == 1:
            print "Goalies file life in minutes: " + str((time.mktime(t1) - t2) / 60) + "\r"

    if os.path.exists(StandingsFile):
        t2 = os.path.getmtime(StandingsFile)
        if ((time.mktime(t1) - t2) / 60) > 60:
            os.remove(StandingsFile)
            print "Deleting standings file...\r"
        elif debug == 1:
            print "Standings file life in minutes: " + str((time.mktime(t1) - t2) / 60) + "\r"

    if os.path.exists(InjuriesFile):
        t2 = os.path.getmtime(InjuriesFile)
        if ((time.mktime(t1) - t2) / 60) > 60:
            os.remove(InjuriesFile)
            print "Deleting injuries file..."
        elif debug == 1:
            print "Injuries file life in minutes: " + str((time.mktime(t1) - t2) / 60) + "\r"

    for x in range(30):
        file_check = '%s\%s-lines.html' % (cache_directory,TeamNames[x])
        if os.path.exists(file_check):
            t2 = os.path.getmtime(file_check)
            if ((time.mktime(t1) - t2) / 60) > 60:
                os.remove(file_check)
                print "Deleting %s lines file..." % (TeamNames[x])
            elif debug == 1:
                print "%s lines file life in minutes: %d" % (TeamNames[x],(time.mktime(t1) - t2) / 60)
        

## --------------------------------------------------------------------------------------
## List files in a folder
## --------------------------------------------------------------------------------------
def ListFiles(sPath,sExt):
    # returns a list of names (with extension, without full path) of all files 
    # in folder sPath
    lsFiles = []
    for sName in os.listdir(sPath):
        if os.path.isfile(os.path.join(sPath, sName)) and sName[0-(len(sExt)):].lower() == sExt.lower():
            lsFiles.append(sName)
    return lsFiles


## --------------------------------------------------------------------------------------
## Build Thread File
## --------------------------------------------------------------------------------------
def build_game_thread():
    print 'Hi'


## --------------------------------------------------------------------------------------
## Mainline code
## --------------------------------------------------------------------------------------

def build_table():
    for team in team_dicts:
        print "\r\n|Field|Data|"
        print ":--:|:--:"
        print "|City|" + team['TeamCities'] + "|"
        for k,v in team.iter_items():
            print k
            if k is not 'TeamCities':
                print "|" + k + "|" + v + "|"


print "GameTimePy v1.0.14.1\r"
print "by sentry07 (/r/GameTime)\r\n"

this_directory = os.path.dirname(os.path.abspath(__file__)) + "\\"
cache_directory = this_directory + "Data"
output_directory = this_directory + "Generated"

ScheduleFile = cache_directory + "\schedule.html"
AllPlayersFile = cache_directory + "\AllPlayers.html"
AllGoaliesFile = cache_directory + "\AllGoalies.html"
StandingsFile = cache_directory + "\Standings.html"
InjuriesFile = cache_directory + "\Injuries.html"

if not os.path.exists(cache_directory):
    os.makedirs(cache_directory)

if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    
# check_filedates()
get_team_stats()
get_today_schedule()

print "\r\n"
print "Select template file to use:"
TemplateFiles = ListFiles(this_directory,'txt')
for idx, _file in enumerate(TemplateFiles):
    print "[%d] %s" % (idx, _file)
template_num = int(raw_input("> "))
if template_num <= len(TemplateFiles):
    print "Using %s for game thread." % (TemplateFiles[template_num])

if game_count > 0:
    print "\r\nToday's games:\r"
    for game in today_games:
        print "[" + str(game['game_num']) + "] " + game['away_team'] + " @ " + game['home_team'] + " : " + game['local_time'] + "\r"
    print "[0] Exit\r"
    game_num = int(raw_input("> "))

    if game_num <= game_count and game_num > 0:
        print "Please wait...\r"
else:
    print "\r\nNo games today.\r"
