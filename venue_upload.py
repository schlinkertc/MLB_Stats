import config
import game_log_parse
import mysql.connector

cnx = mysql.connector.connect(host = config.host, user= config.user, passwd = config.passwd, database='MLB_Stats')
cursor = cnx.cursor()

stmt = """SELECT gameid FROM games"""
cursor.execute(stmt)
game_ids = []
for obj in cursor:
    game_ids.append(obj)
