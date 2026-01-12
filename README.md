# Tourism Recommendation System

Sistem rekomendasi wisata menggunakan **LightFM** (Hybrid Collaborative + Content-based Filtering) dengan deployment web sederhana dan interaktif.

## Overview

Project ini merupakan sistem rekomendasi wisata yang dapat memberikan rekomendasi destinasi wisata berdasarkan profil user (umur, asal kota, jenis kelamin). Sistem menggunakan:

- **Machine Learning:** LightFM untuk hybrid recommendation
- **Backend:** FastAPI untuk REST API
- **Frontend:** HTML/CSS/JavaScript (Vanilla JS, no framework)
- **Deployment:** Localhost-based (dapat di-deploy ke cloud)

## Project Structure
Untuk struktur proyek ini lihat pada [PROJECT_STRUCTURE.txt](./PROJECT_STRUCTURE.txt)

## Quick Start

### 1. Prerequisites

- Python 3.8+
- Conda environment (LightFMProject)
- pip

### 2. Activate Environment
#### conda
```bash
conda init
conda activate (your_env)
```
#### venv
``` bash
.\Scripts\activate
```

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Pastikan Model Artifacts Ada

Check folder `models/` berisi:
- **item_feature_map.pkl**
- **item_features.pkl**
- **item_id_map.pkl**
- **lightfm_model.pkl**
- **user_feature_map.pkl**
- **user_features.pkl**
- **user_id_map.pkl**

Jika belum ada, jalankan notebook training terlebih dahulu.

### 5. Start Backend Server

```bash
cd backend/app
python main.py
```

Server akan running di: **http://localhost:8000**

## Data

### Wisata (8 destinasi):
- Gunung Bromo
- Kawah Ijen
- Pantai Klayar
- Telaga Sarangan
- Air Terjun Tumpak Sewu
- Pantai Balekambang
- Goa Gong Pacitan
- Pantai Watu Karung

### User Features:
- Umur (integer)
- Asal Kota (10 kota di Jawa Timur)
- Jenis Kelamin (P/L)

### Item Features:
- Kategori (Alam/Sejarah)
- Fasilitas (Parkir, Toilet, Warung, dll)
- Lokasi (Kota/Kabupaten)
- Harga (IDR)

## API Endpoints

### Health Check
```
GET /api/health
```

### Get Recommendations
```
POST /api/recommend?n=5
Content-Type: application/json

{
    "umur": 25,
    "asal_kota": "Surabaya",
    "jenis_kelamin": "P"
}
```

### Get All Wisata
```
GET /api/wisata
```

### Get Wisata Detail
```
GET /api/wisata/{wisata_id}
```

**Dokumentasi lengkap:** http://localhost:8000/docs (Swagger UI)

## Model Training

Model dilatih menggunakan LightFM (dengan environtment kaggle) dengan:
- **Algorithm:** WARP loss
- **Epochs:** ~30-50
- **Features:** User demographics + Item attributes
- **Evaluation:** Precision@K, Recall@K

Lihat notebook: [notebooks/model-training.ipynb](./notebooks/model-training.ipynb)

## Tech Stack

- **ML/AI:** Python, LightFM, NumPy, Pandas, Scikit-learn
- **Backend:** FastAPI, Uvicorn, Pydantic
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Tools:** Jupyter Notebook, Pickle