
import streamlit as st
import sqlite3
import pandas as pd



# Inyectar favicon manualmente
st.markdown(
    """
    <head>
        <link rel="icon" href="favicon_buski.png" type="image/png">
    </head>
    """,
    unsafe_allow_html=True
)

# Logo y título
st.image("buski_logo.png", width=220)
st.title("🔎 Buski")
st.markdown("*Tu comparador de precios inteligente.*")

# Conexión a base de datos
conn = sqlite3.connect("offers.db")
query = "SELECT tienda, nombre_producto, precio, url, fecha_consulta FROM offers ORDER BY fecha_consulta DESC"
df = pd.read_sql_query(query, conn)

# Filtros
tiendas = st.multiselect("Filtrar por tienda:", options=df["tienda"].unique(), default=df["tienda"].unique())
buscar = st.text_input("Buscar por nombre del producto:")

df_filtrado = df[df["tienda"].isin(tiendas)]
if buscar:
    df_filtrado = df_filtrado[df_filtrado["nombre_producto"].str.contains(buscar, case=False, na=False)]

# Mostrar tabla
st.write(f"Mostrando {len(df_filtrado)} resultados:")
st.dataframe(df_filtrado[["tienda", "nombre_producto", "precio", "url", "fecha_consulta"]], use_container_width=True)

# Botón para exportar
st.download_button("📥 Descargar resultados", df_filtrado.to_csv(index=False), "ofertas_buski.csv", "text/csv")
