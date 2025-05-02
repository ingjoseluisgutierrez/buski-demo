
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="Buski - Comparador de Ofertas",
    page_icon="🔎",
    layout="wide"
)

st.image("buski_logo.png", width=220)
st.title("🔎 Buski")
st.markdown("*Tu comparador de precios inteligente.*")
st.markdown("Encuentra en un solo lugar las mejores ofertas de Mercado Libre, Alkosto y Éxito.")

# Conexión a la base de datos
conn = sqlite3.connect("offers.db")
query = "SELECT tienda, nombre_producto, precio, url, fecha_consulta FROM offers ORDER BY fecha_consulta DESC"
df = pd.read_sql_query(query, conn)

# Filtros
tiendas = st.multiselect("Filtrar por tienda:", options=df["tienda"].unique(), default=df["tienda"].unique())
buscar = st.text_input("Buscar por nombre del producto:")

df_filtrado = df[df["tienda"].isin(tiendas)]
if buscar:
    df_filtrado = df_filtrado[df_filtrado["nombre_producto"].str.contains(buscar, case=False, na=False)]

# Mostrar resultados
st.write(f"Mostrando {len(df_filtrado)} resultados:")
st.dataframe(df_filtrado[["tienda", "nombre_producto", "precio", "url", "fecha_consulta"]], use_container_width=True)

# Botón para exportar a CSV
st.download_button("📥 Descargar resultados", df_filtrado.to_csv(index=False), "ofertas_buski.csv", "text/csv")
