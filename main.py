from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
import sys

def start_training_pipeline():
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info(f"Data Ingestion completed successfully. Artifact: {dataingestionartifact}")

    except Exception as e:
        logging.error(f"An unhandled exception occurred: {e}")
        raise NetworkSecurityException(e, sys)

if __name__=="__main__":
    start_training_pipeline()
