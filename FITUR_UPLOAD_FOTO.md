# 📸 FITUR UPLOAD FOTO - PANDUAN LENGKAP

## 🎯 Overview

Fitur upload foto memungkinkan **Penerbit** untuk menambahkan gambar saat membuat artikel berita.
- Gambar disimpan sebagai **BLOB di PostgreSQL**
- Support format: **JPEG, PNG, GIF, BMP**
- Max size: **5 MB per gambar**
- Preview gambar sebelum publish
- Resize otomatis jika gambar terlalu besar

---

## 🔧 LANGKAH INSTALASI

### Step 1: Jalankan SQL Migration

1. Login ke **Railway Dashboard**
2. Buka **PostgreSQL Database**
3. Klik tab **Query**
4. Copy-paste isi file `migration_add_image_column.sql`
5. Klik **Run**

**File migration akan:**
- Tambah kolom `image_data` (BYTEA) - untuk menyimpan binary gambar
- Tambah kolom `image_filename` (VARCHAR) - nama file
- Tambah kolom `image_mimetype` (VARCHAR) - tipe file (image/jpeg, dll)
- Tambah index untuk performa

### Step 2: Update File Python

Download file-file yang sudah diupdate:

1. **app_db_fixed.py** - Fungsi database untuk handle gambar
2. **penerbit_dashboard.py** - Dashboard dengan fitur upload
3. **user_dashboard.py** - Dashboard untuk menampilkan gambar (opsional)

### Step 3: Install Dependencies Tambahan

```bash
pip install Pillow>=9.0.0
```

Update `requirements.txt`:
```
PyQt5>=5.15.0
psycopg2-binary>=2.9.0
Pillow>=9.0.0
```

---

## 📋 FUNGSI-FUNGSI BARU

### Di app_db_fixed.py:

```python
# 1. Create news dengan gambar
create_news_with_image(
    author="username",
    title="Judul Artikel", 
    content="Isi artikel...",
    published=True,
    image_data=binary_data,  # bytes
    image_filename="foto.jpg",
    image_mimetype="image/jpeg"
)

# 2. Get gambar dari artikel
image_data, filename, mimetype = get_news_image(news_id=1)

# 3. Update gambar artikel
update_news_image(news_id=1, image_data, filename, mimetype)

# 4. Hapus gambar
delete_news_image(news_id=1)

# 5. List artikel dengan info gambar
list_my_news_with_images(author="username", limit=50)
# Returns: [(id, title, status, created, has_image), ...]
```

---

## 🎨 FITUR UI BARU

### Penerbit Dashboard:

1. **Button "📸 UPLOAD IMAGE"**
   - Click untuk pilih gambar dari komputer
   - Support multi-format (JPG, PNG, GIF, BMP)
   
2. **Preview Area**
   - Menampilkan preview gambar yang dipilih
   - Ukuran max preview: 400x300px
   - Info: nama file, ukuran file, dimensi

3. **Button "🗑️ REMOVE IMAGE"**
   - Hapus gambar yang sudah dipilih
   - Muncul setelah gambar di-upload

4. **Auto Resize**
   - Gambar > 1920px width otomatis di-resize
   - Quality 85% untuk balance size vs quality

5. **Validation**
   - Max 5MB per file
   - Format harus valid (JPEG/PNG/GIF/BMP)
   - Warning jika file terlalu besar

---

## 🧪 CARA TESTING

### Test 1: Upload Gambar Baru

1. Login sebagai **Penerbit**
2. Buka tab **"⚡ CREATE ARTICLE"**
3. Isi **Title** dan **Content**
4. Click **"📸 UPLOAD IMAGE"**
5. Pilih gambar dari komputer (JPG/PNG)
6. Preview muncul ✅
7. Click **"🚀 PUBLISH NOW"**
8. Artikel tersimpan dengan gambar ✅

### Test 2: Lihat Artikel dengan Gambar

1. Buka tab **"📡 MY ARTICLES"**
2. Lihat kolom **"IMAGE"**
3. Artikel dengan gambar ada icon **"🖼️"**
4. Artikel tanpa gambar ada **"-"**

### Test 3: Remove Gambar

1. Upload gambar
2. Preview muncul
3. Click **"🗑️ REMOVE IMAGE"**
4. Preview hilang ✅
5. Upload gambar lain
6. Preview gambar baru muncul ✅

### Test 4: Validasi Size

1. Pilih gambar > 5MB
2. Warning muncul: "File too large!"
3. Gambar tidak di-upload ✅

### Test 5: Display di User Dashboard

1. Login sebagai **User**
2. Buka artikel yang ada gambarnya
3. Gambar tampil di atas content ✅

---

## 📊 DATABASE STRUCTURE

### Tabel `news` (Updated):

```sql
CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP,
    
    -- NEW COLUMNS for images
    image_data BYTEA,              -- Binary gambar
    image_filename VARCHAR(255),   -- Nama file
    image_mimetype VARCHAR(100),   -- MIME type
    
    FOREIGN KEY (author) REFERENCES users(username)
);
```

### Contoh Query:

```sql
-- Cek artikel yang punya gambar
SELECT id, title, author, 
       CASE WHEN image_data IS NOT NULL THEN 'Yes' ELSE 'No' END as has_image
FROM news
WHERE status = 'published';

-- Cek ukuran total gambar
SELECT 
    COUNT(*) as total_images,
    pg_size_pretty(SUM(length(image_data))) as total_size
FROM news
WHERE image_data IS NOT NULL;

-- Get artikel dengan gambar
SELECT id, title, author, image_filename, image_mimetype,
       length(image_data) as image_size
FROM news
WHERE image_data IS NOT NULL;
```

---

## 🐛 TROUBLESHOOTING

### Error: "Module 'PIL' not found"
```bash
pip install Pillow
```

### Error: "Image too large"
- Resize gambar sebelum upload
- Max 5MB per file
- Gunakan online tool untuk compress

### Error: "Failed to save image"
- Cek koneksi database
- Cek migration sudah dijalankan
- Cek kolom `image_data` exists di tabel `news`

### Gambar tidak muncul di User Dashboard
- Cek fungsi `get_news_image()` sudah dipanggil
- Cek QPixmap conversion
- Cek image_data tidak NULL di database

### Database size membengkak
- Normal, gambar disimpan sebagai BLOB
- Solusi: Cleanup old images
- Atau migrate ke file system / cloud storage

---

## 💡 TIPS & BEST PRACTICES

### 1. Compress Gambar
```python
# Di kode, gambar otomatis di-compress quality 85%
image.save(buffer, format='JPEG', quality=85, optimize=True)
```

### 2. Resize Large Images
```python
# Auto resize jika > 1920px width
if image.width > 1920:
    ratio = 1920 / image.width
    new_height = int(image.height * ratio)
    image = image.resize((1920, new_height), Image.LANCZOS)
```

### 3. Supported Formats
- ✅ JPEG (.jpg, .jpeg) - Best for photos
- ✅ PNG (.png) - Best for graphics/logos  
- ✅ GIF (.gif) - Animated images
- ✅ BMP (.bmp) - High quality
- ❌ WebP - Not yet supported
- ❌ SVG - Not supported (vector)

### 4. Performance
- Use index pada `image_filename`
- Lazy load images di User Dashboard
- Cache images di client side

### 5. Security
- Validate file type dari MIME
- Max size limit (5MB)
- Sanitize filename
- No executable files allowed

---

## 📈 FUTURE ENHANCEMENTS

### Phase 2:
- [ ] Multiple images per artikel (gallery)
- [ ] Image crop/edit tool
- [ ] Drag & drop upload
- [ ] Thumbnail generation
- [ ] Image optimization auto

### Phase 3:
- [ ] Cloud storage integration (S3/Cloudinary)
- [ ] CDN for faster loading
- [ ] Image analytics (views, clicks)
- [ ] Lazy loading infinite scroll
- [ ] WebP format support

---

## 📝 CHANGELOG

### v1.0 (Dec 2025)
- ✅ Basic image upload
- ✅ Preview before publish
- ✅ BLOB storage in PostgreSQL
- ✅ Auto resize large images
- ✅ Format validation
- ✅ Size limit 5MB

---

## 🙏 CREDITS

Developed by: **Muhreza12**  
Project: **Crypto Insight - Cyberpunk Edition**  
Course: **Sistem Operasi - Multi User Project**  

---

## 📞 SUPPORT

Jika ada pertanyaan atau issue:
1. Check troubleshooting section
2. Review kode di `app_db_fixed.py`
3. Check SQL migration sudah run
4. Test dengan gambar kecil dulu (< 1MB)

Good luck! 🚀
