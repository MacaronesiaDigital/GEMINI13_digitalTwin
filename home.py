import streamlit as st
from PIL import Image
#with open ("style.css") as f:
#    st.markdown(f"<styles>{f.read()}</styles>", unsafe_allow_html=True)
import plotly.express as px
import pandas as pd
import os 
import warnings
from datetime import timedelta
warnings.filterwarnings('ignore')
import datetime
import psycopg2

from dash_datos import page_summary  # Importa la función que creaste en dash_datos.py




gemini_icon = 'https://dsm01pap006files.storage.live.com/y4m3V8LKKeJnD1a0AxWuavohyGInpEWlBwM9566v8gNlx-RN4_yOWlh_68BxT4vkCUstW03fmOoq9jBq-wML_0Awh_91SukCAvnfCesAtnzOp8mp5SALfWGPXqFxfb2_Fmf90tsXoNw4ZbI6XECVcmi2Q5QIfKMd9PczrYgx3qPjuc19_FF4dEbzWfpX9v4EAUbL0YKD1U-1nU0CXQA0RxHWg?encodeFailures=1&width=500&height=500'
st.set_page_config(page_title='GEMINIODS13', page_icon=gemini_icon, layout='wide')
header_image = 'https://dsm01pap006files.storage.live.com/y4m0rkiAn-_tlR9B8UAnUY2G7_Y1n1gURUBI5UhLdSEDeDUiZFuu_ra_6LYnimihnuBGDLWqxLfs6Qo6VwA0MBiBYrGh_3cbH86N3FdP0c0Qi8Nf_GqwVlfdGRp7nTvndb09bOXmdjJn_mrTsNY40NvK0-7bGwfJAdOjMUzwNeuJeH_sNOfI0kiqS5FmPSabSIeYvRVKZKuuPFPcROwo-7TJg?encodeFailures=1&width=1920&height=633'
st.markdown(f'<img src="{header_image}">', unsafe_allow_html=True)
st.title('Macaronesia Digital')

# Agrega un botón para abrir la página de datos
if st.button("Abrir Página de Datos"):
    page_summary()  # Llama a la función para abrir la página