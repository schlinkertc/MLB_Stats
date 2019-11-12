#!/usr/bin/env python
# coding: utf-8

# In[28]:


import statsapi as mlb
import pandas as pd

# get 10 years of games in 3 parts


games = mlb.schedule(start_date='2016-04-03',end_date='2019-09-29',sportId='1')
games2 = mlb.schedule(start_date='2012-03-31',end_date='2015-10-01',sportId='1')
games3 = mlb.schedule(start_date='2009-04-01',end_date='2011-10-01',sportId='1')

#combine games data
games.extend(games2)
games.extend(games3)


df = pd.DataFrame(games)

#parse the dataframe.

df = df[df['game_type']=='R']
df = df[['game_id','game_datetime','game_date','status','away_id','home_id']]
df['game_datetime'] = df['game_datetime'].map(lambda x: x.replace('T',' ').strip('Z'))
duplicate_games = df[df['game_id'].duplicated(keep=False)==True]['game_id']
df.drop(duplicate_games.index, inplace=True)


# In[76]:


df
