import streamlit as st
from pyproj import Transformer
import psycopg2
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Mon App de Géomètre", page_icon="🌍")

# Connexion Supabase
@st.cache_resource
def get_connection():
    return psycopg2.connect(st.secrets["DATABASE_URL"])

conn = get_connection()

st.title("🌍 Convertisseur de Coordonnées")
st.write("Bienvenue dans ma première application de géomatique !")

# Sidebar
st.sidebar.header("Paramètres de conversion")
source_crs = st.sidebar.text_input("Système source (ex: EPSG:4326)", "EPSG:4326")
target_crs = st.sidebar.text_input("Système cible (ex: EPSG:32630)", "EPSG:32630")

# Entrée des données
col1, col2 = st.columns(2)
with col1:
    lat = st.number_input("Latitude (X)", value=5.3)
with col2:
    lon = st.number_input("Longitude (Y)", value=-4.0)

if st.button("Convertir"):
    try:
        transformer = Transformer.from_crs(source_crs, target_crs)
        x_out, y_out = transformer.transform(lat, lon)

        st.success("Conversion réussie !")
        st.metric("Résultat X", f"{x_out:.3f}")
        st.metric("Résultat Y", f"{y_out:.3f}")

        # ✅ Sauvegarde dans Supabase
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO conversions (source_crs, target_crs, lat_entree, lon_entree, x_sortie, y_sortie)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (source_crs, target_crs, lat, lon, x_out, y_out))
            conn.commit()
        st.caption("💾 Conversion sauvegardée !")

    except Exception as e:
        st.error(f"Erreur de conversion : {e}")

st.info("Astuce : Utilisez l'EPSG 32630 pour la zone UTM 30N (Côte d'Ivoire).")

# ✅ Historique des conversions
st.divider()
st.subheader("📋 Historique des conversions")
df = pd.read_sql("SELECT * FROM conversions ORDER BY date_heure DESC LIMIT 20", conn)
st.dataframe(df)
