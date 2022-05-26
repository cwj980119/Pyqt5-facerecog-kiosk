import pymysql

db=pymysql.connect(host="localhost",user="root", password="ksc2021583", charset="utf8")
print(db)
cursor=db.cursor()
cursor.execute('USE classicmodels;')

db.commit()
db.close()