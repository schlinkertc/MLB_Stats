import statsapi as mlb
import pandas as pd
import time

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
