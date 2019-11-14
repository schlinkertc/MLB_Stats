import statsapi as mlb
import pandas as pd
import time
import query_helper

# get games
def get_games(start_year,end_year):
    years = range(start_year,end_year+1)
    games = []
    for y in years:
        try:
            games.append(mlb.schedule(start_date='{}-01-01'.format(y),end_date='{}-12-29'.format(y),sportId='1'))
        except:
            get_games(y,y)

    return [item for sublist in games for item in sublist]

    #df = pd.DataFrame(games)

    #df = df[df['game_type']=='R']
    #df = df[['game_id','game_datetime','game_date','status','away_id','home_id','game_type']]
    #df['game_datetime'] = df['game_datetime'].map(lambda x: x.replace('T',' ').strip('Z'))
    # duplicate_games = df[df['game_id'].duplicated(keep=False)==True]['game_id']
    # df.drop(duplicate_games.index, inplace=True)

    #return df

def get_venue(game_id):
    null_dict = {'null':'null'}
    c = mlb.get('game',{'gamePk':game_id})['gameData']['venue']
    venue = ({
    'venue_id':c['id'],
    'name':c.get('name','null'),
    'city':c['location'].get('city','null'),
    'state':c['location'].get('state','null'),
    'latitude':c['location'].get('defaultCoordinates',null_dict).get('latitude','null'),
    'longitude':c['location'].get('defaultCoordinates',null_dict).get('longitude','null'),
    'timezone':c['timeZone'].get('tz','null'),
    'capacity':c['fieldInfo'].get('capacity','null'),
    'turf_type':c['fieldInfo'].get('turfType','null'),
    'roof_type':c['fieldInfo'].get('roofType','null'),
    'left_line':c['fieldInfo'].get('leftLine','null'),
    'left_center':c['fieldInfo'].get('leftCenter','null'),
    'center':c['fieldInfo'].get('center','null'),
    'right_center':c['fieldInfo'].get('rightCenter','null'),
    'right_line':c['fieldInfo'].get('rightLine','null'),
    })
    return venue

# takes in a list of game_ids and inserts venue information for the game
# if not already in DB
def get_insert_venues(list_of_ids):

    #connect to DB, get list of venue_ids already in DB
    query_helper.connect('MLB_Stats')
    venues = [item for sublist in query_helper.query('''select venue_id from venues''') for item in sublist]

    #get venue info for game_ids in DB
    for game_id in list_of_ids:
        venue = get_venue(game_id)

        # insert venue into db if it's not already there
        if venue['venue_id'] not in venues:
            query_helper.insert_venue(venue)
            print('inserted',venue['venue_id'])
            venues.append(venue['venue_id'])
        else:
            print('already inserted',game_id)

def get_teams(ids):
    #format list of teams from MYSql query into a single, de-duped list
    all_team_ids = [item for sublist in ids for item in sublist ]
    all_team_ids = list(set(all_team_ids))

    # look up teams with mlb-statsapi
    teams = [mlb.lookup_team(x) for x in all_team_ids]
    #flatten list of lists
    teams = [item for sublist in teams for item in sublist]
    #convert to dataframe to parse
    df = pd.DataFrame(teams,columns=['id','name'])

    # list all the teams in the American League
    AL_teams = ['Oakland Athletics','Kansas City Royals','Houston Astros','Detroit Tigers','Cleveland Indians','Boston Red Sox','Baltimore Orioles','Los Angeles Angels','New York Yankees','Chicago White Sox','Minnesota Twins','Texas Rangers','Toronto Blue Jays','Tampa Bay Rays','Seattle Mariners']
    # set the defaultleague value to NL
    df['league']= 'NL'

    # replace "NL" with "AL" for teams in AL_teams
    df['league'] = df[df['name'].isin(AL_teams)==True]['league'].str.replace('N','A')
    #fill nan values with 'NL'
    df.fillna('NL',inplace=True)

    return df
