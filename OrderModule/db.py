from pymongo import MongoClient

DOMAIN = "orders_db"
PORT = 27017

db_conn = MongoClient(host=[str(DOMAIN) + ":" + str(PORT)],
                      serverSelectionTimeoutMS=3000,
                      username='root',
                      password='example')

orders_database = db_conn['orders']
