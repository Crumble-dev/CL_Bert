import boto3
import pandas as pd
from io import StringIO
from sqlalchemy.orm import Session
from app.models import CoupleWellbeingTrend
from app.database import SessionLocal
import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno del .env

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")

# Inicializa la sesión de boto3 correctamente
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
    region_name=AWS_DEFAULT_REGION
)
s3 = session.client("s3")

def load_csv_from_s3(bucket: str = S3_BUCKET, key: str = "training_dataset.csv"):
    print("Descargando archivo de S3...")
    response = s3.get_object(Bucket=bucket, Key=key)
    print("Archivo descargado, leyendo contenido...")
    content = response['Body'].read().decode('utf-8')
    print("Leyendo CSV con pandas...")
    df = pd.read_csv(StringIO(content))
    print(f"CSV leído: {len(df)} filas")
    return df

def save_to_db(df: pd.DataFrame):
    db: Session = SessionLocal()
    try:
        print("Guardando en base de datos...")
        records = []
        for _, row in df.iterrows():
            record = CoupleWellbeingTrend(
                couple_id=row['couple_id'],
                week_number=row['week_number'],
                puntuacion_cuestionario_das=row['puntuacion_cuestionario_das'],
                calificacion_satisfaccion_tareas_avg=row['calificacion_satisfaccion_tareas_avg'],
                tasa_cumplimiento_tareas=row['tasa_cumplimiento_tareas'],
                promedio_estres_individual=row['promedio_estres_individual'],
                interacion_balance_ratio=row['interacion_balance_ratio'],
                empatia_gap_score=row['empatia_gap_score'],
                comunicacion_health_score=row['comunicacion_health_score'],
                churn_risk=row['churn_risk'],
                embedding_0=row['embedding_descripcion_interaccion_0'],
                embedding_1=row['embedding_descripcion_interaccion_1'],
                embedding_2=row['embedding_descripcion_interaccion_2'],
                embedding_3=row['embedding_descripcion_interaccion_3'],
                embedding_4=row['embedding_descripcion_interaccion_4'],
                embedding_5=row['embedding_descripcion_interaccion_5'],
                embedding_6=row['embedding_descripcion_interaccion_6'],
                embedding_7=row['embedding_descripcion_interaccion_7'],
                embedding_8=row['embedding_descripcion_interaccion_8'],
                embedding_9=row['embedding_descripcion_interaccion_9'],
                embedding_10=row['embedding_descripcion_interaccion_10'],
            )
            records.append(record)
        db.bulk_save_objects(records)
        db.commit()
        print("Datos guardados exitosamente.")
    finally:
        db.close()
