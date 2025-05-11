from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
from .fetch_campgrounds import fetch_campgrounds
from ..utils.logger import setup_logger
from ..utils.exceptions import APIError

# Logger'ı başlat
logger = setup_logger(__name__, "campgrounds.log")

def fetch_campgrounds_threaded(page_start: int = 1, page_end: int = 355, size: int = 10, max_workers: int = 5) -> List[Dict[str, Any]]:
    """
    Threading ile birden fazla sayfadan kamp alanı verilerini çeker.
    
    Args:
        page_start: Başlangıç sayfa numarası
        page_end: Bitiş sayfa numarası
        size: Her sayfada çekilecek veri sayısı
        max_workers: Maksimum thread sayısı
        
    Returns:
        List[Dict[str, Any]]: Kamp alanı verilerinin listesi
        
    Raises:
        APIError: API çağrısı başarısız olduğunda
        ValueError: Geçersiz parametre değerleri verildiğinde
    """
    if page_start < 1 or page_end < page_start:
        error_msg = f"Geçersiz sayfa aralığı: {page_start}-{page_end}"
        logger.error(error_msg)
        raise ValueError(error_msg)
        
    if size < 1:
        error_msg = f"Geçersiz sayfa boyutu: {size}"
        logger.error(error_msg)
        raise ValueError(error_msg)
        
    if max_workers < 1:
        error_msg = f"Geçersiz worker sayısı: {max_workers}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.info(f"Kamp alanı verileri çekiliyor: sayfa {page_start}-{page_end}, boyut: {size}, worker: {max_workers}")
    results = []
    failed_pages = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_page = {
            executor.submit(fetch_campgrounds, page, size): page
            for page in range(page_start, page_end + 1)
        }
        
        for future in as_completed(future_to_page):
            page = future_to_page[future]
            try:
                data = future.result()
                results.extend(data)
                logger.debug(f"Sayfa {page} başarıyla çekildi: {len(data)} veri")
            except Exception as exc:
                error_msg = f"Sayfa {page} çekilirken hata oluştu: {str(exc)}"
                logger.error(error_msg)
                failed_pages.append(page)
                raise APIError(error_msg) from exc
    
    if failed_pages:
        logger.warning(f"Başarısız olan sayfalar: {failed_pages}")
    
    logger.info(f"Toplam {len(results)} kamp alanı verisi çekildi")
    return results 