import sys
import os
import certifi

from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME
from networksecurity.utils.ml_utils.model.estimator import NetworkModel #to handle SSL certificate verification issues
ca=certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url=os.getenv("MONGO_DB_URL")
print(mongo_db_url)
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import RedirectResponse, Response
from starlette.responses import JSONResponse
import pandas
from networksecurity.utils.main_utils.utils import load_object

client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
database=client[DATA_INGESTION_DATABASE_NAME]
collection=database[DATA_INGESTION_COLLECTION_NAME]
app=FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="networksecurity/templates")

@app.get("/",tags=['authentication'])
async def index():
    return RedirectResponse(url="/docs")

@app.post("/predict", tags=['prediction'])
async def predict_route(request:Request,file:UploadFile=File(...)):
    try:
        df=pandas.read_csv(file.file)
        preprocessor=load_object("final_model/preprocessor.pkl")
        final_model=load_object("final_model/model.pkl")
        network_model=NetworkModel(preprocessor=preprocessor,model=final_model)
        y_pred=network_model.predict(df)
        print(y_pred)
        df['predicted_column']=y_pred
        # print(df['predicted_column'])
        # optional: save inside the app folder
        output_path = os.path.join("networksecurity", "prediction_output", "prediction.csv")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)

        table_html=df.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html",{"request":request,"table":table_html})
    except Exception as e:
        raise NetworkSecurityException(e,sys)

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()   
        train_pipeline.run_pipeline()
        return Response(content="Training successful!!")
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)  
if __name__ == '__main__':
    port = int(os.getenv("PORT", 8000))  # get PORT from environment, default to 8000 if not set
    app_run(app, host="0.0.0.0", port=port)