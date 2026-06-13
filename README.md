# 🛡️ Network Security ML Pipeline

An end-to-end Machine Learning pipeline for detecting **phishing websites** using supervised learning techniques and production-style MLOps practices.

The project follows a modular architecture consisting of data ingestion, validation, transformation, model training, and prediction pipelines. It is designed to demonstrate how Machine Learning systems are developed in a scalable and maintainable way beyond notebooks.

---

## 📌 Problem Statement

Phishing websites imitate legitimate websites to steal sensitive user information such as passwords, banking credentials, and personal data.

The goal of this project is to:

* Analyze website-related features.
* Train Machine Learning models to classify websites.
* Predict whether a website is **Phishing** or **Legitimate**.
* Build a reusable and production-oriented ML pipeline.

---

# 🚀 Features

* End-to-End ML Pipeline
* Modular Project Architecture
* Data Ingestion Pipeline
* Data Validation
* Data Drift Detection
* Data Transformation Pipeline
* Multiple Model Training
* Model Evaluation and Selection
* Batch Prediction Pipeline
* Docker Support
* Artifact Management

---

# 🏗️ Project Architecture

```text
                 Raw Dataset
                      │
                      ▼
             Data Ingestion
                      │
                      ▼
             Data Validation
          ┌─────────────────┐
          │ Schema Check    │
          │ Missing Values  │
          │ Data Drift      │
          └─────────────────┘
                      │
                      ▼
          Data Transformation
          ┌─────────────────┐
          │ Feature Scaling │
          │ Preprocessing   │
          └─────────────────┘
                      │
                      ▼
              Model Training
          ┌─────────────────┐
          │ Logistic Reg.   │
          │ KNN             │
          │ Decision Tree   │
          │ Random Forest   │
          │ AdaBoost        │
          │ Gradient Boost  │
          └─────────────────┘
                      │
                      ▼
             Best Model Saved
                      │
                      ▼
             Batch Prediction
```

---

# 📂 Project Structure

```bash
networksecurity/

├── Artifacts/
│   ├── data_ingestion/
│   ├── data_validation/
│   ├── data_transformation/
│   └── model_trainer/
│
├── Network_Data/
│   └── phisingData.csv
│
├── networksecurity/
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   │
│   ├── pipeline/
│   │   ├── training_pipeline.py
│   │   └── batch_prediction.py
│   │
│   ├── entity/
│   ├── configuration/
│   ├── exception/
│   ├── logger/
│   └── utils/
│
├── Dockerfile
├── requirements.txt
├── main.py
└── README.md
```

---

# 📊 Dataset

The dataset contains various features extracted from website URLs and webpage properties that help distinguish phishing websites from legitimate ones.

Examples of features:

* URL Length
* Having IP Address
* Prefix/Suffix usage
* HTTPS Token
* Domain Registration Length
* Request URL
* DNS Record
* Website Traffic
* Page Rank
* Age of Domain

### Target Variable

| Label | Meaning            |
| ----- | ------------------ |
| 1     | Legitimate Website |
| -1    | Phishing Website   |

---

# 🔍 Data Validation

The validation pipeline performs:

### Schema Validation

Checks:

* Missing columns
* Unexpected columns
* Datatype mismatches

### Data Drift Detection

Detects distribution shifts between:

* Training Dataset
* Incoming Dataset

This ensures the model remains reliable when new data distributions appear.

---

# ⚙️ Data Transformation

The transformation stage performs:

* Feature preprocessing
* Feature scaling
* Pipeline serialization
* Artifact generation

Generated artifacts:

```bash
preprocessing.pkl
```

This preprocessing object is reused during prediction to maintain consistency.

---

# 🤖 Models Used

The project trains and compares multiple Machine Learning algorithms:

| Model               |
| ------------------- |
| Logistic Regression |
| K Nearest Neighbors |
| Decision Tree       |
| Random Forest       |
| AdaBoost            |
| Gradient Boosting   |

The best model is automatically selected based on evaluation metrics.

---

# 📈 Evaluation

The models are evaluated using:

* Accuracy Score
* Precision
* Recall
* F1 Score

The highest-performing model is saved as:

```bash
model.pkl
```

for future predictions.

---

# 🐳 Docker Support

The application is containerized using Docker.

Build image:

```bash
docker build -t network-security .
```

Run container:

```bash
docker run -p 5000:5000 network-security
```

---

# 🛠️ Installation

Clone repository

```bash
git clone https://github.com/syedaftab-dev/networksecurity.git

cd networksecurity
```

Create virtual environment

```bash
python -m venv venv
```

Activate environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the training pipeline

```bash
python main.py
```

---

# 💡 Future Improvements

* Deploy using FastAPI
* Real-time URL prediction API
* Model Monitoring
* Experiment Tracking with MLflow
* CI/CD Pipeline
* Cloud Deployment on AWS

---

# 👨‍💻 Author

**Syed Aftab**

B.Tech CSE
IIITDM Kurnool

* GitHub: https://github.com/syedaftab-dev
* LinkedIn: https://www.linkedin.com/in/syed-aftab-797130345/

---

⭐ If you found this project useful, consider giving it a star.
