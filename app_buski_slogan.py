
import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime

# Configurar la página con título, favicon y layout
st.set_page_config(
    page_title="Buski - Comparador de Precios",
    page_icon="favicon_buski.png",
    layout="wide"
)

# Inyectar favicon manual
st.markdown(
    """
    <head>
        <link rel="icon" href="favicon_buski.png" type="image/png">
    </head>
    """,
    unsafe_allow_html=True
)

# Mostrar logo y título
from datetime import datetime
st.markdown(f"🕒 Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

st.image("buski_logo.png", width=220)
st.markdown("*Tu comparador de precios inteligente.*")

st.markdown("Consulta diariamente las mejores ofertas en productos de tecnología disponibles en Mercado Libre, Alkosto y Éxito. Usa los filtros para encontrar lo que buscas rápidamente.")

# Verificar si es necesario actualizar los datos (una vez al día)
db_file = "offers.db"
update_flag_file = "last_update.txt"

def debe_actualizar():
    if not os.path.exists(update_flag_file):
        return True
    with open(update_flag_file, "r") as f:
        last = f.read().strip()
    return last != datetime.now().strftime("%Y-%m-%d")

def guardar_fecha_actualizacion():
    with open(update_flag_file, "w") as f:
        f.write(datetime.now().strftime("%Y-%m-%d"))

def actualizar_datos():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM offers")

    productos = [
        # formato: (tienda, nombre_producto, precio, url, categoria)
        ("Mercado Libre", "TV Samsung 70 pulgadas 4K", 3299900, "https://mercadolibre.com/tv1", "Televisores"),
        ("Mercado Libre", "Celular Xiaomi Redmi Note 12", 899000, "https://mercadolibre.com/cel1", "Celulares"),
        ("Alkosto", "TV LG 70 UHD AI ThinQ", 3499900, "https://alkosto.com/tv1", "Televisores"),
        ("Alkosto", "Portátil Lenovo IdeaPad 3 Ryzen 5", 2199900, "https://alkosto.com/laptop1", "Portátiles"),
        ("Éxito", "TV Kalley 70 Smart TV", 2799900, "https://exito.com/tv1", "Televisores"),
        ("Éxito", "Samsung Galaxy A54 5G", 1699000, "https://exito.com/cel1", "Celulares"),
        ("Mercado Libre", "Laptop HP 14 Ryzen 7", 2649900, "https://mercadolibre.com/laptop1", "Portátiles"),
        ("Alkosto", "Celular Realme 11 Pro", 1449900, "https://alkosto.com/cel2", "Celulares"),
        ("Éxito", "Portátil Asus VivoBook i5", 2399900, "https://exito.com/laptop2", "Portátiles"),
        ("Mercado Libre", "Monitor LG UltraWide 29\"", 899000, "https://mercadolibre.com/monitor1", "Monitores"),
    ]
        ("Mercado Libre", "TV Samsung 70 pulgadas 4K", 3299900, "https://mercadolibre.com/tv1"),
        ("Mercado Libre", "Celular Xiaomi Redmi Note 12", 899000, "https://mercadolibre.com/cel1"),
        ("Alkosto", "TV LG 70 UHD AI ThinQ", 3499900, "https://alkosto.com/tv1"),
        ("Alkosto", "Portátil Lenovo IdeaPad 3 Ryzen 5", 2199900, "https://alkosto.com/laptop1"),
        ("Éxito", "TV Kalley 70 Smart TV", 2799900, "https://exito.com/tv1"),
        ("Éxito", "Samsung Galaxy A54 5G", 1699000, "https://exito.com/cel1"),
        ("Mercado Libre", "Laptop HP 14 Ryzen 7", 2649900, "https://mercadolibre.com/laptop1"),
        ("Alkosto", "Celular Realme 11 Pro", 1449900, "https://alkosto.com/cel2"),
        ("Éxito", "Portátil Asus VivoBook i5", 2399900, "https://exito.com/laptop2"),
        ("Mercado Libre", "Monitor LG UltraWide 29\"", 899000, "https://mercadolibre.com/monitor1"),
    ]

    for tienda, nombre, precio, url, categoria in productos:
        cursor.execute("""
            INSERT INTO offers (tienda, nombre_producto, precio, url, fecha_consulta, categoria)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tienda, nombre, precio, url, datetime.now().isoformat(), categoria))
    
    conn.commit()
    conn.close()
    guardar_fecha_actualizacion()

if debe_actualizar():
    actualizar_datos()

# Leer base de datos
conn = sqlite3.connect(db_file)
query = "SELECT tienda, nombre_producto, precio, url, categoria FROM offers ORDER BY precio ASC"
df = pd.read_sql_query(query, conn)

# Filtros adicionales
categoria = st.multiselect("Filtrar por categoría:", options=df["categoria"].unique(), default=df["categoria"].unique())
tiendas = st.multiselect("Filtrar por tienda:", options=df["tienda"].unique(), default=df["tienda"].unique())
buscar = st.text_input("Buscar por nombre del producto:")

df_filtrado = df[df["tienda"].isin(tiendas) & df["categoria"].isin(categoria)]
if buscar:
    df_filtrado = df_filtrado[df_filtrado["nombre_producto"].str.contains(buscar, case=False, na=False)]

# Mostrar tabla sin columnas innecesarias
st.write(f"🔍 Resultados encontrados: {len(df_filtrado)}")

# Convertir enlaces en formato clicable
df_filtrado["url"] = df_filtrado["url"].apply(lambda x: f'<a href="{x}" target="_blank">Ver producto</a>')
st.write(df_filtrado[["tienda", "nombre_producto", "precio", "url", "categoria"]].to_html(escape=False, index=False), unsafe_allow_html=True)


# Descargar CSV

# Botón para descargar los datos
st.download_button("📥 Descargar resultados", df_filtrado.drop(columns=["url"]).to_csv(index=False), "ofertas_buski.csv", "text/csv")

