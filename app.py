import streamlit as st
from pyproj import Transformer
from supabase import create_client
import pandas as pd

st.set_page_config(page_title="Mon App de Géomètre", page_icon="🌍")

@st.cache_resource
def get_client():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

supabase = get_client()

st.title("🌍 Convertisseur de Coordonnées")
st.write("Bienvenue dans ma première application de géomatique !")

st.sidebar.header("Paramètres de conversion")
source_crs = st.sidebar.text_input("Système source (ex: EPSG:4326)", "EPSG:4326")
target_crs = st.sidebar.text_input("Système cible (ex: EPSG:32630)", "EPSG:32630")

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

        supabase.table("conversions").insert({
            "source_crs": source_crs,
            "target_crs": target_crs,
            "lat_entree": lat,
            "lon_entree": lon,
            "x_sortie": x_out,
            "y_sortie": y_out
        }).execute()
        st.caption("💾 Conversion sauvegardée !")

    except Exception as e:
        st.error(f"Erreur : {e}")

st.info("Astuce : Utilisez l'EPSG 32630 pour la zone UTM 30N (Côte d'Ivoire).")

st.divider()
st.subheader("📋 Historique des conversions")
data = supabase.table("conversions").select("*").order("id", desc=True).limit(20).execute()
if data.data:
    st.dataframe(pd.DataFrame(data.data))
else:
    st.info("Aucune conversion enregistrée pour l'instant.")
