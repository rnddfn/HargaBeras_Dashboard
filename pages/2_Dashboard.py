import streamlit as st
import pandas as pd
import plotly.express as px
import warnings
import plotly.graph_objects as go
# import altair as alt  <-- DIHAPUS (Tidak terpakai)

warnings.filterwarnings("ignore")

# Pengaturan halaman
st.set_page_config(layout="wide", page_title="Dashboard Harga Komoditas Sulut")

def apply_global_style(fig):
    """Menerapkan styling konsisten untuk semua chart Plotly."""
    fig.update_layout(
        font_family="Poppins",
        font_color="#333333",
        font_size=14,
        title_font=dict(family="Poppins", size=22, color="#000000"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            font=dict(size=13)
        ),
        xaxis=dict(
            title_font=dict(size=16, family="Segoe UI", color="#444"),
        ),
        yaxis=dict(
            title_font=dict(size=16, family="Segoe UI", color="#444"),
        )
    )
    return fig

# CSS 
st.markdown("""
<style>
.block-container {padding:1rem 2rem;}
</style>
""", unsafe_allow_html=True)
st.title("📊 Dashboard Analisis Harga Komoditas Sulut")

# Load data
@st.cache_data
def load_data(path):
    df = pd.read_csv(path, parse_dates=["Tanggal"])
    return df

df = load_data("output.csv")

# Sidebar Filter
with st.sidebar:
    st.title("⚙️ Filter Dashboard")

    # --- Filter Tanggal ---
    with st.expander("📅 Pilih Tanggal", expanded=True):
        min_date = df['Tanggal'].min().date() # Konversi ke .date() untuk st.date_input
        max_date = df['Tanggal'].max().date()
        start_date = st.date_input("Dari tanggal:", min_value=min_date, max_value=max_date, value=min_date)
        end_date = st.date_input("Sampai tanggal:", min_value=min_date, max_value=max_date, value=max_date)

    # --- Filter Musim ---
    with st.expander("🌤️ Musim", expanded=True):
        if 'season' in df.columns:
            seasons = df['season'].unique().tolist()
            season_filter = st.multiselect("Pilih musim:", options=seasons, default=seasons)
        else:
            st.warning("Kolom 'season' tidak ditemukan.")
            season_filter = [] # Kosongkan filter jika kolom tidak ada

    # Footer sidebar diganti ke st.caption
    st.caption("© 2025 Dashboard Harga Komoditas")

# Filter data berdasarkan input sidebar
start_datetime = pd.to_datetime(start_date)
end_datetime = pd.to_datetime(end_date)
filter_tanggal = (df['Tanggal'] >= start_datetime) & (df['Tanggal'] <= end_datetime)

if 'season' in df.columns and season_filter:
    filter_musim = df['season'].isin(season_filter)
    df_filtered = df.loc[filter_tanggal & filter_musim].copy()
else:
    df_filtered = df.loc[filter_tanggal].copy()

if not df_filtered.empty:
    df_filtered.loc[:, 'perc_change'] = (df_filtered['daily_delta'] / df_filtered['lag_1'] * 100).fillna(0)
else:
    df_filtered['perc_change'] = pd.Series(dtype='float64')

st.markdown("---")
st.header("🏆 KPI Utama")

if not df_filtered.empty:
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        avg_price = df_filtered['prices'].mean()
        st.metric("Harga Rata-rata", f"Rp {avg_price:,.0f}")
    with col2:
        max_price = df_filtered['prices'].max()
        st.metric("Harga Tertinggi", f"Rp {max_price:,.0f}")
    with col3:
        min_price = df_filtered['prices'].min()
        st.metric("Harga Terendah", f"Rp {min_price:,.0f}")
    with col4:
        price_std = df_filtered['prices'].std()
        st.metric("Std Deviasi", f"Rp {price_std:,.0f}")
    with col5:
        if 'perc_change_7d' in df_filtered.columns and not df_filtered['perc_change_7d'].dropna().empty:
            last_7d = df_filtered['perc_change_7d'].iloc[-1]
            st.metric("Perubahan 7 Hari", f"{last_7d:.2f}%", delta=f"{last_7d:.2f}%")
        else:
            st.metric("Perubahan 7 Hari", "N/A")
    with col6:
        if 'perc_change_30d' in df_filtered.columns and not df_filtered['perc_change_30d'].dropna().empty:
            last_30d = df_filtered['perc_change_30d'].iloc[-1]
            st.metric("Perubahan 30 Hari", f"{last_30d:.2f}%", delta=f"{last_30d:.2f}%")
        else:
            st.metric("Perubahan 30 Hari", "N/A")
else:
    st.warning("Tidak ada data untuk rentang filter yang dipilih.")

st.markdown("---")

# Chart Utama (Tren Harga)
st.header("Tren Harga Beras") 
col1, col2 = st.columns([4, 1])

with col1:
    with st.container(border=True):
        fig_main = go.Figure()
        
        if not df_filtered.empty:
            fig_main.add_trace(go.Scatter(
                x=df_filtered['Tanggal'], y=df_filtered['prices'], name='Harga Aktual',
                line=dict(color='#344F1F', width=2), mode='lines'
            ))
            if 'rolling_mean_7_custom' in df_filtered.columns:
                fig_main.add_trace(go.Scatter(
                    x=df_filtered['Tanggal'], y=df_filtered['rolling_mean_7_custom'], name='MA 7 Hari',
                    line=dict(color='#f59e0b', width=2, dash='dash')
                ))
            if 'rolling_mean_30_custom' in df_filtered.columns:
                fig_main.add_trace(go.Scatter(
                    x=df_filtered['Tanggal'], y=df_filtered['rolling_mean_30_custom'], name='MA 30 Hari',
                    line=dict(color='#A72703', width=2, dash='dot')
                ))

        fig_main.update_layout(
            title='Tren Harga Beras dengan Moving Average',
            xaxis_title='Tanggal',
            yaxis_title='Harga (Rp)',
            hovermode='x unified',
            height=550
        )
        fig_main = apply_global_style(fig_main) # Terapkan style global
        st.plotly_chart(fig_main, use_container_width=True)

with col2:
    st.subheader("Statistik Ringkas")
    if not df_filtered.empty:
        stats_df = pd.DataFrame({
            'Metrik': ['Mean', 'Median', 'Q1', 'Q3', 'IQR', 'Range'],
            'Nilai': [
                f"Rp {df_filtered['prices'].mean():,.0f}",
                f"Rp {df_filtered['prices'].median():,.0f}",
                f"Rp {df_filtered['prices'].quantile(0.25):,.0f}",
                f"Rp {df_filtered['prices'].quantile(0.75):,.0f}",
                f"Rp {df_filtered['prices'].quantile(0.75) - df_filtered['prices'].quantile(0.25):,.0f}",
                f"Rp {df_filtered['prices'].max() - df_filtered['prices'].min():,.0f}"
            ],
        })
        st.dataframe(stats_df, hide_index=True)
    else:
        st.info("Data kosong.")

st.markdown("---")

st.header("🌤️ Harga Beras Musiman")
# Analisis Musiman (Bulan & Musim)
if not df_filtered.empty and 'season' in df_filtered.columns:
    df_monthly = df_filtered.groupby('month')['prices'].mean().reset_index().sort_values('prices', ascending=False)
    df_season = df_filtered.groupby('season')['prices'].mean().reset_index().sort_values('prices', ascending=False)

    min_y = min(df_monthly['prices'].min(), df_season['prices'].min()) * 0.98
    max_y = max(df_monthly['prices'].max(), df_season['prices'].max()) * 1.02
    y_range = [min_y, max_y]

    fig_bar_month = px.bar(
        df_monthly, x='month', y='prices', text='prices',
        title="Harga Rata-rata per Bulan",
        labels={'month':'Bulan', 'prices':'Harga Rata-rata (Rp)'},
        color='prices', color_continuous_scale='greens'
    )
    fig_bar_month.update_traces(texttemplate='Rp %{text:,.0f}', textposition='outside')
    fig_bar_month.update_layout(
        yaxis=dict(title='Harga Rata-rata (Rp)', range=y_range),
        xaxis=dict(title='Bulan')
    )
    fig_bar_month = apply_global_style(fig_bar_month)
    st.plotly_chart(fig_bar_month, use_container_width=True)

    fig_bar_season = px.bar(
        df_season, x='season', y='prices', text='prices',
        title="Harga Rata-rata per Musim",
        labels={'season':'Musim', 'prices':'Harga Rata-rata (Rp)'},
        color_discrete_sequence=['#3CB371']
    )
    fig_bar_season.update_traces(texttemplate='Rp %{text:,.0f}', textposition='outside')
    fig_bar_season.update_layout(
        yaxis=dict(title='Harga Rata-rata (Rp)', range=y_range),
        xaxis=dict(title='Musim')
    )
    fig_bar_season = apply_global_style(fig_bar_season)
    st.plotly_chart(fig_bar_season, use_container_width=True)

st.markdown("---")
st.header("📊 Distribusi Harga")
col1, col2 = st.columns(2)

with col1:
    fig_hist = px.histogram(
        df_filtered, x='prices', nbins=30, title="Histogram Harga",
        color_discrete_sequence=['#F4991A']
    )
    fig_hist = apply_global_style(fig_hist)
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    fig_box = px.box(
        df_filtered, y='prices', title="Boxplot Harga",
        color_discrete_sequence=['#F4991A']
    )
    fig_box = apply_global_style(fig_box)
    st.plotly_chart(fig_box, use_container_width=True)

st.markdown("---")
st.header("🌤️ Analisis Faktor Eksternal")
col1, col2, col3 = st.columns(3)

with col1:
    fig_temp = px.scatter(
        df_filtered, x='Temperature', y='prices', color='Temperature',
        trendline="ols", color_continuous_scale=[(0, "#A5D6A7"), (0.5, "#66BB6A"), (1, "#2E7D32")],
        title="Harga vs Temperatur"
    )
    fig_temp.update_traces(marker=dict(size=8, opacity=0.8))
    fig_temp.update_coloraxes(colorbar_title="Suhu (°C)")
    fig_temp = apply_global_style(fig_temp)
    st.plotly_chart(fig_temp, use_container_width=True)

with col2:
    fig_rain = px.scatter(
        df_filtered, x='Curah Hujan', y='prices', color='Curah Hujan',
        trendline="ols", color_continuous_scale=[(0, "#C8E6C9"), (0.5, "#81C784"), (1, "#2E7D32")],
        title="Harga vs Curah Hujan"
    )
    fig_rain.update_traces(marker=dict(size=8, opacity=0.8))
    fig_rain.update_coloraxes(colorbar_title="Curah Hujan (mm)")
    fig_rain = apply_global_style(fig_rain)
    st.plotly_chart(fig_rain, use_container_width=True)

with col3:
    fig_hum = px.scatter(
        df_filtered, x='Kelembapan', y='prices', color='Kelembapan',
        trendline="ols", color_continuous_scale=[(0, "#C8E6C9"), (0.5, "#66BB6A"), (1, "#1B5E20")],
        title="Harga vs Kelembapan"
    )
    fig_hum.update_traces(marker=dict(size=8, opacity=0.8))
    fig_hum.update_coloraxes(colorbar_title="Kelembapan (%)")
    fig_hum = apply_global_style(fig_hum)
    st.plotly_chart(fig_hum, use_container_width=True)

st.markdown("---")
st.header("🌡️ Heatmap Korelasi Faktor terhadap Harga Beras")

corr_cols = [
    'prices', 'Temperature', 'Curah Hujan', 'Kelembapan',
    'Inflasi_total', 'cpi', 'usd_idr', 'perc_change_7d', 'perc_change_30d'
]
existing_corr_cols = [col for col in corr_cols if col in df_filtered.columns]

if not df_filtered[existing_corr_cols].empty:
    corr_matrix = df_filtered[existing_corr_cols].corr()
    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale='RdYlGn',
        title="Korelasi antara Harga, Cuaca, dan Indikator Ekonomi",
        aspect="auto"
    )
    fig_corr = apply_global_style(fig_corr)
    st.plotly_chart(fig_corr, use_container_width=True)
else:
    st.info("Data tidak cukup untuk menampilkan heatmap korelasi.")

st.markdown("---")
st.header("📊 Distribusi Lonjakan Harga Harian (Deteksi Anomali)")

fig_box_delta = px.box(
    df_filtered, 
    y='daily_delta', 
    title="Boxplot Perubahan Harga Harian",
    color_discrete_sequence=['#F4991A'] 
)
fig_box_delta = apply_global_style(fig_box_delta)
st.plotly_chart(fig_box_delta, use_container_width=True)