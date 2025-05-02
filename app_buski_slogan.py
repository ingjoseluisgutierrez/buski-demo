
import streamlit as st
import sqlite3
import pandas as pd

# Configuración de página
st.set_page_config(
    page_title="Buski - Comparador de Precios",
    page_icon="favicon_buski.png",
    layout="wide"
)

# Inyectar favicon manualmente
st.markdown(
    """
    <head>
        <link rel="icon" href="favicon_buski.png" type="image/png">
    </head>
    """,
    unsafe_allow_html=True
)

# CSS para centrar tabla
st.markdown(
    """
    <style>
    .center-table {
        display: flex;
        justify-content: center;
    }
    .center-table table {
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Encabezado
st.image("buski_logo.png", width=300)
st.markdown("*Tu comparador de precios inteligente.*")
st.markdown("Consulta diariamente las mejores ofertas en productos de tecnología disponibles en Mercado Libre, Alkosto y Éxito. Usa los filtros para encontrar lo que buscas rápidamente.")

# Leer base de datos
conn = sqlite3.connect("offers.db")
query = "SELECT tienda, nombre_producto, precio, url, categoria FROM offers ORDER BY precio ASC"
df = pd.read_sql_query(query, conn)

# Filtros
tiendas = st.multiselect("Filtrar por tienda:", options=df["tienda"].unique(), default=df["tienda"].unique())
categorias = st.multiselect("Filtrar por categoría:", options=df["categoria"].unique(), default=df["categoria"].unique())
buscar = st.text_input("Buscar por nombre del producto:")

df_filtrado = df[df["tienda"].isin(tiendas) & df["categoria"].isin(categorias)]
if buscar:
    df_filtrado = df_filtrado[df_filtrado["nombre_producto"].str.contains(buscar, case=False, na=False)]

# Enlaces clicables
df_filtrado["url"] = df_filtrado["url"].apply(lambda x: f'<a href="{x}" target="_blank">Ver producto</a>')

# Mostrar resultados centrados
st.write(f"🔍 Resultados encontrados: {len(df_filtrado)}")
st.markdown('<div class="center-table">' + df_filtrado[["tienda", "nombre_producto", "precio", "url", "categoria"]].to_html(escape=False, index=False) + '</div>', unsafe_allow_html=True)

# Exportar CSV
st.download_button("📥 Descargar resultados", df_filtrado.drop(columns=["url"]).to_csv(index=False), "ofertas_buski.csv", "text/csv")
