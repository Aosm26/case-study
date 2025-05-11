class BaseError(Exception):
    """Temel hata sınıfı"""
    pass

class APIError(BaseError):
    """API ile ilgili hatalar için"""
    pass

class DatabaseError(BaseError):
    """Veritabanı ile ilgili hatalar için"""
    pass

class ValidationError(BaseError):
    """Veri doğrulama hataları için"""
    pass

class GeocodingError(BaseError):
    """Adres çözümleme hataları için"""
    pass 