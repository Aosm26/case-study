import requests
import time
from typing import List, Dict, Any
from ..utils.logger import setup_logger
from ..utils.exceptions import GeocodingError

# Logger'ı başlat
logger = setup_logger(__name__, "geocoding.log")

def fetch_address_for_campgrounds(campgrounds: List[Dict[str, Any]], count: int = 50, max_workers: int = 5) -> List[Dict[str, Any]]:
    """
    Kamp alanları için adres bilgilerini çeker.
    
    Args:
        campgrounds: Kamp alanı verilerinin listesi
        count: İşlenecek maksimum kamp alanı sayısı
        max_workers: Maksimum thread sayısı (şu an kullanılmıyor)
        
    Returns:
        List[Dict[str, Any]]: Adres bilgileri eklenmiş kamp alanı verileri
        
    Raises:
        GeocodingError: Adres çözümleme başarısız olduğunda
        ValueError: Geçersiz parametre değerleri verildiğinde
    """
        
    if count < 1:
        error_msg = f"Geçersiz count değeri: {count}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    def get_address(camp: Dict[str, Any]) -> str:
        """
        Tek bir kamp alanı için adres bilgisini çeker.
        
        Args:
            camp: Kamp alanı verisi
            
        Returns:
            str: Adres bilgisi veya None
            
        Raises:
            GeocodingError: Adres çözümleme başarısız olduğunda
        """
        try:
            lat = camp.get("attributes", {}).get("latitude")
            lon = camp.get("attributes", {}).get("longitude")
            
            if lat is None or lon is None:
                logger.warning(f"Koordinat bilgisi eksik: lat={lat}, lon={lon}")
                return None
                
            url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
            logger.debug(f"Adres çözümleme isteği: {url}")
            
            response = requests.get(
                url,
                headers={"User-Agent": "CampgroundGeocoder/1.0"},
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            address = data.get("display_name")
            
            if not address:
                logger.warning(f"Adres bulunamadı: lat={lat}, lon={lon}")
                return None
                
            logger.debug(f"Adres başarıyla çözümlendi: {address}")
            return address
            
        except requests.RequestException as e:
            error_msg = f"Adres çözümleme hatası: {str(e)}"
            logger.error(error_msg)
            raise GeocodingError(error_msg) from e
        except Exception as e:
            error_msg = f"Beklenmeyen hata: {str(e)}"
            logger.error(error_msg)
            raise GeocodingError(error_msg) from e

    logger.info(f"Adres çözümleme başlıyor: {count} kamp alanı için")
    processed_count = 0
    error_count = 0

    for i, camp in enumerate(campgrounds[:count]):
        try:
            address = get_address(camp)
            camp["attributes"]["address"] = address
            processed_count += 1
            logger.info(f"İlerleme: {i+1}/{count} ({processed_count} başarılı, {error_count} hata)")
            time.sleep(1)  # Rate limit için bekleme
        except GeocodingError as e:
            error_count += 1
            logger.error(f"Kamp alanı {i+1} için hata: {str(e)}")
            camp["attributes"]["address"] = None
            continue

    logger.info(f"Adres çözümleme tamamlandı: {processed_count} başarılı, {error_count} hata")
    return campgrounds 