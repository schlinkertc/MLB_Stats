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

## I used the following code to query our AWS database and create DataFrames. DataFrames were later merged
## into a master DataFrame for easier reading.

query_helper.set_database_name('MLB_Stats')

games_teams = query_helper.query_to_df("""select G.gameid, G.home_team, t.team_name as away_team, G.game_date, G.status from
(select g.gameid, g.game_date, g.status, t.team_name as home_team, g.away_id
from MLB_Stats.games g
inner join MLB_Stats.teams t on t.team_id=g.home_id) G
inner join MLB_Stats.teams t on t.team_id=G.away_id;""")

runs_games = query_helper.query_to_df("""SELECT A.gameid, A.total_runs, t.league FROM
(SELECT g.gameid, i.home_team_runs + i.away_team_runs as total_runs, g.home_id
from games g
inner join game_info i on i.gameid=g.gameid) A
inner join teams t on t.team_id=A.home_id;""")

df_weather = query_helper.query_to_df("""select
i.gameid,
i.home_team_runs + i.away_team_runs as total_runs, i.weather_category
from
MLB_Stats.game_info i;""")

df_temp = query_helper.query_to_df("""select
i.gameid,
i.home_team_runs + i.away_team_runs as total_runs, i.temp
from
MLB_Stats.game_info i;""")

df_venue = query_helper.query_to_df("""
    select
    i.gameid, i.away_team_runs+i.home_team_runs as run_total,
    v.`name` as venue_name
    from game_info i
    inner join venues v
    on i.venue_id=v.venue_id;""")

df_venue_teams = df_venue.merge(games_teams,how='inner',on='gameid')
df = df_venue_teams.merge(df_temp,how='inner',on='gameid')

df = df.merge(df_weather,how='inner',on='gameid')

df.drop(columns=['total_runs_x','total_runs_y'],inplace=True)

division_map = {'Boston Red Sox': 'AL_east',
 'New York Yankees': 'AL_east',
 'Tampa Bay Rays': 'AL_east',
 'Toronto Blue Jays': 'AL_east',
 'Baltimore Orioles': 'AL_east',
 'Minnesota Twins':'AL_central',
 'Kansas City Royals':'AL_central',
 'Detroit Tigers':'AL_central',
 'Chicago White Sox':'AL_central',
 'Cleveland Indians':'AL_central',
 'Los Angeles Angels':'AL_west',
 'Oakland Athletics':'AL_west',
 'Seattle Mariners':'AL_west',
 'Texas Rangers':'AL_west',
 'Houston Astros':'AL_west',
 'Philadelphia Phillies':'NL_east',
 'Miami Marlins':'NL_east',
 'New York Mets':'NL_east',
 'Atlanta Braves':'NL_east',
 'Washington Nationals':'NL_east',
 'St. Louis Cardinals':'NL_central',
 'Milwaukee Brewers':'NL_central',
 'Chicago Cubs':'NL_central',
 'Cincinnati Reds':'NL_central',
 'Pittsburgh Pirates':'NL_central',
 'Los Angeles Dodgers':'NL_west',
 'Arizona Diamondbacks':'NL_west',
 'San Francisco Giants':'NL_west',
 'Colorado Rockies':'NL_west',
 'San Diego Padres':'NL_west'}

df_venue_teams['division'] = games_teams['home_team'].map(lambda x : division_map[x])

def get_gameData(game_ids):
    games = []

    for game_id in game_ids:
        APIcall = mlb.get('game',{"gamePk":game_id})

        gameData = APIcall['gameData']

        game = gameData['game']

        game['home_id'] = gameData['teams']['home']['id']
        game['away_id'] = gameData['teams']['away']['id']
        game['venue_id'] = gameData['venue']['id']

        games.append(game)
    return pd.DataFrame(games)

def get_weather(game_ids):
    game_weather = []

    for game_id in game_ids:
        APIcall = mlb.get('game',{"gamePk":game_id})

        weather = APIcall['gameData']['weather']
        weather['pk'] = game_id

        game_weather.append(weather)
    return pd.DataFrame(game_weather)
