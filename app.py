import streamlit as st
from pyproj import Transformer

# Configuration de la page
st.set_page_config(page_title="Mon App de Géomètre", page_icon="🌍")

st.title("🌍 Convertisseur de Coordonnées")
st.write("Bienvenue dans ma première application de géomatique !")

# Sidebar pour les paramètres
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
        # Calcul de conversion
        transformer = Transformer.from_crs(source_crs, target_crs)
        x_out, y_out = transformer.transform(lat, lon)
        
        # Affichage des résultats
        st.success("Conversion réussie !")
        st.metric("Résultat X", f"{x_out:.3f}")
        st.metric("Résultat Y", f"{y_out:.3f}")
    except Exception as e:
        st.error(f"Erreur de conversion : {e}")

st.info("Astuce : Utilisez l'EPSG 32630 pour la zone UTM 30N (Côte d'Ivoire).")