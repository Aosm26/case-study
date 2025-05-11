import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .campground_db import CampgroundDB

def create_tables():
    try:
        engine = create_engine("postgresql://user:password@localhost:5433/case_study")
        Base.metadata.create_all(engine)
        logging.info("Tablolar başarıyla oluşturuldu.")
        print("Tablolar oluşturuldu.")
    except Exception as e:
        logging.error(f"Tablolar oluşturulurken hata oluştu: {e}")
        print(f"Hata oluştu: {e}")

# main.py çalışınca otomatik çalışsın istiyorsan:
create_tables()
