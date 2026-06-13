cd e:\Projects\nwtwork\networksecurity

git rm -r --cached . | Out-Null

function Commit-If-Changes ($msg) {
    if (git diff --cached --quiet) {
        Write-Host "No changes for: $msg"
    } else {
        git commit -m "$msg"
    }
}

git add requirements.txt setup.py .gitignore README.md Dockerfile
Commit-If-Changes "Initialize project setup and requirements"

git add networksecurity/logging/
Commit-If-Changes "Add custom logging framework"

git add networksecurity/exception/
Commit-If-Changes "Implement custom exception handling"

git add networksecurity/constant/
Commit-If-Changes "Define project constants"

git add networksecurity/entity/
Commit-If-Changes "Add configuration and artifact entities"

git add networksecurity/cloud/
Commit-If-Changes "Implement cloud syncing functionality"

git add networksecurity/utils/main_utils/
Commit-If-Changes "Add main utility functions"

git add networksecurity/utils/ml_utils/
Commit-If-Changes "Add ML utility functions and metrics"

git add networksecurity/components/data_ingestion.py networksecurity/components/__init__.py
Commit-If-Changes "Develop Data Ingestion component"

git add networksecurity/components/data_validation.py
Commit-If-Changes "Develop Data Validation component"

git add networksecurity/components/data_transformation.py
Commit-If-Changes "Develop Data Transformation component"

git add networksecurity/components/model_trainer.py
Commit-If-Changes "Develop Model Trainer component"

git add networksecurity/pipeline/training_pipeline.py networksecurity/pipeline/__init__.py
Commit-If-Changes "Implement Training Pipeline"

git add networksecurity/pipeline/batch_pipeline.py
Commit-If-Changes "Implement Batch Prediction Pipeline"

git add push_data.py networksecurity/valid_data/
Commit-If-Changes "Add script for pushing data and test data"

git add networksecurity/templates/ networksecurity/prediction_output/
Commit-If-Changes "Add HTML templates and prediction output directory"

git add main.py networksecurity/__init__.py
Commit-If-Changes "Create main FastAPI application"

git add logs/ networksecurity/logs/
Commit-If-Changes "Add logging directories"

git add networksecurity/*__pycache__*
Commit-If-Changes "Add pycache files"

git add -A
Commit-If-Changes "Final project adjustments and cleanup"

git push -f origin main
