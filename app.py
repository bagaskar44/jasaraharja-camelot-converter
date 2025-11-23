import streamlit as st
import camelot
import pandas as pd
import io
import tempfile
import os

# Konfigurasi halaman
st.set_page_config(
    page_title="PDF to Excel Converter",
    page_icon="📄",
    layout="centered"
)

# Header
st.title("📄 Automation Converter")
st.markdown("Data siap dianalisis dalam satu kali klik!")

# File uploader
uploaded_file = st.file_uploader(
    "Upload file PDF",
    type=['pdf'],
    help="Pilih file PDF yang mengandung tabel"
)

if uploaded_file is not None:
    # Opsi tambahan
    st.subheader("⚙️ Pengaturan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        pages_option = st.selectbox(
            "Halaman yang akan diproses",
            ["Semua halaman", "Halaman tertentu"],
            help="Pilih halaman yang ingin dikonversi"
        )
    
    with col2:
        if pages_option == "Halaman tertentu":
            pages_input = st.text_input(
                "Nomor halaman",
                placeholder="Contoh: 1-3, 5, 7",
                help="Gunakan format: 1-3 untuk range, atau 1,2,3 untuk halaman spesifik"
            )
        else:
            pages_input = 'all'
    
    # Pilihan mode ekstraksi
    st.markdown("**Mode Ekstraksi:**")
    flavor_display = st.radio(
        "Pilih metode ekstraksi tabel",
        ["PDF Bergaris", "PDF Teks"],
        help="Lattice: untuk tabel dengan garis pembatas | Stream: untuk tabel tanpa garis",
        horizontal=True
    )
    
    if flavor_display == 'PDF Bergaris':
        flavor = "lattice"
    else:
        flavor = "stream"
    
    # Input nama file
    output_filename = st.text_input(
        "Nama file output",
        value="converted_tables",
        help="Nama file Excel yang akan didownload (tanpa ekstensi .xlsx)"
    )
    
    # Tombol konversi
    if st.button("🔄 Konversi ke Excel", type="primary"):
        with st.spinner("Sedang memproses PDF..."):
            try:
                # Simpan file upload ke temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                # Baca tabel dari PDF menggunakan Camelot
                if pages_option == "Semua halaman":
                    tables = camelot.read_pdf(tmp_path, pages='all', flavor=flavor)
                else:
                    tables = camelot.read_pdf(tmp_path, pages=pages_input, flavor=flavor)
                
                # Hapus temporary file
                os.unlink(tmp_path)
                
                # Cek apakah ada tabel yang ditemukan
                if not tables or len(tables) == 0:
                    st.warning("⚠️ Tidak ada tabel yang ditemukan dalam PDF.")
                    st.info(f"💡 Coba ganti mode ekstraksi dari '{flavor}' ke '{'stream' if flavor == 'lattice' else 'lattice'}'")
                else:
                    st.success(f"✅ Berhasil menemukan {len(tables)} tabel!")
                    
                    # Preview tabel dengan accuracy score
                    st.subheader("📊 Preview Tabel")
                    for i, table in enumerate(tables):
                        df = table.df
                        accuracy = table.accuracy
                        
                        with st.expander(f"Tabel {i+1} - {len(df)} baris × {len(df.columns)} kolom (Accuracy: {accuracy:.1f}%)"):
                            st.dataframe(df, use_container_width=True)
                    
                    # Buat Excel file di memory
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        # Gabungkan semua tabel menjadi satu
                        all_dfs = []
                        for i, table in enumerate(tables):
                            df = table.df
                            
                            # Baris kedua jadi header
                            df.columns = df.iloc[1] 
                            # Buang baris kedua
                            df = df.drop(index=1).reset_index(drop=True)
                            
                            # Dataframe setelah pertama hapus header
                            if i >= 1:
                                df = df.drop(df.index[:1])
                                
                            # Bersihkan kolom kosong
                            df = df.dropna(axis=1, how="all")
                            # Konversi angka
                            for col in df.columns[1:]:
                                df[col] = df[col].str.replace(",", ".", regex=False)
                                df[col] = pd.to_numeric(df[col], errors="ignore")
                            
                            all_dfs.append(df)
                            
                        # Gabungkan semua dataframe
                        combined_df = pd.concat(all_dfs, ignore_index=True)
                        combined_df.to_excel(writer, sheet_name='All_Tables', index=False)
                    
                    output.seek(0)
                    
                    # Tombol download
                    st.subheader("💾 Download Hasil")
                    st.download_button(
                        label="📥 Download Excel File",
                        data=output,
                        file_name=f"{output_filename}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        type="primary"
                    )
                    
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan: {str(e)}")
                st.info("💡 Tips: Pastikan PDF mengandung tabel yang terstruktur dengan baik dan coba ganti mode ekstraksi")

else:
    # Instruksi penggunaan
    st.info("👆 Upload file PDF untuk memulai konversi")
    
    with st.expander("ℹ️ Cara Penggunaan"):
        st.markdown("""
        1. **Upload file PDF** yang mengandung tabel
        2. **Pilih halaman** yang ingin dikonversi (opsional)
        3. **Pilih mode ekstraksi:**
           - **Lattice**: Untuk tabel dengan garis pembatas (lebih akurat)
           - **Stream**: Untuk tabel tanpa garis/hanya spasi
        4. Klik tombol **Konversi ke Excel**
        5. **Preview tabel** yang berhasil diekstrak (dengan skor akurasi)
        6. **Download file Excel** hasil konversi
        
        **Catatan:**
        - Aplikasi ini menggunakan Camelot untuk ekstraksi tabel
        - Accuracy score menunjukkan tingkat kepercayaan ekstraksi
        - Jika hasil kurang memuaskan, coba ganti mode ekstraksi
        - Setiap tabel akan disimpan di sheet terpisah
        """)
    
    with st.expander("📦 Instalasi Dependencies"):
        st.code("""
pip install camelot-py[cv]
pip install streamlit pandas openpyxl

# Untuk Linux, mungkin perlu:
apt-get install python3-tk ghostscript
        """, language="bash")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit • Powered by Camelot")
