import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from openai import OpenAI
from dotenv import load_dotenv
import os
import io

load_dotenv()

# -------- Page config --------
st.set_page_config(
    page_title="Dashboard Intelligence - Erlangga",
    page_icon="📊",
    layout="wide",
)

# -------- Required columns --------
REQUIRED_COLUMNS = {
    "order_id":     "ID unik per transaksi",
    "date":         "Tanggal transaksi (YYYY-MM-DD)",
    "product":      "Nama produk",
    "category":     "Kategori produk",
    "qty":          "Jumlah unit terjual (angka)",
    "revenue":      "Total pendapatan transaksi (angka, Rupiah)",
    "channel":      "Channel penjualan (Tokopedia, Shopee, dll)",
    "city":         "Kota pembeli",
    "discount_pct": "Persentase diskon (0-100)",
    "rating":       "Rating produk (1.0-5.0)",
}

# -------- Helpers --------
@st.cache_data
def load_default_data():
    # data default untuk ditampilkan saat belum upload file
    df = pd.read_csv("data/sales_data.csv", parse_dates=["date"])
    return df

def validate_and_enrich(df):
    """Validate columns and add month/month_num if missing."""
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        return df, missing
    df["date"] = pd.to_datetime(df["date"])
    if "month" not in df.columns:
        df["month"] = df["date"].dt.strftime("%B")
    if "month_num" not in df.columns:
        df["month_num"] = df["date"].dt.month
    return df, []

def get_template_csv():
    df = load_default_data().head(5)
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return buf.getvalue()

# -------- Sidebar -------- 
with st.sidebar:
    st.header("Data Source")
    upload_mode = st.radio(
        "Pilih sumber data:",
        ["Sample Data (default)", "Upload CSV saya"],
        index=0,
    )

    if upload_mode == "Upload CSV saya":
        st.markdown("**Kolom yang dibutuhkan:**")
        for col, desc in REQUIRED_COLUMNS.items():
            st.markdown(f"- `{col}` — {desc}")

        st.download_button(
            label="Download Template CSV",
            data=get_template_csv(),
            file_name="template_sales.csv",
            mime="text/csv",
            use_container_width=True,
        )

        uploaded_file = st.file_uploader("Upload CSV kamu:", type=["csv"])

        if uploaded_file:
            try:
                df_raw = pd.read_csv(uploaded_file)
                df, missing = validate_and_enrich(df_raw)
                if missing:
                    st.error("Kolom tidak lengkap. Yang kurang:\n\n" +
                             "\n".join([f"- `{c}`" for c in missing]))
                    st.info("Download template di atas sebagai referensi.")
                    df = load_default_data()
                    st.caption("Menampilkan sample data.")
                else:
                    st.success(f"{len(df):,} rows loaded dari {uploaded_file.name}")
            except Exception as e:
                st.error(f"Gagal baca file: {str(e)}")
                df = load_default_data()
        else:
            df = load_default_data()
            st.caption("Belum ada file — menampilkan sample data.")
    else:
        df = load_default_data()
        st.caption("Menggunakan sample data e-commerce 2024.")

# -------- Header --------
st.title("Dashboard Intelligence - Erlangga")
st.caption("E-Commerce · Natural Language Analytics")
st.divider()

# -------- KPI Cards --------
total_revenue   = df["revenue"].sum()
total_orders    = len(df)
avg_order_value = df["revenue"].mean()
top_channel     = df.groupby("channel")["revenue"].sum().idxmax()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Revenue",   f"Rp {total_revenue:,.0f}")
k2.metric("Total Orders",    f"{total_orders:,}")
k3.metric("Avg Order Value", f"Rp {avg_order_value:,.0f}")
k4.metric("Top Channel",     top_channel)

st.divider()

# -------- Charts row 1 -------- 
c1, c2 = st.columns(2)

with c1:
    st.subheader("Revenue per Bulan")
    monthly = (
        df.groupby(["month_num", "month"])["revenue"]
        .sum()
        .reset_index()
        .sort_values(by="month_num")
    )
    fig_monthly = px.bar(
        monthly, x="month", y="revenue",
        color="revenue", color_continuous_scale="Blues",
        labels={"revenue": "Revenue (Rp)", "month": "Bulan"},
    )
    fig_monthly.update_layout(showlegend=False, coloraxis_showscale=False,
                               margin=dict(t=10, b=10), yaxis_tickformat=",")
    st.plotly_chart(fig_monthly, use_container_width=True)

with c2:
    st.subheader("Revenue per Channel")
    channel_df = df.groupby("channel")["revenue"].sum().reset_index()
    fig_channel = px.pie(
        channel_df, values="revenue", names="channel",
        color_discrete_sequence=px.colors.sequential.Blues_r,
        hole=0.4,
    )
    fig_channel.update_layout(margin=dict(t=10, b=10))
    st.plotly_chart(fig_channel, use_container_width=True)

# -------- Charts row 2 -------- 
c3, c4 = st.columns(2)

with c3:
    st.subheader("Top 10 Produk")
    top_products = (
        df.groupby("product")["revenue"]
        .sum()
        .sort_values(ascending=True)
        .tail(10)
        .reset_index()
    )
    fig_prod = px.bar(
        top_products, x="revenue", y="product", orientation="h",
        color="revenue", color_continuous_scale="Teal",
        labels={"revenue": "Revenue (Rp)", "product": ""},
    )
    fig_prod.update_layout(showlegend=False, coloraxis_showscale=False,
                            margin=dict(t=10, b=10), xaxis_tickformat=",")
    st.plotly_chart(fig_prod, use_container_width=True)

with c4:
    st.subheader("Revenue per Kota")
    city_df = (
        df.groupby("city")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig_city = px.bar(
        city_df, x="city", y="revenue",
        color="revenue", color_continuous_scale="Purples",
        labels={"revenue": "Revenue (Rp)", "city": "Kota"},
    )
    fig_city.update_layout(showlegend=False, coloraxis_showscale=False,
                            margin=dict(t=10, b=10), yaxis_tickformat=",")
    st.plotly_chart(fig_city, use_container_width=True)

st.divider()

# -------- LLM Chat -------- 
st.subheader("💬 Ask Your Data")
st.caption("Tanya insight apapun tentang data penjualan ini pakai bahasa indonesia.")

# data saat ini sudah diolah jadi text context untuk LLM, jadi saat tanya tinggal jawab tanpa proses ulang data
# belum bisa buat context yang benar-benar dinamis (misal buat chart on the fly) karena keterbatasan token, jadi kita buat summary statis yang cukup komprehensif untuk cover banyak pertanyaan umum

@st.cache_data
def build_context(df_hash, df):
    monthly_rev = (df.groupby(["month_num","month"])["revenue"].sum()
                   .reset_index().sort_values("month_num")
                   .set_index("month")["revenue"])
    top_prod    = df.groupby("product")["revenue"].sum().sort_values().tail(5)
    channel_rev = df.groupby("channel")["revenue"].sum().sort_values()
    city_rev    = df.groupby("city")["revenue"].sum().sort_values().tail(5)
    cat_rev     = df.groupby("category")["revenue"].sum().sort_values()
    avg_disc    = df.groupby("product")["discount_pct"].mean().sort_values().tail(5)
    prod_city   = (df.groupby(["city", "product"])["revenue"].sum()
                   .reset_index()
                   .sort_values(["city", "revenue"], ascending=[True, False])
                   .groupby("city").head(3)
                   .to_string(index=False))

    return f"""
Kamu adalah analis data senior. Jawab pertanyaan berdasarkan data berikut secara langsung, tajam, dan actionable.

=== DATASET OVERVIEW ===
- Total orders: {len(df):,}
- Total revenue: Rp {df['revenue'].sum():,.0f}
- Periode: {df['date'].min().strftime('%d %b %Y')} – {df['date'].max().strftime('%d %b %Y')}
- Avg order value: Rp {df['revenue'].mean():,.0f}
- Avg rating: {df['rating'].mean():.2f}

=== REVENUE PER BULAN ===
{monthly_rev.to_string()}

=== TOP 5 PRODUK (by revenue) ===
{top_prod.to_string()}

=== REVENUE PER CHANNEL ===
{channel_rev.to_string()}

=== TOP 5 KOTA ===
{city_rev.to_string()}

=== REVENUE PER KATEGORI ===
{cat_rev.to_string()}

=== TOP 5 PRODUK DISKON TERBESAR (avg %) ===
{avg_disc.to_string()}

=== TOP 3 PRODUK PER KOTA ===
{prod_city}

=== SAMPLE 10 ROWS ===
{df.sample(10, random_state=42)[['date','product','category','qty','revenue','channel','city','discount_pct']].to_string(index=False)}
""".strip()

# Use df length+hash as cache key so context rebuilds on new upload
df_hash = len(df)
context = build_context(df_hash, df)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if not st.session_state.messages:
    st.markdown("**Coba tanya:**")
    col1, col2, col3 = st.columns(3)
    suggestions = [
        "Bulan mana penjualan tertinggi dan kenapa?",
        "Channel mana yang paling efisien?",
        "Produk mana yang perlu di-boost?",
    ]
    for col, suggestion in zip([col1, col2, col3], suggestions):
        if col.button(suggestion, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": suggestion})
            st.rerun()

if prompt := st.chat_input("Tanya tentang data penjualan..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key or api_key == "sk-your-key-here":
                    response_text = "API key belum diset. Buka file `.env` dan isi `OPENAI_API_KEY`."
                else:
                    client = OpenAI(api_key=api_key)
                    response = client.chat.completions.create(
                        model="gpt-4.1-nano",
                        messages=[
                            {"role": "system", "content": context},
                            *[{"role": m["role"], "content": m["content"]}
                              for m in st.session_state.messages],
                        ],
                        max_tokens=600,
                        temperature=0.3,
                    )
                    response_text = response.choices[0].message.content
            except Exception as e:
                response_text = f" Error: {str(e)}"

        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})

if st.session_state.messages:
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()
