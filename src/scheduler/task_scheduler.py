import schedule
import time
import threading
from typing import Optional
from ..utils.logger import setup_logger
from ..api_client.fetch_campgrounds_threaded import fetch_campgrounds_threaded
from ..api_client.geocode_addresses import fetch_address_for_campgrounds
from ..api_client.save_to_db import save_campgrounds_to_db

# Logger'ı başlat
logger = setup_logger(__name__, "scheduler.log")

class TaskScheduler:
    """
    Zamanlanmış görevleri yöneten sınıf.
    """
    def __init__(self):
        self._scheduler_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        
    def update_campgrounds(self):
        """
        Kamp alanı verilerini güncelleyen görev.
        """
        try:
            logger.info("Zamanlanmış görev başlatılıyor: Kamp alanı güncelleme")
            
            # Kamp alanı verilerini çek
            all_data = fetch_campgrounds_threaded(
                page_start=1,
                page_end=36,
                size=100,
                max_workers=10
            )
            logger.info(f"Toplam {len(all_data)} kamp alanı verisi çekildi")
            
            # Adres bilgilerini çek
            all_data = fetch_address_for_campgrounds(
                all_data,
                count=50,
                max_workers=5
            )
            
            # Veritabanına kaydet
            save_campgrounds_to_db(all_data)
            
            logger.info("Zamanlanmış görev başarıyla tamamlandı")
            
        except Exception as e:
            logger.error(f"Zamanlanmış görev hatası: {str(e)}")
    
    def _run_scheduler(self):
        """
        Zamanlanmış görevleri çalıştıran thread fonksiyonu.
        """
        while not self._stop_event.is_set():
            schedule.run_pending()
            time.sleep(1)
    
    def start(self, interval_hours: int = 24):
        """
        Zamanlanmış görevleri başlatır.
        
        Args:
            interval_hours: Görevlerin tekrarlanma süresi (saat)
        """
        if self._scheduler_thread and self._scheduler_thread.is_alive():
            logger.warning("Zamanlanmış görevler zaten çalışıyor")
            return
            
        # Görevi zamanla
        schedule.every(interval_hours).hours.do(self.update_campgrounds)
        
        # İlk çalıştırma
        self.update_campgrounds()
        
        # Scheduler thread'ini başlat
        self._stop_event.clear()
        self._scheduler_thread = threading.Thread(target=self._run_scheduler)
        self._scheduler_thread.daemon = True
        self._scheduler_thread.start()
        
        logger.info(f"Zamanlanmış görevler başlatıldı (her {interval_hours} saatte bir)")
    
    def stop(self):
        """
        Zamanlanmış görevleri durdurur.
        """
        if not self._scheduler_thread or not self._scheduler_thread.is_alive():
            logger.warning("Zamanlanmış görevler zaten durmuş durumda")
            return
            
        self._stop_event.set()
        self._scheduler_thread.join()
        schedule.clear()
        
        logger.info("Zamanlanmış görevler durduruldu") 