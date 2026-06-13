# -------------------------------
# Import required modules
# -------------------------------
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact  # Artifacts
from networksecurity.entity.config_entity import DataValidationConfig  # Config paths, drift report path
from networksecurity.exception.exception import NetworkSecurityException  # Custom exceptions
from networksecurity.logging.logger import logging  # Logger
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH  # Schema YAML path
from scipy.stats import ks_2samp  # For dataset drift detection
import pandas as pd
import os, sys
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file  # YAML utils

# -------------------------------
# Data Validation Class
# -------------------------------
class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        """
        Constructor: store artifacts from ingestion & validation config
        Example:
        data_ingestion_artifact.trained_file_path = "artifact/train/train.csv"
        data_ingestion_artifact.test_file_path = "artifact/test/test.csv"
        data_validation_config.drift_report_file_path = "artifact/drift/drift_report.yaml"
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact  # Store train/test paths
            self.data_validation_config = data_validation_config  # Store config paths
            # Load schema from YAML file, example: {"feature1": "int", "feature2": "float", "label": "int"}
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # -------------------------------
    # Read CSV file
    # -------------------------------
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        """
        Read CSV as DataFrame
        Example:
        file_path = "artifact/train/train.csv"
        Returns: pd.DataFrame with shape (1000, 10)
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # -------------------------------
    # Validate number of columns
    # -------------------------------
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        """
        Check if dataframe has expected number of columns
        Example:
        schema_config has 10 columns
        train dataframe has 10 columns → True
        test dataframe has 9 columns → False
        """
        try:
            number_of_columns = len(self._schema_config)  # Expected columns
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # -------------------------------
    # Detect dataset drift using KS test
    # -------------------------------
    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        """
        Compare train vs test distributions column-wise using KS test
        Example:
        base_df: train dataframe
        current_df: test dataframe
        For column "feature1", KS test p-value = 0.1 → no drift
        For column "feature2", KS test p-value = 0.01 → drift detected
        Drift report saved as YAML
        """
        try:
            status = True  # Overall drift status
            report = {}  # Store drift info per column

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]

                # KS 2-sample test
                is_same_dist = ks_2samp(d1, d2)

                # If p-value < threshold → drift found
                if threshold <= is_same_dist.pvalue:
                    is_found = False  # No drift
                else:
                    is_found = True  # Drift detected
                    status = False

                # Update report
                report.update({column: {
                    "p_value": float(is_same_dist.pvalue),
                    "drift_status": is_found
                }})

            # Save drift report YAML
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)

            return status  # True if no drift, False if any drift detected

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # -------------------------------
    # Initiate full validation
    # -------------------------------
    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Full pipeline:
        1. Read train/test CSVs
        2. Validate columns
        3. Check dataset drift
        4. Save valid CSVs
        5. Return DataValidationArtifact
        """
        try:
            # Step 1: Get file paths from ingestion artifact
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Step 2: Read CSVs
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            # Step 3: Validate number of columns
            status_train = self.validate_number_of_columns(train_dataframe)
            if not status_train:
                logging.error("Train dataframe does not contain all required columns")

            status_test = self.validate_number_of_columns(test_dataframe)
            if not status_test:
                logging.error("Test dataframe does not contain all required columns")

            # Step 4: Detect dataset drift
            status_drift = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)

            # Step 5: Save valid train/test CSVs
            os.makedirs(os.path.dirname(self.data_validation_config.valid_train_file_path), exist_ok=True)
            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

            # Step 6: Create artifact with validation status and paths
            data_validation_artifact = DataValidationArtifact(
                validation_status=status_drift,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
print("data validation completed")