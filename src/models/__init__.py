import os

from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql

# Lee src/.env (en el computador). En Render las variables se configuran en el panel.
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

# Cadena de conexión: se toma de la variable DATABASE_URL.
# Si no existe, se usa el MySQL local de XAMPP.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root@localhost:3306/woodart_PY?charset=utf8mb4",
)

# Las bases en la nube (por ejemplo Aiven) exigen conexión cifrada (SSL).
connect_args = {}
if os.getenv("DB_SSL", "").lower() in ("1", "true", "si", "sí") or "aivencloud.com" in DATABASE_URL:
    connect_args["ssl"] = {"check_hostname": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,   # descarta conexiones que el servidor cerró
    pool_recycle=280,     # renueva las conexiones antes de que caduquen
)

Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()
Base.metadata.bind = engine
