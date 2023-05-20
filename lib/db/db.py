from pymongo import MongoClient
from contextlib import contextmanager

from pymongo.errors import PyMongoError

from lib.configlib import DatabaseConfig
from lib.exceptions import DatabaseException, ConfigException
from lib.logger import Logger


class Database:
    def __init__(self, creds: DatabaseConfig, db_name: str = None):
        Logger.attention("Trying to establish a connection to the database.")
        if not isinstance(creds, DatabaseConfig):
            raise ConfigException("Incorrect credential type provided to the class constructor")

        try:
            self.client = MongoClient(creds.db_host, creds.db_port, username=creds.db_user, password=creds.db_pass,
                                      authSource=creds.db_auth_source, connectTimeoutMS=5000)
            self.database = self.client[db_name] if db_name else None

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

    def insert_document(self, collection_name, document):
        Logger.attention("Inserting a document into the database..")

        try:
            collection = self.get_collection(collection_name)
            doc = collection.insert_one(document)

            Logger.success("Inserted document successfully!")

            return doc
        except DatabaseException:
            Logger.error("Unknown collection name provided. Please check your environment and try again later.")
        except PyMongoError as db_err:
            Logger.error(f"Unable to insert the provided document.\nErr: {str(db_err)}")

    def find_documents(self, collection_name, query=None, projection=None):
        collection = self.get_collection(collection_name)
        return collection.find(query, projection)

    def find_one_document(self, collection_name, query=None, projection=None):
        collection = self.get_collection(collection_name)
        return collection.find_one(query, projection)

    def update_document(self, collection_name, query, update):
        collection = self.get_collection(collection_name)
        return collection.update_many(query, update)

    def delete_document(self, collection_name, query):
        collection = self.get_collection(collection_name)
        return collection.delete_many(query)

    def __enter__(self):
        Logger.success("Database connection established successfully!")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Logger.attention("Database connection closed")
        pass
