"""
Service untuk load model dan generate recommendations
"""
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import List, Dict, Optional
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self):
        """Initialize recommendation service"""
        self.model = None
        self.user_features = None
        self.item_features = None
        self.wisata_data = None
        self.user_id_map = None
        self.item_id_map = None
        self.user_feature_map = None
        self.item_feature_map = None
        self.is_loaded = False
        
    def load_model(self, model_dir: str = None):
        """Load trained model and data"""
        try:
            # Auto-detect project root and models directory
            if model_dir is None:
                # Get current file directory
                current_dir = Path(__file__).parent
                # Navigate to project root (from backend/app/services/ to root)
                project_root = current_dir.parent.parent.parent
                model_path = project_root / "models"
            else:
                model_path = Path(model_dir)
            
            logger.info(f"Loading model from: {model_path.absolute()}")
            
            # Check if path exists
            if not model_path.exists():
                raise FileNotFoundError(f"Models directory not found: {model_path.absolute()}")
            
            # Load model
            logger.info("Loading LightFM model...")
            model_file = model_path / "lightfm_model.pkl"
            if not model_file.exists():
                raise FileNotFoundError(f"Model file not found: {model_file}")
            with open(model_file, "rb") as f:
                self.model = pickle.load(f)
            logger.info("✓ Model loaded")
            
            # Load feature matrices
            logger.info("Loading feature matrices...")
            with open(model_path / "user_features.pkl", "rb") as f:
                self.user_features = pickle.load(f)
            logger.info(f"✓ User features loaded: {self.user_features.shape}")
            
            with open(model_path / "item_features.pkl", "rb") as f:
                self.item_features = pickle.load(f)
            logger.info(f"✓ Item features loaded: {self.item_features.shape}")
            
            # Load mappings (terpisah)
            logger.info("Loading ID mappings...")
            with open(model_path / "user_id_map.pkl", "rb") as f:
                self.user_id_map = pickle.load(f)
            logger.info(f"✓ User ID map loaded: {len(self.user_id_map)} users")
            
            with open(model_path / "item_id_map.pkl", "rb") as f:
                self.item_id_map = pickle.load(f)
            logger.info(f"✓ Item ID map loaded: {len(self.item_id_map)} items")
            
            # Load feature mappings
            logger.info("Loading feature mappings...")
            with open(model_path / "user_feature_map.pkl", "rb") as f:
                self.user_feature_map = pickle.load(f)
            logger.info(f"✓ User feature map loaded: {len(self.user_feature_map)} features")
            
            with open(model_path / "item_feature_map.pkl", "rb") as f:
                self.item_feature_map = pickle.load(f)
            logger.info(f"✓ Item feature map loaded: {len(self.item_feature_map)} features")
            
            # Load wisata data
            logger.info("Loading wisata data...")
            wisata_file = model_path / "wisata_data.csv"
            if not wisata_file.exists():
                raise FileNotFoundError(f"Wisata data not found: {wisata_file}")
            self.wisata_data = pd.read_csv(wisata_file)
            
            # Convert wisata_data to dict for faster lookup
            # Determine the ID column name
            if 'Place_Id' in self.wisata_data.columns:
                id_col = 'Place_Id'
            elif 'wisata_id' in self.wisata_data.columns:
                id_col = 'wisata_id'
            else:
                # Use first column as ID
                id_col = self.wisata_data.columns[0]
                logger.warning(f"Using '{id_col}' as ID column")
            
            self.wisata_dict = self.wisata_data.set_index(id_col).to_dict('index')
            
            self.is_loaded = True
            logger.info("="*60)
            logger.info("🎉 All model artifacts loaded successfully!")
            logger.info(f"📊 Total wisata: {len(self.wisata_data)}")
            logger.info("="*60)
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def get_recommendations(
        self, 
        umur: int, 
        asal_kota: str, 
        jenis_kelamin: str, 
        n_recommendations: int = 5
    ) -> List[Dict]:
        """Generate recommendations for user profile"""
        try:
            if not self.is_loaded:
                self.load_model()
            
            # Create user feature string
            user_feature_str = f"umur_{umur}|asal_kota_{asal_kota}|jenis_kelamin_{jenis_kelamin}"
            logger.info(f"Generating recommendations for: {user_feature_str}")
            
            # DEBUG: Print shapes
            logger.info(f"DEBUG - User features shape: {self.user_features.shape}")
            logger.info(f"DEBUG - Item features shape: {self.item_features.shape}")
            logger.info(f"DEBUG - User ID map length: {len(self.user_id_map)}")
            logger.info(f"DEBUG - Item ID map length: {len(self.item_id_map)}")
            
            # Get all item IDs
            n_items = self.item_features.shape[0]
            item_ids = np.arange(n_items)
            logger.info(f"DEBUG - Total items to predict: {n_items}")
            logger.info(f"DEBUG - item_ids: {item_ids}")
            
            # Use first user as dummy for cold start
            user_idx = 0
            logger.info(f"DEBUG - Using user_idx: {user_idx}")
            
            # Predict scores
            try:
                logger.info("DEBUG - Starting prediction...")
                scores = self.model.predict(
                    user_ids=user_idx,
                    item_ids=item_ids,
                    user_features=self.user_features,
                    item_features=self.item_features
                )
                logger.info(f"DEBUG - Prediction done. Scores shape: {scores.shape}")
                logger.info(f"DEBUG - Scores sample (first 5): {scores[:5]}")
            except Exception as pred_error:
                logger.error(f"ERROR in prediction: {pred_error}")
                logger.error(f"Error type: {type(pred_error).__name__}")
                import traceback
                logger.error(f"Traceback:\n{traceback.format_exc()}")
                raise
            
            # Get top N recommendations
            top_indices = np.argsort(-scores)[:n_recommendations]
            logger.info(f"DEBUG - Top indices: {top_indices}")
            logger.info(f"DEBUG - Top scores: {scores[top_indices]}")
            
            # Reverse item_id_map to get Place_Id from internal ID
            id_to_place = {v: k for k, v in self.item_id_map.items()}
            logger.info(f"DEBUG - id_to_place sample (first 3): {list(id_to_place.items())[:3]}")
            logger.info(f"DEBUG - wisata_dict keys sample: {list(self.wisata_dict.keys())[:3]}")
            
            recommendations = []
            for i, idx in enumerate(top_indices):
                logger.info(f"DEBUG - [{i+1}] Processing idx: {idx}")
                place_id = id_to_place.get(idx)
                logger.info(f"DEBUG - [{i+1}] Mapped to place_id: {place_id}")
                
                if place_id is None:
                    logger.warning(f"DEBUG - [{i+1}] place_id is None for idx {idx}")
                    continue
                
                if place_id not in self.wisata_dict:
                    logger.warning(f"DEBUG - [{i+1}] place_id '{place_id}' not in wisata_dict")
                    logger.warning(f"DEBUG - Available keys: {list(self.wisata_dict.keys())}")
                    continue
                
                try:
                    wisata_info = self.wisata_dict[place_id]
                    logger.info(f"DEBUG - [{i+1}] wisata_info keys: {wisata_info.keys()}")
                    
                    # Helper function to get value with fallback
                    def get_field(primary, fallback, default='Unknown'):
                        val = wisata_info.get(primary, wisata_info.get(fallback, default))
                        return val if pd.notna(val) else default
                    
                    # Create recommendation dict
                    rec = {
                        "place_id": str(place_id),
                        "nama_wisata": str(get_field('Place_Name', 'nama_wisata')),
                        "kategori": str(get_field('Category', 'kategori')),
                        "lokasi": str(get_field('City', 'lokasi')),
                        "harga": int(get_field('Price', 'harga', 0)),
                        "rating": float(get_field('Rating', 'rating', 4.0)),
                        "score": float(scores[idx]),
                        "deskripsi": str(get_field('Description', 'deskripsi', 'Tempat wisata menarik di Jawa Timur'))[:200] + "...",
                        "image_url": f"/static/images/{str(get_field('Place_Name', 'nama_wisata', 'default')).lower().replace(' ', '_')}.jpg"
                    }
                    recommendations.append(rec)
                    logger.info(f"DEBUG - [{i+1}] ✓ Added: {rec['nama_wisata']} | Score: {rec['score']:.4f}")
                except Exception as rec_error:
                    logger.error(f"ERROR creating recommendation for place_id {place_id}: {rec_error}")
                    logger.error(f"wisata_info: {wisata_info}")
                    import traceback
                    logger.error(f"Traceback:\n{traceback.format_exc()}")
            
            logger.info(f"✓ Generated {len(recommendations)} recommendations")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            import traceback
            logger.error(f"Full traceback:\n{traceback.format_exc()}")
            raise
    
    def get_all_wisata(self) -> List[Dict]:
        """Get all wisata data"""
        try:
            if not self.is_loaded:
                self.load_model()
            
            wisata_list = []
            for place_id, wisata_info in self.wisata_dict.items():
                # Helper function
                def get_field(primary, fallback, default='Unknown'):
                    val = wisata_info.get(primary, wisata_info.get(fallback, default))
                    return val if pd.notna(val) else default
                
                wisata = {
                    "place_id": place_id,
                    "nama_wisata": str(get_field('Place_Name', 'nama_wisata')),
                    "kategori": str(get_field('Category', 'kategori')),
                    "lokasi": str(get_field('City', 'lokasi')),
                    "harga": int(get_field('Price', 'harga', 0)),
                    "rating": float(get_field('Rating', 'rating', 4.0)),
                    "deskripsi": str(get_field('Description', 'deskripsi', 'Tempat wisata menarik'))[:200] + "...",
                    "image_url": f"/static/images/{str(get_field('Place_Name', 'nama_wisata', 'default')).lower().replace(' ', '_')}.jpg"
                }
                wisata_list.append(wisata)
            
            return wisata_list
            
        except Exception as e:
            logger.error(f"Error getting wisata list: {str(e)}")
            raise
    
    def get_wisata_info(self, place_id: str) -> Optional[Dict]:
        """Get specific wisata information"""
        try:
            if not self.is_loaded:
                self.load_model()
            
            if place_id not in self.wisata_dict:
                return None
            
            wisata_info = self.wisata_dict[place_id]
            
            # Helper function
            def get_field(primary, fallback, default='Unknown'):
                val = wisata_info.get(primary, wisata_info.get(fallback, default))
                return val if pd.notna(val) else default
            
            return {
                "place_id": place_id,
                "nama_wisata": str(get_field('Place_Name', 'nama_wisata')),
                "kategori": str(get_field('Category', 'kategori')),
                "lokasi": str(get_field('City', 'lokasi')),
                "harga": int(get_field('Price', 'harga', 0)),
                "rating": float(get_field('Rating', 'rating', 4.0)),
                "deskripsi": str(get_field('Description', 'deskripsi', 'Tempat wisata menarik di Jawa Timur')),
                "image_url": f"/static/images/{str(get_field('Place_Name', 'nama_wisata', 'default')).lower().replace(' ', '_')}.jpg"
            }
            
        except Exception as e:
            logger.error(f"Error getting wisata info: {str(e)}")
            raise

# Create singleton instance
recommendation_service = RecommendationService()