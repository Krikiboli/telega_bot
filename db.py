import pymongo

client = pymongo.MongoClient()
db = client["Fefe_info"]
collection = db["Начальники"]


def create_many(data):
    collection.insert_many(data)


def create(data_dict):
    collection.insert_one(data_dict)


def read(elem_dict):
    return collection.find_one(elem_dict)


def update(data, new_field):
    return collection.update_one(data, {'$set': new_field})


def delete(data):
    return collection.delete_one(data)
