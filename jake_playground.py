
# coding: utf-8

# In[15]:


import charlie_functions
import config
import mysql.connector
import pandas as pd


# In[32]:


game_list = charlie_functions.get_games(2009,2019)


# In[33]:


game_list[:3]


# In[34]:


def parse_game(game):
    game_parsed = {'gameid' : game['game_id'],
                   'game_end_datetime' : game['game_datetime'],
                   'game_date' : game['game_date'],
                   'home_id' : game['home_id'],
                   'away_id' : game['away_id'],
                   'status' : game['status']
    }
    
    return game_parsed


# In[12]:


regular_season_games = []
for item in game_list:
    if item['game_type'] != 'R':
        pass
    else:
        regular_season_games.append(parse_game(item))


# In[13]:


len(regular_season_games)


# In[36]:


count_r =0
count_else = 0
for item in game_list:
    if item['game_type'] == 'R':
        count_r += 1
    else:
        count_else += 1
count_r,count_else


# In[24]:


162*15*10


# In[16]:


df = pd.DataFrame(regular_season_games)


# In[17]:


df.head()


# In[20]:


df[['gameid','game_end_datetime','game_date','status','away_id','home_id']]
df['game_end_datetime'] = df['game_end_datetime'].map(lambda x: x.replace('T',' ').strip('Z'))
duplicate_games = df[df['gameid'].duplicated(keep=False)==True]['gameid']
df.drop(duplicate_games.index, inplace=True)


# In[38]:


df = df[['gameid','game_end_datetime','game_date','status','away_id','home_id']]


# In[39]:




