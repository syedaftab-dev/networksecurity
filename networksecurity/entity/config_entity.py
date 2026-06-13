# ---------------------- config.py ----------------------
# Ye file project ke sabhi configurations (paths & directories) define karti hai.
# Har stage of ML pipeline (ingestion, validation, transformation, etc.) ke liye
# yahan ek config class hoti hai jo batati hai:
# "is phase ka data kaha se aayega aur kaha save hoga?"

from datetime import datetime     # Timestamp generate karne ke liye
import os                         # File/folder path operations ke liye
from networksecurity.constant import training_pipeline  # Sab constants import kar rahe hain

# Just to verify constants work sahi se import ho rahe hain
print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFACT_DIR)


# -------------------------------------------------------
# 🔹 CLASS 1: TrainingPipelineConfig
# -------------------------------------------------------
class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        # Example: current time = 9th Oct 2025, 10:25:15 PM
        # So formatted timestamp = "10_09_2025_22_25_15"
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")

        # Ye constant define karta hai pipeline ka naam
        # Example: PIPELINE_NAME = "networksecurity"
        self.pipeline_name = training_pipeline.PIPELINE_NAME

        # ARTIFACT_DIR constant = "artifacts"
        # Har run ke liye alag folder create hoga inside "artifacts"
        self.artifact_name = training_pipeline.ARTIFACT_DIR

        # Final artifact directory with timestamp
        # Example output: artifacts/10_09_2025_22_25_15
        self.artifact_dir = os.path.join(self.artifact_name, timestamp)

        # Final trained model yahan save hota hai
        # Example: final_model/model.pkl
        self.model_dir = os.path.join("final_model")

        # Reference ke liye timestamp variable store kar liya
        self.timestamp: str = timestamp


# -------------------------------------------------------
# 🔹 CLASS 2: DataIngestionConfig
# -------------------------------------------------------
class DataIngestionConfig:
    """
    Ye class handle karti hai Data Ingestion phase ke sab path aur parameters.
    Yani kaha se raw data read karna hai, aur kaha par train/test data save karna hai.
    """

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        # Example: artifacts/10_09_2025_22_25_15/data_ingestion
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME
        )

        # Raw data (feature store) save hone ka path
        # Example: artifacts/10_09_2025_22_25_15/data_ingestion/feature_store/network_data.csv
        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
            training_pipeline.FILE_NAME
        )

        # Training file path (split hone ke baad)
        # Example: artifacts/.../data_ingestion/ingested/train.csv
        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME
        )

        # Testing file path (split hone ke baad)
        # Example: artifacts/.../data_ingestion/ingested/test.csv
        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME
        )

        # Train-test split ratio (usually 0.2 → 80/20)
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION

        # MongoDB details
        # Example: database_name="network_security_db", collection_name="sensor_data"
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME


# -------------------------------------------------------
# 🔹 CLASS 3: DataValidationConfig
# -------------------------------------------------------
class DataValidationConfig:
    """
    Ye class data validation phase ke paths define karti hai:
    valid aur invalid data kaha save karna hai, aur drift report ka location.
    """

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        # Example: artifacts/.../data_validation
        self.data_validation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_VALIDATION_DIR_NAME
        )

        # Folder for valid data (jisme schema ke hisaab se correct files save hongi)
        # Example: artifacts/.../data_validation/valid
        self.valid_data_dir: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_VALID_DIR
        )

        # Folder for invalid data (jisme incorrect data save hoga)
        # Example: artifacts/.../data_validation/invalid
        self.invalid_data_dir: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_INVALID_DIR
        )

        # Valid aur invalid train/test file paths
        self.valid_train_file_path: str = os.path.join(
            self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME
        )
        self.valid_test_file_path: str = os.path.join(
            self.valid_data_dir, training_pipeline.TEST_FILE_NAME
        )
        self.invalid_train_file_path: str = os.path.join(
            self.invalid_data_dir, training_pipeline.TRAIN_FILE_NAME
        )
        self.invalid_test_file_path: str = os.path.join(
            self.invalid_data_dir, training_pipeline.TEST_FILE_NAME
        )

        # Drift report ka path — ye data drift detect karta hai (old vs new data)
        # Example: artifacts/.../data_validation/drift_report/report.yaml
        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
        )

# data transformation config
# --------------------------------------------------------
# Data Transformation Config Class
# --------------------------------------------------------

class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        """
        Ye constructor data transformation ke liye zaruri file/folder ke paths banata hai.
        training_pipeline_config : ye ek object hai jisme artifact folder ka main path hota hai.
        Example:
            training_pipeline_config.artifact_dir = "artifact"
        """
        # --------------------------------------------------------
        # Step 1: Create base directory for data transformation
        # --------------------------------------------------------
        # Example:
        # agar artifact_dir = "artifact"
        # aur DATA_TRANSFORMATION_DIR_NAME = "data_transformation"
        # to final path hoga: "artifact/data_transformation"
        # --------------------------------------------------------
        self.data_transformation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_TRANSFORMATION_DIR_NAME
        )
        # --------------------------------------------------------
        # Step 2: Transformed Train Data Path
        # --------------------------------------------------------
        # Train CSV ko transform karke .npy (NumPy array format) me store karte hain.
        # Example:
        # artifact/data_transformation/transformed_data/train.npy
        # --------------------------------------------------------
        self.transformed_train_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"),  # "train.csv" → "train.npy"
        )
        # --------------------------------------------------------
        # Step 3: Transformed Test Data Path
        # --------------------------------------------------------
        # Similarly, test.csv ko transform karke .npy format me save karte hain.
        # Example:
        # artifact/data_transformation/transformed_data/test.npy
        # --------------------------------------------------------
        self.transformed_test_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TEST_FILE_NAME.replace("csv", "npy"),
        )
        # --------------------------------------------------------
        # Step 4: Transformed Object File Path
        # --------------------------------------------------------
        # Ye path store karta hai preprocessing object (Scaler, Encoder etc.)
        # Example:
        # artifact/data_transformation/preprocessing/preprocessor.pkl
        # --------------------------------------------------------
        self.transformed_object_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            training_pipeline.PREPROCESSING_OBJECT_FILE_NAME,
        )
class ModelTrainerConfig:
    def  __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir:str = os.path.join(
            training_pipeline_config.artifact_dir,training_pipeline.MODEL_TRAINER_DIR_NAME
        )
        self.trained_model_file_path:str=os.path.join(
            self.model_trainer_dir,training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,training_pipeline.MODEL_FILE_NAME

        )
        self.expected_accuracy:float=training_pipeline.MODEL_TRAINER_EXPECTED_SCORE 
        self.overfitting_underfitting_threshold=training_pipeline.MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD
        