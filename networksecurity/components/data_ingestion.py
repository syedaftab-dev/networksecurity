# -------------------------------
# Import required modules
# -------------------------------
from networksecurity.exception.exception import NetworkSecurityException  # Custom exception class
from networksecurity.logging.logger import logging                         # Logger to log info
from networksecurity.entity.config_entity import DataIngestionConfig      # Config with paths, MongoDB info
from networksecurity.entity.artifact_entity import DataIngestionArtifact  # Artifact to return paths

import os      # For folder/file operations
import sys     # For exception details
import numpy as np  # For handling missing values
import pandas as pd  # For DataFrame operations
import pymongo      # MongoDB client
from sklearn.model_selection import train_test_split  # For train/test split
from dotenv import load_dotenv  # Load environment variables

# Load MongoDB connection string from .env file
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")  # Example: "mongodb+srv://username:password@cluster0.mongodb.net"

# -------------------------------
# Data Ingestion Class
# -------------------------------
class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        """
        Constructor: config object ko store karte hain
        Example: 
        config = DataIngestionConfig(
            database_name="network_db",
            collection_name="attacks",
            feature_store_file_path="artifact/feature_store/data.csv",
            training_file_path="artifact/train/train.csv",
            testing_file_path="artifact/test/test.csv",
            train_test_split_ratio=0.2
        )
        """
        try:
            # Store the config object for later use in methods
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            # Agar koi error aaye initialization me, custom exception throw kar do
            raise NetworkSecurityException(e, sys)

    # -------------------------------
    # Step 1: Export MongoDB collection as DataFrame
    # -------------------------------
    def export_collection_as_dataframe(self) -> pd.DataFrame:
        """
        MongoDB collection se saara data fetch karke DataFrame me convert karna
        Example:
        MongoDB data:
        | feature1 | feature2 | label |
        |----------|----------|-------|
        | 1        | 0        | 0     |
        | 2        | "na"     | 1     |
        | 3        | 1        | 0     |
        
        After conversion:
        | feature1 | feature2 | label |
        |----------|----------|-------|
        | 1        | 0        | 0     |
        | 2        | NaN      | 1     |
        | 3        | 1        | 0     |
        """
        try:
            # Get database and collection name from config
            db_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            logging.info(f"Connecting to MongoDB Database: {db_name}, Collection: {collection_name}")

            # Connect to MongoDB using pymongo
            mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = mongo_client[db_name][collection_name]

            # Count total documents in collection
            count = collection.count_documents({})
            logging.info(f"Total documents in collection: {count}")

            # Agar collection empty hai to error throw karo
            if count == 0:
                raise ValueError(f"The collection '{collection_name}' is empty in database '{db_name}'.")

            # Convert all documents to Pandas DataFrame
            df = pd.DataFrame(list(collection.find()))

            # Drop MongoDB default _id column if exists
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            # Replace "na" strings with np.nan for proper missing value handling
            df.replace({"na": np.nan}, inplace=True)

            logging.info(f"DataFrame created with shape: {df.shape}")  # Example shape: (1000, 10)
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # -------------------------------
    # Step 2: Export DataFrame to Feature Store CSV
    # -------------------------------
    def export_data_into_feature_store(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        DataFrame ko feature store CSV me save karna
        Example:
        dataframe shape: (1000, 10)
        feature_store_file_path: artifact/feature_store/data_10_10_2025.csv
        """
        try:
            # Path to save CSV from config
            feature_store_path = self.data_ingestion_config.feature_store_file_path

            # Directory create karlo agar exist nahi karti
            dir_path = os.path.dirname(feature_store_path)
            os.makedirs(dir_path, exist_ok=True)

            # Save DataFrame as CSV
            dataframe.to_csv(feature_store_path, index=False, header=True)
            logging.info(f"Feature store CSV created at: {feature_store_path}")

            # Return dataframe for next step
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # -------------------------------
    # Step 3: Split data into Train/Test CSVs
    # -------------------------------
    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        """
        Split DataFrame into train/test using ratio from config
        Example:
        train_test_split_ratio = 0.2
        dataframe shape: (1000, 10)
        train_set shape: (800, 10)
        test_set shape: (200, 10)
        """
        try:
            # Train/test split using sklearn
            train_set, test_set = train_test_split(
                dataframe, 
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42  # deterministic split
            )
            logging.info("Performed train-test split.")

            # Create directories for train/test if not exist
            train_dir = os.path.dirname(self.data_ingestion_config.training_file_path)
            test_dir = os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(train_dir, exist_ok=True)
            os.makedirs(test_dir, exist_ok=True)

            # Save train CSV
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            logging.info(f"Train CSV saved at: {self.data_ingestion_config.training_file_path}")

            # Save test CSV
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info(f"Test CSV saved at: {self.data_ingestion_config.testing_file_path}")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # -------------------------------
    # Step 4: Full pipeline initiation
    # -------------------------------
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Full pipeline:
        1. Fetch MongoDB data
        2. Save Feature Store CSV
        3. Split Train/Test CSVs
        4. Return paths in DataIngestionArtifact
        """
        try:
            logging.info("Starting data ingestion process...")

            # Step 1: Fetch data
            dataframe = self.export_collection_as_dataframe()

            # Step 2: Save feature store CSV
            dataframe = self.export_data_into_feature_store(dataframe)

            # Step 3: Split data
            self.split_data_as_train_test(dataframe)

            # Step 4: Create artifact object with train/test paths
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            logging.info("Data ingestion completed successfully.")
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
print("data ingestion completed")