// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// DOM Elements
const userForm = document.getElementById('userForm');
const submitBtn = document.getElementById('submitBtn');
const btnText = document.querySelector('.btn-text');
const btnLoader = document.querySelector('.btn-loader');
const resultsSection = document.getElementById('resultsSection');
const loadingSection = document.getElementById('loadingSection');
const errorSection = document.getElementById('errorSection');
const recommendationsGrid = document.getElementById('recommendationsGrid');
const userInfo = document.getElementById('userInfo');
const errorMessage = document.getElementById('errorMessage');

// Form Submit Handler
userForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(userForm);
    const userData = {
        umur: parseInt(formData.get('umur')),
        asal_kota: formData.get('asal_kota'),
        jenis_kelamin: formData.get('jenis_kelamin')
    };
    const nRecommendations = parseInt(formData.get('n_recommendations'));
    
    // Show loading state
    showLoading();
    
    try {
        // Call API
        const response = await fetch(`${API_BASE_URL}/recommend?n=${nRecommendations}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Display results
        displayRecommendations(data);
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Terjadi kesalahan saat mengambil rekomendasi');
    }
});

// Show Loading State
function showLoading() {
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    loadingSection.style.display = 'block';
}

// Hide Loading State
function hideLoading() {
    submitBtn.disabled = false;
    btnText.style.display = 'inline';
    btnLoader.style.display = 'none';
    loadingSection.style.display = 'none';
}

// Display Recommendations
function displayRecommendations(data) {
    hideLoading();
    
    // Update user info
    const { user_profile, recommendations } = data;
    userInfo.innerHTML = `
        <strong>Profil:</strong> ${user_profile.jenis_kelamin === 'P' ? 'Perempuan' : 'Laki-laki'}, 
        ${user_profile.umur} tahun, dari ${user_profile.asal_kota}
    `;
    
    // Clear previous results
    recommendationsGrid.innerHTML = '';
    
    // Create recommendation cards
    recommendations.forEach((rec, index) => {
        const card = createRecommendationCard(rec, index);
        recommendationsGrid.appendChild(card);
    });
    
    // Show results
    resultsSection.style.display = 'block';
    
    // Smooth scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

// Create Recommendation Card
function createRecommendationCard(rec, index) {
    const card = document.createElement('div');
    card.className = 'recommendation-card';
    card.style.animationDelay = `${index * 0.1}s`;
    
    // Format price
    const formattedPrice = new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
    }).format(rec.harga);
    
    // Format score
    const scorePercent = Math.round(rec.score * 100);
    
    card.innerHTML = `
        <div class="card-image">
            <img src="${rec.image_url}" 
                 alt="${rec.nama_wisata}"
                 onerror="this.style.display='none'; this.parentElement.innerHTML += '🏝️'">
            <div class="card-score">⭐ ${rec.score.toFixed(2)}</div>
        </div>
        <div class="card-content">
            <h3 class="card-title">${rec.nama_wisata}</h3>
            <span class="card-category">${rec.kategori}</span>
            
            <div class="card-info">
                <strong>📍 Lokasi:</strong> ${rec.lokasi}
            </div>
            
            <div class="card-info">
                <strong>🎯 Fasilitas:</strong> ${rec.fasilitas}
            </div>
            
            <div class="card-price">
                ${formattedPrice}
            </div>
        </div>
    `;
    
    return card;
}

// Show Error
function showError(message) {
    hideLoading();
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    resultsSection.style.display = 'none';
}

// Hide Error
function hideError() {
    errorSection.style.display = 'none';
}

// Check API Health on page load
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        console.log('API Health:', data);
        
        if (!data.model_loaded) {
            console.warn('Model belum loaded!');
        }
    } catch (error) {
        console.error('API tidak dapat dijangkau:', error);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkAPIHealth();
});
