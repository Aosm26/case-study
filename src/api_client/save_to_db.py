from typing import List, Dict, Any
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from src.models.campground_db import CampgroundDB
from ..utils.logger import setup_logger
from ..utils.exceptions import DatabaseError

# Logger'ı başlat
logger = setup_logger(__name__, "database.log")

def json_to_campground_db(item: Dict[str, Any]) -> CampgroundDB:
    """
    JSON verisini CampgroundDB nesnesine dönüştürür.
    
    Args:
        item: Kamp alanı JSON verisi
        
    Returns:
        CampgroundDB: Veritabanı modeli nesnesi
    """
    try:
        attrs = item.get("attributes", {})
        return CampgroundDB(
            id=item.get("id"),
            type=item.get("type"),
            name=attrs.get("name"),
            latitude=attrs.get("latitude"),
            longitude=attrs.get("longitude"),
            region_name=attrs.get("region-name"),
            administrative_area=attrs.get("administrative-area"),
            nearest_city_name=attrs.get("nearest-city-name"),
            bookable=attrs.get("bookable"),
            operator=attrs.get("operator"),
            photos_count=attrs.get("photos-count"),
            rating=attrs.get("rating"),
            reviews_count=attrs.get("reviews-count"),
            slug=attrs.get("slug"),
            price_low=attrs.get("price-low"),
            price_high=attrs.get("price-high"),
            availability_updated_at=attrs.get("availability-updated-at"),
            address=attrs.get("address"),
        )
    except Exception as e:
        error_msg = f"Veri dönüştürme hatası: {str(e)}"
        logger.error(error_msg)
        raise DatabaseError(error_msg) from e

def save_campgrounds_to_db(all_data: List[Dict[str, Any]], db_url: str = "postgresql://user:password@localhost:5433/case_study") -> None:
    """
    Kamp alanı verilerini veritabanına kaydeder.
    
    Args:
        all_data: Kaydedilecek kamp alanı verilerinin listesi
        db_url: Veritabanı bağlantı URL'i
        
    Raises:
        DatabaseError: Veritabanı işlemi başarısız olduğunda
        ValueError: Geçersiz parametre değerleri verildiğinde
    """
    if not isinstance(all_data, list):
        error_msg = "all_data parametresi liste olmalıdır"
        logger.error(error_msg)
        raise ValueError(error_msg)
        
    if not all_data:
        logger.warning("Kaydedilecek veri bulunamadı")
        return

    logger.info(f"Veritabanına kayıt başlıyor: {len(all_data)} kamp alanı")
    session = None
    
    try:
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        success_count = 0
        error_count = 0
        
        for i, item in enumerate(all_data, 1):
            try:
                obj = json_to_campground_db(item)
                session.merge(obj)  # varsa günceller, yoksa ekler
                success_count += 1
                
                if i % 100 == 0:  # Her 100 kayıtta bir commit
                    session.commit()
                    logger.info(f"İlerleme: {i}/{len(all_data)} ({success_count} başarılı, {error_count} hata)")
                    
            except Exception as e:
                error_count += 1
                logger.error(f"Kayıt hatası (ID: {item.get('id')}): {str(e)}")
                continue
        
        session.commit()
        logger.info(f"Veritabanına kayıt tamamlandı: {success_count} başarılı, {error_count} hata")
        
    except SQLAlchemyError as e:
        error_msg = f"Veritabanı hatası: {str(e)}"
        logger.error(error_msg)
        if session:
            session.rollback()
        raise DatabaseError(error_msg) from e
    except Exception as e:
        error_msg = f"Beklenmeyen hata: {str(e)}"
        logger.error(error_msg)
        if session:
            session.rollback()
        raise DatabaseError(error_msg) from e
    finally:
        if session:
            session.close() 