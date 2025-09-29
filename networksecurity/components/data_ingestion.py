from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import numpy as np
import pandas as pd
import pymongo
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self) -> pd.DataFrame:
        """
        Read all data from MongoDB collection and return as DataFrame
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            logging.info(f"Connecting to MongoDB Database: {database_name}, Collection: {collection_name}")

            mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = mongo_client[database_name][collection_name]

            count = collection.count_documents({})
            logging.info(f"Total documents in collection: {count}")
            if count == 0:
                raise ValueError(f"The collection '{collection_name}' is empty in database '{database_name}'.")

            # Fetch all documents
            df = pd.DataFrame(list(collection.find()))

            # Drop _id if exists
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            # Replace "na" strings with np.nan
            df.replace({"na": np.nan}, inplace=True)

            logging.info(f"DataFrame created with shape: {df.shape}")
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Save DataFrame to feature store path
        """
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            logging.info(f"Feature store CSV created at: {feature_store_file_path}")
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        """
        Split the data into train and test CSVs
        """
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42
            )
            logging.info("Performed train-test split.")

            # Create directories if not exists
            train_dir = os.path.dirname(self.data_ingestion_config.training_file_path)
            test_dir = os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(train_dir, exist_ok=True)
            os.makedirs(test_dir, exist_ok=True)

            # Save CSVs
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info(f"Train CSV saved at: {self.data_ingestion_config.training_file_path}")
            logging.info(f"Test CSV saved at: {self.data_ingestion_config.testing_file_path}")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Full data ingestion pipeline: fetch, save feature store, split train-test
        """
        try:
            logging.info("Starting data ingestion process...")

            # Fetch data from MongoDB
            dataframe = self.export_collection_as_dataframe()

            # Save feature store CSV
            dataframe = self.export_data_into_feature_store(dataframe)

            # Split train/test and save
            self.split_data_as_train_test(dataframe)

            # Create artifact
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            logging.info("Data ingestion completed successfully.")
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
