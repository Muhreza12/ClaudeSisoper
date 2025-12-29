-- migration_add_image_column.sql
-- Menambahkan kolom image_data ke tabel news untuk fitur upload foto

-- Tambah kolom untuk menyimpan gambar sebagai BYTEA (binary data)
ALTER TABLE news 
ADD COLUMN IF NOT EXISTS image_data BYTEA;

-- Tambah kolom untuk menyimpan nama file gambar
ALTER TABLE news 
ADD COLUMN IF NOT EXISTS image_filename VARCHAR(255);

-- Tambah kolom untuk menyimpan tipe MIME gambar
ALTER TABLE news 
ADD COLUMN IF NOT EXISTS image_mimetype VARCHAR(100);

-- Tambah index untuk performa
CREATE INDEX IF NOT EXISTS idx_news_has_image ON news(image_filename) WHERE image_filename IS NOT NULL;

-- Komentar
COMMENT ON COLUMN news.image_data IS 'Binary data gambar artikel (JPEG/PNG)';
COMMENT ON COLUMN news.image_filename IS 'Nama file gambar original';
COMMENT ON COLUMN news.image_mimetype IS 'MIME type gambar (image/jpeg, image/png, dll)';

-- Selesai! 
-- Jalankan migration ini di Railway PostgreSQL Query Console
