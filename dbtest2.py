import pymysql
import sys
import os
import requests
import base64

host="database-1.cb5pctivsgrb.us-east-1.rds.amazonaws.com"
username="root"
port=3306
database="log-in"
password="ksc2021583"

db=pymysql.connect(host,username,password)
    
cursor=db.cursor()
print(cursor)