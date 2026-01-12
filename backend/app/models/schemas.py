"""
Pydantic models untuk request/response API
"""
from pydantic import BaseModel, Field
from typing import List, Optional

class UserProfile(BaseModel):
    """Model untuk profil user yang akan digunakan untuk rekomendasi"""
    user_id: Optional[str] = Field(None, description="User ID jika sudah ada di sistem")
    umur: int = Field(..., ge=1, le=100, description="Usia pengguna")
    asal_kota: str = Field(..., description="Kota asal pengguna")
    jenis_kelamin: str = Field(..., pattern="^(P|L)$", description="Jenis kelamin: P atau L")
    
    class Config:
        schema_extra = {
            "example": {
                "umur": 25,
                "asal_kota": "Surabaya",
                "jenis_kelamin": "P"
            }
        }

class WisataRecommendation(BaseModel):
    """Model untuk hasil rekomendasi wisata"""
    place_id: str
    nama_wisata: str
    kategori: str
    harga: int
    lokasi: str
    rating: float
    score: float
    deskripsi: str
    image_url: str  # URL/path untuk gambar wisata
    
class RecommendationResponse(BaseModel):
    """Response untuk endpoint rekomendasi"""
    user_profile: UserProfile
    recommendations: List[WisataRecommendation]
    total_recommendations: int
    
class ErrorResponse(BaseModel):
    """Response untuk error"""
    error: str
    detail: Optional[str] = None
