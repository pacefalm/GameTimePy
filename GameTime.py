# -*- coding: cp1252 -*-

## Import Modules
from datetime import datetime
from bs4 import BeautifulSoup
import urllib2
## http://home.wlu.edu/~lambertk/breezypythongui/

## Constants Section
TeamNames = ["Penguins", "Devils", "Rangers", "Islanders", "Flyers", "Blackhawks", "RedWings", "Blues", "BlueJackets", "Predators", "Canadiens", "Bruins", "Senators", "MapleLeafs", "Sabres", "Canucks", "Wild", "Oilers", "Flames", "Avalanche", "Ducks", "Kings", "Stars", "Sharks", "Coyotes", "Jets", "Hurricanes", "Capitals", "Lightning", "Panthers"]
TeamCities = ["Pittsburgh", "New Jersey", "NY Rangers", "NY Islanders", "Philadelphia", "Chicago", "Detroit", "St. Louis", "Columbus", "Nashville", "Montréal", "Boston", "Ottawa", "Toronto", "Buffalo", "Vancouver", "Minnesota", "Edmonton", "Calgary", "Colorado", "Anaheim", "Los Angeles", "Dallas", "San Jose", "Phoenix", "Winnipeg", "Carolina", "Washington", "Tampa Bay", "Florida"]
TeamLong = ["Pittsburgh Penguins", "New Jersey Devils", "New York Rangers", "New York Islanders", "Philadelphia Flyers", "Chicago Blackhawks", "Detroit Red Wings", "St. Louis Blues", "Columbus Blue Jackets", "Nashville Predators", "Montreal Canadiens", "Boston Bruins", "Ottawa Senators", "Toronto Maple Leafs", "Buffalo Sabres", "Vancouver Canucks", "Minnesota Wild", "Edmonton Oilers", "Calgary Flames", "Colorado Avalanche", "Anaheim Ducks", "Los Angeles Kings", "Dallas Stars", "San Jose Sharks", "Phoenix Coyotes", "Winnipeg Jets", "Carolina Hurricanes", "Washington Capitals", "Tampa Bay Lightning", "Florida Panthers"]
TeamNamesAbbr = ["PIT", "NJD", "NYR", "NYI", "PHI", "CHI", "DET", "STL", "CBJ", "NSH", "MON", "BOS", "OTT", "TOR", "BUF", "VAN", "MIN", "EDM", "CGY", "COL", "ANA", "LOS", "DAL", "SJS", "PHO", "WPG", "CAR", "WSH", "TBL", "FLA"]
TeamReddits = ["/r/penguins", "/r/devils", "/r/rangers", "/r/newyorkislanders", "/r/flyers", "/r/hawks", "/r/detroitredwings", "/r/stlouisblues", "/r/bluejackets", "/r/predators", "/r/habs", "/r/bostonbruins", "/r/ottawasenators", "/r/leafs", "/r/sabres", "/r/canucks", "/r/wildhockey", "/r/edmontonoilers", "/r/calgaryflames", "/r/coloradoavalanche", "/r/anaheimducks", "/r/losangeleskings", "/r/dallasstars", "/r/sanjosesharks", "/r/coyotes", "/r/winnipegjets", "/r/canes", "/r/caps", "/r/tampabaylightning", "/r/floridapanthers"]
TeamArenas = ["Consol Energy Center", "Prudential Center", "Madison Square Garden", "Nassau Veterans Memorial Coliseum", "Wells Fargo Center", "United Center", "Joe Louis Arena", "Scottrade Center", "Nationwide Arena", "Bridgestone Arena", "Bell Centre", "TD Garden", "Canadian Tire Centre", "Air Canada Centre", "First Niagara Center", "Rogers Arena", "Xcel Energy Center", "Rexall Place", "Scotiabank Saddledome", "Pepsi Center", "Honda Center", "Staples Center", "American Airlines Center", "SAP Center", "Jobing.com Arena", "MTS Centre", "PNC Arena", "Verizon Center", "Tampa Bay Times Forum", "BB&T Center"]
TeamArenaPlace = ["Pittsburgh, PA, USA", "Newark, NJ, USA", "New York, NY, USA", "Long Island, NY, USA", "Philadelphia, PA, USA", "Chicago, IL, USA", "Detroit, MI, USA", "St Louis, MO, USA", "Columbus, OH, USA", "Nashville, TN, USA", "Montreal, QC, CAN", "Boston, MA, USA", "Ottawa, ON, CAN", "Toronto, ON, CAN", "Buffalo, NY, USA", "Vancouver, BC, CAN", "St Paul, MN, USA", "Edmonton, AB, CAN", "Calgary, AB, CAN", "Denver, CO, USA", "Anaheim, CA, USA", "Los Angeles, CA, USA", "Dallas, TX, USA", "San Jose, CA, USA", "Glendale, AZ, USA", "Winnipeg, MB, CAN", "Raleigh, NC, USA", "Washington, DC, USA", "Tampa, FL, USA", "Sunrise, FL, USA"]
TeamTimeZone = ["ET", "ET", "ET", "ET", "ET", "CT", "ET", "CT", "ET", "CT", "ET", "ET", "ET", "ET", "ET", "PT", "CT", "MT", "MT", "MT", "PT", "PT", "CT", "PT", "MT", "CT", "ET", "ET", "ET", "ET"]


## Build Dictionaries
by_city = {}
by_abbr = {}
by_nhl = {}
by_tsn = {}

for x in range(0,30):
    by_city[TeamCities[x]] = {
        "name"      : TeamNames[x],
        "long"      : TeamLong[x],
        "arena"     : TeamArenas[x],
        "location"  : TeamArenaPlace[x],
        "abbr"      : TeamNamesAbbr[x],
        "reddit"    : TeamReddits[x],
        "tz"        : TeamTimeZone[x]
        }

    by_abbr[TeamNamesAbbr[x]] = {
        "city"      : TeamCities[x],
        "name"      : TeamNames[x],
        "long"      : TeamLong[x],
        "arena"     : TeamArenas[x],
        "location"  : TeamArenaPlace[x],
        "reddit"    : TeamReddits[x],
        "tz"        : TeamTimeZone[x]
        }


## Global Variables

#Dictionary for holding team schedules [ date, visitor, home, time(et), network/results ]
schedule = {}


## Global Functions
def get_schedule(team_name):
    w = urllib2.urlopen('http://{}.nhl.com/club/schedule.htm'.format(team_name.lower()))
    soup = BeautifulSoup(w.read())
    w.close()

    data = soup.find('table', 'data')
    schedule[team_name.lower()] = []
    
    for tr in data.findAll('tr', { 'class': [ 'rwEven', 'rwOdd' ]}):
        temp_sched = [td.text.replace('\n','').replace('\t','').replace(u'\xa0','').strip() for td in tr.findAll('td')]
        try:
            temp_sched[0] = datetime.strptime(temp_sched[0],'%a, %d %b %Y')
        except:
            temp_sched[0] = datetime.strptime(temp_sched[0],'%a %b %d, %Y')
        temp_sched.pop()
        schedule[team_name.lower()].append(temp_sched)

