"""
Main entrypoint for The Dyrt web scraper case study.

Usage:
    The scraper can be run directly (`python main.py`) or via Docker Compose (`docker compose up`).

If you have any questions in mind you can connect to me directly via info@smart-maple.com
"""

import sys
import argparse
from src.utils.logger import setup_logger
from src.utils.exceptions import APIError, DatabaseError, GeocodingError
from src.api_client.fetch_campgrounds_threaded import fetch_campgrounds_threaded
from src.api_client.geocode_addresses import fetch_address_for_campgrounds
from src.api_client.save_to_db import save_campgrounds_to_db
from src.scheduler.task_scheduler import TaskScheduler

# Ana logger'ı başlat
logger = setup_logger("main", "main.log")

def run_once():
    """
    Veri çekme işlemini bir kez çalıştırır.
    """
    try:
        logger.info("Uygulama başlatılıyor...")
        
        # Kamp alanı verilerini çek
        logger.info("Kamp alanı verileri çekiliyor...")
        all_data = fetch_campgrounds_threaded(page_start=1, page_end=36, size=100, max_workers=10)
        logger.info(f"Toplam {len(all_data)} kamp alanı verisi çekildi")
        
        # Adres bilgilerini çek
        logger.info("Adres bilgileri çekiliyor...")
        all_data = fetch_address_for_campgrounds(all_data, count=1, max_workers=5)
        # count = 1 çünkü tümünü çekmek istediğimde api kısıtlıyor dolayısıyla 1 yaptım
        
        # Veritabanına kaydet
        logger.info("Veriler veritabanına kaydediliyor...")
        save_campgrounds_to_db(all_data)
        
        logger.info("Uygulama başarıyla tamamlandı")
        
    except APIError as e:
        logger.error(f"API hatası: {str(e)}")
        sys.exit(1)
    except GeocodingError as e:
        logger.error(f"Adres çözümleme hatası: {str(e)}")
        sys.exit(1)
    except DatabaseError as e:
        logger.error(f"Veritabanı hatası: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {str(e)}")
        sys.exit(1)

def run_scheduled(interval_hours: int = 24):
    """
    Zamanlanmış görevleri başlatır.
    
    Args:
        interval_hours: Görevlerin tekrarlanma süresi (saat)
    """
    try:
        logger.info("Zamanlanmış görevler başlatılıyor...")
        scheduler = TaskScheduler()
        scheduler.start(interval_hours)
        
        # Ana thread'i canlı tut
        while True:
            try:
                input("Çıkmak için Ctrl+C'ye basın...\n")
            except KeyboardInterrupt:
                logger.info("Kullanıcı tarafından durduruldu")
                scheduler.stop()
                break
                
    except Exception as e:
        logger.error(f"Zamanlanmış görev hatası: {str(e)}")
        sys.exit(1)

def main():
    """
    Ana uygulama akışı.
    """
    parser = argparse.ArgumentParser(description="The Dyrt web scraper")
    parser.add_argument(
        "-s", "--schedule",
        action="store_true",
        help="Zamanlanmış görevleri başlat"
    )
    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=24,
        help="Görevlerin tekrarlanma süresi (saat)"
    )
    
    args = parser.parse_args()
    
    if args.schedule:
        run_scheduled(args.interval)
    else:
        run_once()

if __name__ == "__main__":
    main()