from pymongo import MongoClient
import personal

#personal.user
#personal.dbname
#personal.dbpw
#personal.port

login = "mongodb://" + personal.user + ":" + personal.dbpw + "@stoctistics-shard-00-00-vjbe.azure.mongodb.net:" + personal.port + ",stoctistics-shard-00-01-vjbe.azure.mongodb.net:" + personal.port +",stoctistics-shard-00-02-vjvbe.azure.mongodb.net:" + personal.port + "/" + personal.dbname + "?ssl=true&replicaSet=Stoctistics-shard-0&authSource=admin&retryWrites=true&w=majority"

#client = MongoClient("mongodb://richard:<password>@stoctistics-shard-00-00-vjvbe.azure.mongodb.net:27017,stoctistics-shard-00-01-vjvbe.azure.mongodb.net:27017,stoctistics-shard-00-02-vjvbe.azure.mongodb.net:27017/<dbname>?ssl=true&replicaSet=Stoctistics-shard-0&authSource=admin&retryWrites=true&w=majority")

client = MongoClient(login)
db = client["stocks"]
SPY = db["SPY"]
