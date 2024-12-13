from pymongo import MongoClient

con = MongoClient(
    'mongodb+srv://lucasprobst:********@db-convidados.uwkdk.mongodb.net/',
    tlsAllowInvalidCertificates=True
)
db = con.get_database('BancoConvidados')
collection = db.get_collection('dadosConvidados')
collection_login = db.get_collection('dadosLogin')