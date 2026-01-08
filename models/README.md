# LightFM Tourism Recommendation Models

Direktori ini menyimpan artifacts dari model LightFM yang sudah dilatih.

## 📦 Model Artifacts

File-file yang diperlukan:

1. **lightfm_model.pkl** - Model LightFM yang sudah trained
2. **dataset_mapping.pkl** - Mapping untuk user_id, wisata_id ke indices
3. **item_features.pkl** - Features matrix untuk wisata (kategori, fasilitas, dll)
4. **user_features.pkl** - Features matrix untuk user (umur, asal_kota, jenis_kelamin)

## 🔄 Cara Melatih/Memperbarui Model

Model dilatih menggunakan notebook di `notebooks/model-training-v1.ipynb`.

### Steps:

1. Buka notebook training
2. Jalankan semua cells
3. Model akan otomatis tersimpan di folder ini
4. Restart backend server untuk load model baru

## 📊 Model Information

- **Algorithm:** LightFM (Hybrid Collaborative + Content-based Filtering)
- **Loss Function:** WARP (Weighted Approximate-Rank Pairwise)
- **Features:** 
  - User: umur, asal_kota, jenis_kelamin
  - Item: kategori, fasilitas, lokasi

## 🔍 Model Loading

Model di-load otomatis oleh `recommendation_service.py` saat backend start.

```python
# Load model
with open("models/lightfm_model.pkl", "rb") as f:
    model = pickle.load(f)
```

## 📝 Notes

- **Jangan** hapus atau rename file-file di folder ini
- Backup model artifacts sebelum melatih model baru
- File size: ~1-10 MB (tergantung ukuran dataset)

## 🐛 Troubleshooting

**Error loading model:**
- Check apakah semua 4 file ada
- Check versi lightfm yang digunakan (harus sama dengan saat training)
- Try retrain model jika ada version mismatch

**Model accuracy rendah:**
- Tambah lebih banyak interaction data
- Tune hyperparameters di notebook training
- Tambah lebih banyak features
