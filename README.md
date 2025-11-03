# Jasa Raharja PDF to Excel Converter

**Automated PDF to Excel Conversion with Smart Data Transformation**

Aplikasi konversi PDF ke Excel yang dirancang khusus untuk mengotomatisasi proses ekstraksi, transformasi, dan loading (ETL) data Jasa Raharja. Aplikasi ini tidak hanya mengekstrak tabel dari PDF, tetapi juga secara otomatis mentransformasi data sesuai format standar yang siap digunakan untuk visualisasi dan pengambilan keputusan.

---

## Instalasi

### Kebutuhan Sistem
- Python 3.8 atau lebih tinggi
- Koneksi internet untuk instalasi dependency

### Langkah Instalasi

1. Clone atau download repository ini

2. Install dependencies Python:
```bash
pip install -r requirements.txt
```

3. Install system dependencies:

**Untuk Linux/Ubuntu:**
```bash
sudo apt-get update
sudo apt-get install python3-tk ghostscript
```

**Untuk macOS:**
```bash
brew install ghostscript tcl-tk
```

4. Jalankan aplikasi:
```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser pada http://localhost:8501

---

## Cara Penggunaan

### Langkah 1: Upload File PDF
Upload file PDF yang mengandung tabel data

### Langkah 2: Konfigurasi
- Pilih halaman yang akan diproses (semua atau halaman tertentu)
- Pilih mode ekstraksi:
  - **Lattice**: untuk tabel dengan garis pembatas
  - **Stream**: untuk tabel tanpa garis pembatas

### Langkah 3: Konversi
- Masukkan nama file output
- Klik tombol "Konversi ke Excel"
- Review hasil ekstraksi dan accuracy score

### Langkah 4: Download
Download file Excel yang sudah siap digunakan untuk analisis

---

## Alur Kerja Sistem

```
PDF File → Extraction → Transformation → Excel File
            (Camelot)    (Auto Format)    (Ready to Use)
```

### Proses Transformasi
1. Deteksi header kolom otomatis
2. Pembersihan baris duplikat
3. Eliminasi kolom kosong
4. Standardisasi format angka
5. Konversi tipe data
6. Penyesuaian dengan format Jasa Raharja

---

## Troubleshooting

**Tidak ada tabel yang terdeteksi:**
- Coba ganti mode ekstraksi (lattice ke stream atau sebaliknya)
- Pastikan PDF tidak berupa hasil scan image
- Periksa kualitas dan kejernihan PDF

**Hasil ekstraksi kurang akurat:**
- Periksa accuracy score pada preview
- Gunakan mode lattice untuk tabel bergaris
- Gunakan mode stream untuk tabel tanpa garis

**Format angka tidak sesuai:**
- Sistem otomatis mengkonversi koma menjadi titik desimal
- Untuk format khusus, dapat dilakukan penyesuaian pada kode

---

## Dependencies

- streamlit - Framework aplikasi web
- camelot-py - Library ekstraksi tabel PDF
- pandas - Library manipulasi data
- openpyxl - Library untuk membuat file Excel
- opencv-python - Library pemrosesan gambar

---

## Struktur Project

```
jasa-raharja-pdf-converter/
├── app.py                # Aplikasi utama
├── requirements.txt      # Python dependencies
├── README.md            # Dokumentasi
```

---

**Built for Jasa Raharja - Transforming PDF Data into Actionable Insights**
