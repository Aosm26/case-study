# The Dyrt Kamp Alanı Veri Toplayıcı

Bu proje, The Dyrt web sitesinden kamp alanı verilerini toplayan, işleyen ve PostgreSQL veritabanında saklayan bir veri toplama uygulamasıdır.

## 🚀 Özellikler

- **Veri Toplama**: The Dyrt API'si üzerinden kamp alanı verilerini çeker
- **Adres Çözümleme**: OpenStreetMap Nominatim API kullanarak koordinatlardan adres bilgisi çeker
- **Çoklu İş Parçacığı**: Threading ile paralel veri çekme
- **Veritabanı Entegrasyonu**: PostgreSQL veritabanı ile entegrasyon
- **Veri Doğrulama**: Pydantic ile veri doğrulama
- **Hata Yönetimi**: Kapsamlı hata yakalama ve işleme
- **Loglama**: Detaylı loglama sistemi
- **Zamanlanmış Görevler**: Otomatik veri güncelleme
- **Docker Desteği**: Containerized deployment

## ⚠️ API Kısıtlamaları ve Çözümler

### OpenStreetMap Nominatim API Kısıtlamaları
- **Rate Limiting**: API, saniyede 1 istek ile sınırlıdır
- **Çözüm**: 
  - Her istek arasında 1 saniye bekleme süresi
  - İstek sayısını sınırlama (varsayılan: 50 adres)
  - Hata durumunda otomatik bekleme ve yeniden deneme

### The Dyrt API Kısıtlamaları
- **Sayfalama**: Her sayfada maksimum 100 veri
- **Çözüm**:
  - Threading ile paralel sayfa çekme
  - Otomatik sayfa sayısı hesaplama
  - Hata durumunda kalan sayfaları tekrar deneme

## 🔧 Özelleştirmeler

### Veri Çekme Özelleştirmeleri
- Sayfa başına veri sayısı ayarı (`size` parametresi)
- Maksimum thread sayısı ayarı (`max_workers` parametresi)
- Başlangıç ve bitiş sayfa numarası belirleme

### Adres Çözümleme Özelleştirmeleri
- İşlenecek maksimum adres sayısı ayarı (`count` parametresi)
- Rate limiting için bekleme süresi ayarı
- User-Agent özelleştirme

### Veritabanı Özelleştirmeleri
- Batch işlem boyutu ayarı (varsayılan: 100 kayıt)
- Otomatik tablo oluşturma
- Var olan kayıtları güncelleme (merge) stratejisi

### Zamanlanmış Görev Özelleştirmeleri
- Görev tekrarlama aralığı ayarı
- İlk çalıştırma zamanı belirleme
- Hata durumunda yeniden deneme stratejisi

## 📋 Gereksinimler

- Python 3.8+
- PostgreSQL 13+
- Docker ve Docker Compose (opsiyonel)

## 🛠️ Kullanılan Teknolojiler

### Backend
- **Python**: Ana programlama dili
- **SQLAlchemy**: ORM (Object-Relational Mapping)
- **Pydantic**: Veri doğrulama ve serileştirme
- **Schedule**: Zamanlanmış görevler
- **Requests**: HTTP istekleri
- **Threading**: Paralel işlem yönetimi

### Veritabanı
- **PostgreSQL**: İlişkisel veritabanı
- **psycopg2**: PostgreSQL Python sürücüsü

### DevOps
- **Docker**: Konteynerizasyon
- **Docker Compose**: Çoklu konteyner yönetimi

## 🚀 Kurulum

### Docker ile Kurulum

1. Docker ve Docker Compose'u yükleyin
2. Projeyi klonlayın:
   ```bash
   git clone [repo-url]
   cd case_study
   ```
3. Docker konteynerlerini başlatın:
   ```bash
   docker compose up -d
   ```

### Manuel Kurulum

1. Python 3.8 veya üstünü yükleyin
2. Projeyi klonlayın:
   ```bash
   git clone [repo-url]
   cd case_study
   ```
3. Sanal ortam oluşturun ve aktifleştirin:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
4. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
5. PostgreSQL veritabanını kurun ve yapılandırın

## 💻 Kullanım

### Tek Seferlik Çalıştırma

```bash
python main.py
```

### Zamanlanmış Görevleri Başlatma

Varsayılan olarak her 24 saatte bir çalışır:
```bash
python main.py --schedule
# veya
python main.py -s
```

Özel aralıkla çalıştırma (örneğin her 12 saatte bir):
```bash
python main.py --schedule --interval 12
# veya
python main.py -s -i 12
```

### Docker ile Çalıştırma

```bash
docker compose up
```

## 📁 Proje Yapısı

```
case_study/
├── src/
│   ├── api_client/
│   │   ├── fetch_campgrounds.py
│   │   ├── fetch_campgrounds_threaded.py
│   │   ├── geocode_addresses.py
│   │   └── save_to_db.py
│   ├── models/
│   │   └── campground_db.py
│   ├── scheduler/
│   │   └── task_scheduler.py
│   └── utils/
│       ├── exceptions.py
│       └── logger.py
├── logs/
├── Dockerfile
├── docker-compose.yml
├── main.py
└── requirements.txt
```

## 🔍 Özellik Detayları

### Veri Toplama
- The Dyrt API'si üzerinden kamp alanı verilerini çeker
- Threading ile paralel veri çekme
- Sayfalama desteği
- Hata durumunda yeniden deneme

### Adres Çözümleme
- OpenStreetMap Nominatim API kullanımı
- Rate limiting yönetimi
- Hata durumunda alternatif çözümler

### Veritabanı İşlemleri
- SQLAlchemy ORM kullanımı
- Otomatik tablo oluşturma
- Veri doğrulama ve dönüştürme
- Batch işlem desteği

### Loglama Sistemi
- Her modül için ayrı log dosyaları
- Farklı log seviyeleri (DEBUG, INFO, WARNING, ERROR)
- Rotating file handler
- Detaylı hata izleme

### Zamanlanmış Görevler
- Esnek zamanlama seçenekleri
- Otomatik yeniden başlatma
- Hata durumunda bildirim
- Thread-safe çalışma

## 🛠️ Geliştirme

### Yeni Özellik Ekleme
1. İlgili modülü oluşturun
2. Gerekli testleri yazın
3. Loglama ekleyin
4. Hata yönetimini ekleyin
5. Dokümantasyonu güncelleyin

### Hata Ayıklama
- Log dosyalarını kontrol edin (`logs/` dizini)
- Hata mesajlarını inceleyin
- Gerekirse debug modunda çalıştırın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.
