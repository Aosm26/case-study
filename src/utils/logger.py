import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logger(name: str, log_file: str = "app.log") -> logging.Logger:
    """
    Logger kurulumu yapar.
    
    Args:
        name: Logger adı
        log_file: Log dosyasının adı
        
    Returns:
        logging.Logger: Yapılandırılmış logger nesnesi
    """
    # Log dizinini oluştur
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Logger oluştur
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Format belirle
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Dosya handler'ı
    file_handler = RotatingFileHandler(
        log_dir / log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Konsol handler'ı
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Handler'ları ekle
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 