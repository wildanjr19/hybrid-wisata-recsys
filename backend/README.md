# Backend - Tourism Recommendation API

Backend API untuk sistem rekomendasi wisata menggunakan LightFM model.

## 📋 Prerequisites

- Python 3.8 atau lebih tinggi
- pip (Python package manager)

## 🚀 Cara Menjalankan Backend

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Pastikan Model Artifacts Ada

Pastikan folder `models/` di root project berisi file-file berikut:
- `lightfm_model.pkl`
- `dataset_mapping.pkl`
- `item_features.pkl`
- `user_features.pkl`

### 3. Jalankan Server

```bash
cd app
python main.py
```

Atau menggunakan uvicorn langsung:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server akan berjalan di: **http://localhost:8000**

## 📚 API Endpoints

### 1. Health Check
```
GET /
GET /api/health
```

### 2. Get Recommendations
```
POST /api/recommend?n=5
Content-Type: application/json

{
    "umur": 25,
    "asal_kota": "Surabaya",
    "jenis_kelamin": "P"
}
```

Response:
```json
{
    "user_profile": {
        "umur": 25,
        "asal_kota": "Surabaya",
        "jenis_kelamin": "P"
    },
    "recommendations": [
        {
            "wisata_id": "W1",
            "nama_wisata": "Gunung Bromo",
            "kategori": "Alam",
            "harga": 35000,
            "fasilitas": "Parkir, Toilet, Warung...",
            "lokasi": "Probolinggo",
            "score": 0.8542,
            "image_url": "/static/images/gunung_bromo.jpg"
        }
    ],
    "total_recommendations": 5
}
```

### 3. Get All Wisata
```
GET /api/wisata
```

### 4. Get Wisata Detail
```
GET /api/wisata/{wisata_id}
```

## 🏗️ Struktur Project

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point FastAPI
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic models
│   ├── routes/
│   │   ├── __init__.py
│   │   └── recommendation.py # API endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   └── recommendation_service.py # Business logic
│   └── utils/
│       └── __init__.py
└── requirements.txt
```

## 🔧 Konfigurasi

### CORS Settings
CORS diaktifkan untuk semua origins (`*`) untuk development. Untuk production, ubah di `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://yourdomain.com"],  # Ganti dengan domain Anda
    ...
)
```

### Port Configuration
Default port: `8000`. Untuk mengubah, edit di `main.py`:

```python
uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
```

## 🧪 Testing API

### Menggunakan curl:
```bash
curl -X POST "http://localhost:8000/api/recommend?n=5" \
     -H "Content-Type: application/json" \
     -d '{"umur": 25, "asal_kota": "Surabaya", "jenis_kelamin": "P"}'
```

### Menggunakan Browser:
Buka: http://localhost:8000/docs

FastAPI otomatis menyediakan interactive API documentation (Swagger UI).

## 📝 Notes

- Model akan di-load otomatis saat server start
- Jika ada error saat loading model, check logs di console
- Untuk production deployment, gunakan gunicorn + uvicorn workers
- Aktifkan environment variable untuk konfigurasi production

## 🐛 Troubleshooting

**Error: Model not found**
- Pastikan folder `models/` ada di root project
- Check path di `recommendation_service.py`

**Error: ModuleNotFoundError**
- Jalankan: `pip install -r requirements.txt`

**Port already in use**
- Ganti port di `main.py` atau kill process yang menggunakan port 8000
