import os

from pymongo import MongoClient

from pymongo.errors import PyMongoError

from lib.exceptions import DatabaseException, EnvironmentException
from lib.logger import Logger


class Database:
    def __init__(self):
        Logger.attention("Trying to establish a connection to the database.")

        try:
            self.client = MongoClient(os.getenv("DB_HOST"), os.getenv("DB_PORT"), username=os.getenv("DB_USER"),
                                      password=os.getenv("DB_PASS"),
                                      authSource=os.getenv("db_auth_source"), connectTimeoutMS=5000)
            self.database = self.client[os.getenv("DB_NAME")] if os.getenv("DB_NAME") else None

            Logger.success("Connection to the database established successfully!")
        except ConnectionError:
            Logger.error(
                "Unable to establish a connection to the database. Please check your environment and try again later.")

    def close_connection(self):
        if self.client:
            self.client.close()

    def get_collection(self, collection_name):
        if self.database is not None:
            return self.database[collection_name]
        else:
            raise DatabaseException("No database specified.")

    def find_documents(self, collection_name, query=None, projection=None):
        Logger.attention("Finding documents in the database..")

        try:
            collection = self.get_collection(collection_name)
            return collection.find(query, projection)
        except DatabaseException:
            Logger.error("Unknown collection name provided. Please check your environment and try again later.")
        except PyMongoError as db_err:
            Logger.error(f"Unable to find documents.\nErr: {str(db_err)}")

    def find_one_document(self, collection_name, query=None, projection=None):
        Logger.attention("Finding one document in the database..")

        try:
            collection = self.get_collection(collection_name)
            return collection.find_one(query, projection)
        except DatabaseException:
            Logger.error("Unknown collection name provided. Please check your environment and try again later.")
        except PyMongoError as db_err:
            Logger.error(f"Unable to find the document.\nErr: {str(db_err)}")

    def update_document(self, collection_name, query, update):
        Logger.attention("Updating documents in the database..")

        try:
            collection = self.get_collection(collection_name)
            return collection.update_many(query, update)
        except DatabaseException:
            Logger.error("Unknown collection name provided. Please check your environment and try again later.")
        except PyMongoError as db_err:
            Logger.error(f"Unable to update documents.\nErr: {str(db_err)}")

    def delete_document(self, collection_name, query):
        Logger.attention("Deleting documents from the database..")

        try:
            collection = self.get_collection(collection_name)
            return collection.delete_many(query)
        except DatabaseException:
            Logger.error("Unknown collection name provided. Please check your environment and try again later.")
        except PyMongoError as db_err:
            Logger.error(f"Unable to delete documents.\nErr: {str(db_err)}")

    def __enter__(self):
        Logger.success("Database connection established successfully!")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Logger.attention("Database connection closed")
        pass
