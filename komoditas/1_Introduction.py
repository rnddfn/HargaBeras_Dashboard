import streamlit as st

st.set_page_config(page_title="Home | Dashboard Komoditas", layout="wide")

st.markdown("""
<style>
.block-container {padding:1rem 2rem;}
</style>
""", unsafe_allow_html=True)

st.title("Dashboard Harga Komoditas Beras Sulawesi Utara")
st.header("""
Selamat datang di Dashboard Analisis Harga Komoditas Sulawesi Utara.  
""")

st.markdown("---")

col1, col2 = st.columns([2, 1])
with col1:
    st.header("Studi Kasus:")
    st.markdown(
    """
    <p style='text-align: justify; font-size:20px;'>
    Studi kasus yang diangkat adalah harga komoditas beras di Sulawesi Utara pada periode 2020-2025. 
    Pemilihan beras sebagai fokus studi didasari oleh fakta bahwa Indonesia merupakan salah satu 
    konsumen beras terbesar di dunia, menempati peringkat ke-3 secara global. <br><br>Dalam beberapa tahun terakhir, 
    terjadi kenaikan harga beras yang signifikan, termasuk di Provinsi Sulawesi Utara, 
    yang berpotensi berdampak pada daya beli masyarakat. Fluktuasi harga juga dapat menimbulkan inflasi, untuk itu upaya pemerintah daerah adalah menjaga harga pangan tetap stabil dan terjangkau []. 
    Adanya visualisasi data memungkinkan pemerintah melihat data historis terkait harga komoditas beras sehingga dapat mengambil keputusan berbasis data.
    </p>
    """,
    unsafe_allow_html=True
)

with col2:
    st.image("resources/sawah.jpg", width=1000)

st.markdown("---")

st.header("Tujuan Dashboard")
st.markdown(
"""
<p style='text-align: justify; font-size:20px;'>
Dashboard ini hadir untuk menjawab 3 pertanyaan spesifik <br>
1.	Bagaimana tren harga beras di Sulawesi Utara dari tahun 2020 - 2025? <br>
2.	Pada periode atau musim apa harga beras cenderung mencapai rata-rata tertinggi? <br>
3.	Faktor eksternal apa yang memiliki korelasi/pengaruh terhadap perubahan harga beras?
""",
unsafe_allow_html=True)

st.markdown("---")

st.header("Data yang Digunakan")
st.markdown(
    """
    <p style='text-align: justify; font-size:20px;'>
        Data yang digunakan dalam projek ini adalah data harga komoditas beras di provinsi Sulawesi Utara dari tahun 2020 - 2025 yang berasal dari kaggle yang diperbarui setiap bulan.
        Berikut adalah tautan ke data tersebut:
        <a href='https://www.kaggle.com/datasets/rickymambu/commodities/data' target='_blank'>
            https://www.kaggle.com/datasets/rickymambu/commodities/data
        </a>.
    </p>
    """, unsafe_allow_html=True)

st.info("➡️ Gunakan menu di sidebar kiri untuk membuka halaman Dashboard.")