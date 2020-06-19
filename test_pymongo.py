from pymongo import MongoClient

client = MongoClient("mongodb://richard:<password>@stoctistics-shard-00-00-vjvbe.azure.mongodb.net:27017,stoctistics-shard-00-01-vjvbe.azure.mongodb.net:27017,stoctistics-shard-00-02-vjvbe.azure.mongodb.net:27017/<dbname>?ssl=true&replicaSet=Stoctistics-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.test
