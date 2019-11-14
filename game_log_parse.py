import statsapi as mlb


def box_upload(game_id):
    game = mlb.boxscore_data(game_id)
    game_dict = {'gameid' : game_id,
            'home_team_runs' : game['homeBattingTotals']['r'],
            'away_team_runs' : game['awayBattingTotals']['r'],
     }

    for item in game['gameBoxInfo']:
        if item['label']=='Venue':
            game_dict['venue'] = (item['value'])
        elif item['label']=='Weather':
            game_dict['weather_category'] = item['value'].split(',')[1].lower().strip().strip('.')
            game_dict['temp'] = int(item['value'].split(',')[0].split(' ')[0])
        elif item['label']=='Wind':
            game_dict['wind_mph'] = int(item['value'].split(',')[0].split(' ')[0])
            game_dict['wind_direction'] = item['value'].split(',')[1].lower().strip().strip('.')
        else:
            pass

    return game_dict

a = mlb.get('game',{'gamePk': 446916})
a.keys()
a['gameData']['weather']['wind'].split(',')[0]

def box_upload_get(game_id):
    game = mlb.get('game',{'gamePk': game_id})

    game_dict = {'gameid' : game_id,
            'home_team_runs' : game['liveData']['boxscore']['teams']['home']['teamStats']['batting']['runs'],
            'away_team_runs' : game['liveData']['boxscore']['teams']['away']['teamStats']['batting']['runs'],
            'venue_id' : game['gameData']['venue'].get('id','null'),
            'weather_category' : game['gameData']['weather'].get('condition','null').lower(),
            'temp' : int(game['gameData']['weather'].get('temp','null')),
            'wind_mph' : int(game['gameData']['weather'].get('wind','null').split(',')[0].split(' ')[0]),
            'wind_direction' : game['gameData']['weather'].get('wind','null').split(',')[1].strip().lower()
     }


    return game_dict
box_upload_get(244194)
