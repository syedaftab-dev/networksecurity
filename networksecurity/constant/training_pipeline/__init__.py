import os
import sys
import numpy as np
import pandas as pd

"""definingcommon constant variables for training pippeline


"""
TARGET_COLUMN="Result"
PIPELINE_NAME:str = "networkwecurity"
ARTIFACT_DIR:str="Artifacts"
FILE_NAME:str="phisingData.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"

"""
Data ingestion related constant start with DATA_INGESTION VAR NAME


"""

DATA_INGESTION_COLLECTION_NAME: str ="networkML"
DATA_INGESTION_DATABASE_NAME:str="networksecurity"
DATA_INGESTION_DIR_NAME: str ="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float=0.2


"""
Data validation related constsnt start with DATA_VALIDATION VAR NAME

"""

DATA_VALIDATION_DIR_NAME: str= "data_validation"
DATA_VALIDATION_VALID_DIR:str="validated"
DATA_VALIDATION_INVALID_DIR:str="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str="report.yaml"
