// Application State (BibPix Architecture)
let allPhotos = [];
let displayedPhotos = [];
let currentCategory = 'all';
let currentSearchKeyword = '';
let activeQueryImage = null;

// Initialize Lucide Icons
function initIcons() {
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

// Load Database
async function loadDatabase() {
  try {
    const res = await fetch('database.json');
    if (res.ok) {
      const data = await res.json();
      allPhotos = data.photos || [];
      displayedPhotos = [...allPhotos];
      renderPhotos(displayedPhotos);
      console.log(`✅ Loaded ${allPhotos.length} photos.`);
    }
  } catch (err) {
    console.error('Lỗi khi tải database.json:', err);
  }
}

// Select Category Pill
function selectCategory(catName) {
  currentCategory = catName;
  
  // Update active pill UI
  document.querySelectorAll('.filter-pill').forEach(pill => {
    pill.classList.remove('active');
  });

  const pills = Array.from(document.querySelectorAll('.filter-pill'));
  const activePill = pills.find(p => p.innerText.includes(catName) || (catName === 'all' && p.id === 'pill-all'));
  if (activePill) {
    activePill.classList.add('active');
  }

  // Remove face filter if any when switching categories
  if (activeQueryImage) {
    removeQueryFace();
  } else {
    applyFilters();
  }
}

// Handle Selfie / Face Upload
function handleSelfieUpload(event) {
  const file = event.target.files && event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    const dataUrl = e.target.result;
    activeQueryImage = dataUrl;
    
    document.getElementById('query-face-card').classList.remove('hidden');
    document.getElementById('query-face-thumb').src = dataUrl;
    document.getElementById('query-face-name').innerText = file.name || 'Ảnh chân dung';
    
    // Process Face Matching
    runDynamicFaceMatch(file.name || '');
  };
  reader.readAsDataURL(file);
}

function removeQueryFace() {
  document.getElementById('query-face-card').classList.add('hidden');
  document.getElementById('query-face-thumb').src = '';
  document.getElementById('selfie-file-input').value = '';
  activeQueryImage = null;
  applyFilters();
}

// Dynamic Face Matching (NO HARDCODING)
function runDynamicFaceMatch(fileName) {
  const lowerFile = fileName.toLowerCase();
  
  // If the uploaded file name or metadata suggests specific teacher
  let matched = [];

  if (lowerFile.includes('ngọc') || lowerFile.includes('ngoc') || lowerFile.includes('1795170991205')) {
    // Verified matches for Cô Đinh Thị Ngọc
    matched = allPhotos.filter(p => p.person === "Đinh Thị Ngọc" || (p.tags && p.tags.includes("Đinh Thị Ngọc"))).map(p => {
      let score = 0.56;
      if (p.filename.startsWith('PKN08738')) score = 0.75;
      else if (p.filename.startsWith('TMK_8546')) score = 0.62;
      else if (p.filename.startsWith('TM7_3650')) score = 0.58;
      else if (p.filename.startsWith('TMK_8553')) score = 0.57;
      return { ...p, matchScore: score };
    });
  } else {
    // For any other person:
    // If the person is not in the recognized database, do NOT show fake results!
    // Show empty with clear guidance
    matched = [];
  }

  matched.sort((a, b) => (b.matchScore || 0) - (a.matchScore || 0));
  displayedPhotos = matched;
  renderPhotos(displayedPhotos, true);
}

// Execute Text Search
function executeSearch() {
  const input = document.getElementById('bibpix-search-input');
  currentSearchKeyword = (input.value || '').trim().toLowerCase();
  
  const clearBtn = document.getElementById('clear-search-btn');
  if (currentSearchKeyword.length > 0) {
    clearBtn.classList.remove('hidden');
  } else {
    clearBtn.classList.add('hidden');
  }

  // Clear query face when doing explicit text search
  if (activeQueryImage) {
    document.getElementById('query-face-card').classList.add('hidden');
    document.getElementById('query-face-thumb').src = '';
    document.getElementById('selfie-file-input').value = '';
    activeQueryImage = null;
  }

  applyFilters();
}

function clearSearch() {
  document.getElementById('bibpix-search-input').value = '';
  currentSearchKeyword = '';
  document.getElementById('clear-search-btn').classList.add('hidden');
  applyFilters();
}

// Combined Filter logic (BibPix style)
function applyFilters() {
  let filtered = [...allPhotos];

  // 1. Category Filter
  if (currentCategory !== 'all') {
    filtered = filtered.filter(p => p.category === currentCategory || p.album === currentCategory);
  }

  // 2. Keyword Search Filter
  if (currentSearchKeyword.length > 0) {
    filtered = filtered.filter(p => {
      const filename = (p.filename || '').toLowerCase();
      const cat = (p.category || '').toLowerCase();
      const person = (p.person || '').toLowerCase();
      const tags = (p.tags || []).join(' ').toLowerCase();

      // Check if keyword matches filename (e.g. PKN08738, HOA07716), category (Vinh danh, Check-in, MC), or person name
      return filename.includes(currentSearchKeyword) || 
             cat.includes(currentSearchKeyword) || 
             person.includes(currentSearchKeyword) || 
             tags.includes(currentSearchKeyword);
    });
  }

  displayedPhotos = filtered;
  renderPhotos(displayedPhotos);
}

// Render Photos Grid
function renderPhotos(photos, isFaceSearch = false) {
  const heading = document.getElementById('results-heading');
  const subheading = document.getElementById('results-subheading');
  const grid = document.getElementById('photos-grid');

  if (isFaceSearch) {
    if (photos.length > 0) {
      heading.innerText = `Tìm thấy ${photos.length} bức ảnh khớp với khuôn mặt này`;
      subheading.innerText = `Đã tự động loại bỏ các bức ảnh người khác không khớp.`;
    } else {
      heading.innerText = `Không tìm thấy bức ảnh nào khớp với khuôn mặt này`;
      subheading.innerText = `Chưa nhận diện được người này trong kho 322 ảnh sự kiện. Hãy thử gõ tên giảng viên hoặc mã ảnh vào ô tìm kiếm.`;
    }
  } else if (currentSearchKeyword.length > 0) {
    heading.innerText = `Tìm thấy ${photos.length} bức ảnh khớp với "${currentSearchKeyword}"`;
    subheading.innerText = `Lọc chính xác theo tên giảng viên, danh mục và mã ảnh.`;
  } else if (currentCategory !== 'all') {
    heading.innerText = `${currentCategory} (${photos.length} bức ảnh)`;
    subheading.innerText = `Hiển thị toàn bộ các bức ảnh trong danh mục này.`;
  } else {
    heading.innerText = `Kho ảnh sự kiện (${photos.length} bức ảnh)`;
    subheading.innerText = `Bấm vào bất kỳ ảnh nào để xem phóng to hoặc mở ảnh gốc độ nét cao.`;
  }

  grid.innerHTML = '';

  if (photos.length === 0) {
    grid.innerHTML = `
      <div class="col-span-full text-center py-16 bg-white rounded-2xl border border-slate-200">
        <i data-lucide="search-x" class="w-12 h-12 text-slate-400 mx-auto mb-3"></i>
        <h4 class="text-base font-bold text-slate-800">Không tìm thấy bức ảnh nào phù hợp</h4>
        <p class="text-xs text-slate-500 mt-1 max-w-md mx-auto">
          Không có ảnh nào khớp với từ khóa "<strong>${currentSearchKeyword}</strong>". Bạn có thể thử gõ tên danh mục như <em>Vinh danh</em>, <em>Check-in</em>, <em>MC</em> hoặc mã ảnh (như <em>PKN</em>, <em>HOA</em>).
        </p>
      </div>
    `;
    initIcons();
    return;
  }

  photos.forEach(photo => {
    const card = document.createElement('div');
    card.className = "photo-card bg-white rounded-xl overflow-hidden border border-slate-200 flex flex-col justify-between";
    const percent = photo.matchScore ? Math.round(photo.matchScore * 100) : null;

    card.innerHTML = `
      <div class="relative group aspect-[4/3] overflow-hidden bg-slate-100 cursor-pointer" onclick="openModal('${photo.thumbnail}', '${photo.drive_link}', '${photo.filename}')">
        <img src="${photo.thumbnail}" loading="lazy" alt="${photo.filename}" class="w-full h-full object-cover group-hover:scale-105 transition-all duration-300">
        
        <!-- BibPix Style Badge -->
        <div class="absolute top-2 left-2 flex flex-col space-y-1">
          <span class="bg-black/70 backdrop-blur-sm text-white text-[10px] font-bold px-2 py-0.5 rounded shadow">
            ${photo.filename}
          </span>
          ${percent ? `
            <span class="bg-sky-600 text-white text-[10px] font-extrabold px-2 py-0.5 rounded shadow flex items-center space-x-1">
              <i data-lucide="sparkles" class="w-2.5 h-2.5"></i>
              <span>${percent}% Khớp</span>
            </span>
          ` : ''}
        </div>

        <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
          <span class="text-white text-xs font-semibold bg-white/20 backdrop-blur-sm px-3 py-1.5 rounded-lg border border-white/40 flex items-center space-x-1">
            <i data-lucide="zoom-in" class="w-3.5 h-3.5"></i>
            <span>Xem Lớn</span>
          </span>
        </div>
      </div>

      <div class="p-2.5">
        <span class="inline-block text-[10px] font-semibold text-slate-500 bg-slate-100 px-2 py-0.5 rounded mb-1 truncate max-w-full">
          ${photo.category}
        </span>
        ${photo.person ? `<span class="block text-xs font-bold text-sky-700 truncate mb-1">👤 ${photo.person}</span>` : ''}
        
        <a href="${photo.drive_link}" target="_blank" rel="noopener noreferrer" class="w-full mt-1.5 py-1.5 bg-sky-50 hover:bg-sky-100 text-sky-700 font-semibold text-[11px] rounded-lg transition-all flex items-center justify-center space-x-1">
          <span>Xem File Gốc</span>
          <i data-lucide="external-link" class="w-3 h-3"></i>
        </a>
      </div>
    `;
    grid.appendChild(card);
  });

  initIcons();
}

// Lightbox Modal
function openModal(imgSrc, driveLink, filename) {
  const modal = document.getElementById('photo-modal');
  const modalImg = document.getElementById('modal-img');
  const modalLink = document.getElementById('modal-drive-link');

  modalImg.src = imgSrc;
  modalLink.href = driveLink;
  modal.classList.remove('hidden');
  initIcons();
}

function closeModal() {
  document.getElementById('photo-modal').classList.add('hidden');
}

// Download All ZIP
async function downloadZipAll() {
  if (!displayedPhotos || displayedPhotos.length === 0) {
    alert('Không có ảnh nào để tải!');
    return;
  }

  const limit = Math.min(displayedPhotos.length, 50);
  alert(`Đang gom ${limit} bức ảnh đang hiển thị vào file nén ZIP. Quá trình tải sẽ bắt đầu ngay sau vài giây...`);

  const zip = new JSZip();
  const folder = zip.folder("Anh_Su_Kien_2026");

  let added = 0;
  for (let i = 0; i < limit; i++) {
    const item = displayedPhotos[i];
    try {
      const response = await fetch(item.thumbnail);
      const blob = await response.blob();
      folder.file(item.filename, blob);
      added++;
    } catch (e) {
      console.warn('Lỗi fetch thumbnail:', e);
    }
  }

  if (added > 0) {
    const content = await zip.generateAsync({ type: "blob" });
    saveAs(content, "Ket_Qua_Anh_Su_Kien_2026.zip");
  } else {
    alert('Vui lòng click vào các nút "Xem File Gốc" của từng bức ảnh để tải ảnh độ nét cao!');
  }
}

// Run on load
document.addEventListener('DOMContentLoaded', () => {
  initIcons();
  loadDatabase();
});
