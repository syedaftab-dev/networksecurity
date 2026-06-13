# ---------------------------------------------
# Import all required libraries and modules
# ---------------------------------------------
import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer  # Missing values fill karne ke liye
from sklearn.pipeline import Pipeline  # Transformation pipeline banane ke liye

# Project ke constants import karte hain
from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

# Artifact (output files ka structure define karte hain)
from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)

# Config file jahan paths aur directory info hoti hai
from networksecurity.entity.config_entity import DataTransformationConfig

# Custom exception aur logger
from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logging.logger import logging

# Helper functions to save numpy/object data
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object


# -----------------------------------------------------
# DataTransformation CLASS
# -----------------------------------------------------
class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        """
        Constructor me hum do cheeze lete hain:
        1. DataValidationArtifact -> valid train/test CSV paths deta hai
        2. DataTransformationConfig -> transformed data ke output paths deta hai
        """
        try:
            self.data_validation_artifact: DataValidationArtifact = data_validation_artifact
            self.data_transformation_config: DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # -----------------------------------------------------
    # Static method to read CSV data
    # -----------------------------------------------------
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        """
        Ye function CSV file ko pandas DataFrame me read karta hai.
        Example:
        Agar train.csv file me data hai:
        | f1 | f2 | label |
        |----|----|--------|
        | 10 | 20 | 1      |
        | 15 | na | 0      |

        To ye DataFrame return karega.
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # -----------------------------------------------------
    # Method to create Data Transformer (Preprocessor)
    # -----------------------------------------------------
    def get_data_transformer_object(cls) -> Pipeline:
        """
        Ye function ek sklearn Pipeline banata hai jisme KNNImputer hota hai
        - Missing values ko fill karne ke liye KNNImputer ka use hota hai.
        
        Example:
        Input data:
        [[1, 2],
         [3, NaN],
         [2, 1]]
        
        KNNImputer nearest values se NaN ko fill karega.
        """
        logging.info("Entered get_data_transformer_object method of DataTransformation class")

        try:
            # KNNImputer initialize karte hain project constants se
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialized KNNImputer with params: {DATA_TRANSFORMATION_IMPUTER_PARAMS}")

            # Pipeline me imputer add karte hain
            processor: Pipeline = Pipeline([("imputer", imputer)])
            return processor

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # -----------------------------------------------------
    # Main Method: Initiate Data Transformation
    # -----------------------------------------------------
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        Ye method full transformation pipeline run karta hai:
        1. Train/Test CSV load karna
        2. Target aur Input features alag karna
        3. Missing values fill karna using KNNImputer
        4. Transformed data save karna as .npy
        5. Preprocessor object save karna
        """
        logging.info("Entered initiate_data_transformation method of DataTransformation class")

        try:
            logging.info("Starting data transformation...")

            # Step 1: Read validated train/test CSV files
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            # Example:
            # train_df.head():
            # | duration | src_bytes | dst_bytes | label |
            # |----------|------------|-----------|--------|
            # | 12       | 1000       | 200       | 1      |
            # | 10       | na         | 500       | -1     |

            # Step 2: Separate input and target features (X and y)
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)
            # Example: agar label column [1, -1, -1, 1] tha -> ab [1, 0, 0, 1] ho gaya

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            # Step 3: Get Preprocessor (Pipeline with KNNImputer)
            preprocessor = self.get_data_transformer_object()

            # Fit on training data
            preprocessor_object = preprocessor.fit(input_feature_train_df)

            # Transform train and test data (missing values handled)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)

            # Example:
            # Before Imputation:
            # [[10, NaN, 1],
            #  [20, 30, 0]]
            # After Imputation:
            # [[10, 25, 1],
            #  [20, 30, 0]]

            # Step 4: Combine transformed X and y
            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]
            # Example:
            # X_train = [[1.2, 3.4], [5.6, 7.8]]
            # y_train = [0, 1]
            # np.c_ => [[1.2, 3.4, 0],
            #           [5.6, 7.8, 1]]

            # Step 5: Save transformed arrays as .npy files
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)

            # Step 6: Save the preprocessor object (so we can reuse during prediction)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)

            # Also save final copy in model folder for deployment
            save_object("final_model/preprocessor.pkl", preprocessor_object)

            # Step 7: Prepare final artifact (paths of saved files)
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            logging.info("Data transformation completed successfully ✅")
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
