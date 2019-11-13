#!/usr/bin/env python
# coding: utf-8

# In[25]:


import config
import mysql.connector as mysql
from mysql.connector import errorcode
import pandas as pd

database_name = 'X'

def set_database_name(database):
    global database_name
    database_name = database

def connect(database_name):
    global cnx
    cnx = mysql.connect(
    host = config.host,
    user = config.admin,
    passwd = config.password,
    database = database_name)
    global cursor
    cursor = cnx.cursor()


# In[9]:


def query(query_string):
    connect(database_name)
    
    cursor.execute(query_string)
    return cursor.fetchall()
    
    cursor.close()
    cnx.close()
    
    
def query_to_df(query_string):
    connect(database_name)
    
    cursor.execute(query_string)
    
    df = pd.DataFrame(cursor.fetchall())
    df.columns = [x[0] for x in cursor.description]
    return df
    
    cursor.close()
    cnx.close()

def create_table(create_query):    
    cursor = cnx.cursor()
    try:
        print("Creating a new table")
        cursor.execute(create_query)
    except mysql.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

    cursor.close()
    cnx.close()


def insert_venue(venue_dict):
    connect(database_name)
    statement = """INSERT INTO venues(
                venue_id,
                name,
                city,
                state,
                latitude,
                longitude,
                timezone,
                capacity,
                turf_type,
                roof_type,
                left_line,
                left_center,
                center,
                right_center,
                right_line)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    data = tuple(venue_dict.values())
    cursor.execute(statement, data)
    cnx.commit()
    
#query_helper.create_table("""CREATE TABLE venues(
# venue_id INT(5),
# name VARCHAR (35),
# city VARCHAR (35),
# state VARCHAR (35),
# latitude FLOAT,
# longitude FLOAT,
# timezone VARCHAR (35),
# capacity INT(6),
# turf_type VARCHAR(35),
# roof_type VARCHAR(35),
# left_line INT (3),
# left_center INT (3),
# center INT (3),
# right_center INT (3),
# right_line INT (3),
# PRIMARY KEY (venue_id))
# ;""")




