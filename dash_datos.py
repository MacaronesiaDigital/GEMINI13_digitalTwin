# -------------------------------------------------------------
#           APLICACIÓN WEB PARA VISUALIZACIÓN DE DATOS
# -------------------------------------------------------------

# PASO 1.- IMPORTAMOS LIBRERÍAS
# ------------------------------

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
# Conéctate a la base de datos PostgreSQL
conn = psycopg2.connect(
    database="postgres",
    user="gemini13",
    password="MDPonny!",
    host="geminiods13.macaronesiadigital.com",  # Cambia esto si tu base de datos está en un servidor remoto
    port="5432"  # Cambia esto si el puerto de tu base de datos es diferente
)
print(conn)

# PASO 2.- CONFIGURAMOS EL INICIO DE LA WEB
# ------------------------------------------
gemini_icon = 'https://dsm01pap006files.storage.live.com/y4m3V8LKKeJnD1a0AxWuavohyGInpEWlBwM9566v8gNlx-RN4_yOWlh_68BxT4vkCUstW03fmOoq9jBq-wML_0Awh_91SukCAvnfCesAtnzOp8mp5SALfWGPXqFxfb2_Fmf90tsXoNw4ZbI6XECVcmi2Q5QIfKMd9PczrYgx3qPjuc19_FF4dEbzWfpX9v4EAUbL0YKD1U-1nU0CXQA0RxHWg?encodeFailures=1&width=500&height=500'
# Título de la pestaña de la app web
st.set_page_config(page_title='GEMINIODS13', page_icon=gemini_icon, layout='wide')


header_image = 'https://dsm01pap006files.storage.live.com/y4m0rkiAn-_tlR9B8UAnUY2G7_Y1n1gURUBI5UhLdSEDeDUiZFuu_ra_6LYnimihnuBGDLWqxLfs6Qo6VwA0MBiBYrGh_3cbH86N3FdP0c0Qi8Nf_GqwVlfdGRp7nTvndb09bOXmdjJn_mrTsNY40NvK0-7bGwfJAdOjMUzwNeuJeH_sNOfI0kiqS5FmPSabSIeYvRVKZKuuPFPcROwo-7TJg?encodeFailures=1&width=1920&height=633'
st.markdown(f'<img src="{header_image}">', unsafe_allow_html=True)

# Título general común a todas las páginas
st.title('GEMINI ODS 13: Gemelo Digital')


# Esto hace que el margen superior sea más pequeño, pues por efecto está muy separado
st.markdown('<style>div.block-container{padding-top:2rem;}</style',
            unsafe_allow_html= True)
# PASO 3.- ACCEDEMOS A LOS DATOS Y LOS ADAPTAMOS
# -----------------------------------------------

# PASO 3.1- CARGAMOS LOS DATOS


# Elegimos como directorio de trabajo aquel donde se encuentren los datos
#ruta = r'C:\Users\eci\GEMINI13_digitalTwin\assets\csv'
ruta = r'C:\Users\eci\GEMINI13_digitalTwin\assets\csv'
os.chdir(ruta)
cursor = conn.cursor()
create_views_sql = """
CREATE TEMPORARY VIEW base AS
SELECT sensor.id AS sensor_id, sensor.name AS type_name, sensor.type, station.name AS station_name, sensor.provider
    FROM farm, station, sensor, public.owner
    where farm.id = station.farm
    and sensor.station = station.id
    and public.owner.id = farm.owner
    and (public.owner.name = 'Domingo' or public.owner.name = 'Blas')
    and (sensor.provider = 'Ecomatik' or sensor.provider = 'Metos');

CREATE TEMPORARY VIEW ion_content AS
SELECT *
	FROM base, reg_sensor_15 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_16 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_17 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_18 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_19 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_20 as tipo
	WHERE tipo.sensor = base.sensor_id
ORDER BY sensor_id, registered_date;

CREATE TEMPORARY VIEW diameter AS 
SELECT sensor_id, type_name, station_name, provider, registered_date, average, unit
    FROM base, reg_sensor_21 as tipo
    WHERE tipo.sensor = base.sensor_id
UNION
SELECT sensor_id, type_name, station_name, provider, registered_date, tipo.value as average, unit
    FROM base, reg_sensor_22 as tipo
    WHERE tipo.sensor = base.sensor_id
ORDER BY sensor_id, registered_date;

CREATE TEMPORARY VIEW voltage AS
SELECT *
	FROM base, reg_sensor_1 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_2 as tipo
	WHERE tipo.sensor = base.sensor_id
ORDER BY sensor_id, registered_date;

CREATE TEMPORARY VIEW humidity AS
SELECT *
	FROM base, reg_sensor_9 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_10 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_11 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_12 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_13 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_14 as tipo
	WHERE tipo.sensor = base.sensor_id
ORDER BY sensor_id, registered_date;

CREATE TEMPORARY VIEW temperature AS
SELECT *
	FROM base, reg_sensor_3 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_4 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_5 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_6 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_7 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_8 as tipo
	WHERE tipo.sensor = base.sensor_id
ORDER BY sensor_id, registered_date;
"""

# Ejecuta la consulta SQL para crear todas las vistas temporales
cursor.execute(create_views_sql)


# Cierra la conexión a la base de datos
#conn.close()

# Datos de diámetro del tall
consulta_sql = "SELECT * FROM diameter" #FROM base, reg_sensor_21 as tipo WHERE tipo.sensor = base.sensor_id ORDER BY sensor_id, registered_date;"
#df = pd.read_csv("diametro.csv")
df = pd.read_sql_query(consulta_sql, conn)

# Ejecuta la consulta SQL y carga los datos en un DataFrame de pandas

# Datos de contenido ióndico volumétrico
consulta_sql_ion = "SELECT *  	FROM base, reg_sensor_15 as tipo 	WHERE tipo.sensor = base.sensor_id UNION SELECT * 	FROM base, reg_sensor_16 as tipo 	WHERE tipo.sensor = base.sensor_id UNION SELECT * 	FROM base, reg_sensor_17 as tipo 	WHERE tipo.sensor = base.sensor_id UNION SELECT * 	FROM base, reg_sensor_18 as tipo 	WHERE tipo.sensor = base.sensor_id UNION SELECT * 	FROM base, reg_sensor_19 as tipo 	WHERE tipo.sensor = base.sensor_id UNION SELECT * 	FROM base, reg_sensor_20 as tipo 	WHERE tipo.sensor = base.sensor_id ORDER BY sensor_id, registered_date;"
#ion_content_df = pd.read_csv("ion_content.csv")
ion_content_df = pd.read_sql_query(consulta_sql_ion, conn)
ion_content_df['type_name'] = ion_content_df['type_name'].replace('Volumetric Ionic Content', 'VIC', regex=True)

# Datos de voltaje
consulta_sql_vol = "SELECT * 	FROM base, reg_sensor_1 as tipo 	WHERE tipo.sensor = base.sensor_id UNION SELECT * 	FROM base, reg_sensor_2 as tipo 	WHERE tipo.sensor = base.sensor_id ORDER BY sensor_id, registered_date;"
voltage_df = pd.read_csv("voltage.csv")
voltage_df = pd.read_sql_query(consulta_sql_vol, conn)
voltage_df['average'] = voltage_df['value']

# Datos de humedad en suelo
consulta_sql_hum ="SELECT * 	FROM base, reg_sensor_9 as tipo 	WHERE tipo.sensor = base.sensor_id UNION SELECT * 	FROM base, reg_sensor_10 as tipo 	WHERE tipo.sensor = base.sensor_id UNION SELECT * 	FROM base, reg_sensor_11 as tipo 	WHERE tipo.sensor = base.sensor_id UNION SELECT * 	FROM base, reg_sensor_12 as tipo 	WHERE tipo.sensor = base.sensor_id UNION SELECT * 	FROM base, reg_sensor_13 as tipo 	WHERE tipo.sensor = base.sensor_id UNION SELECT * 	FROM base, reg_sensor_14 as tipo 	WHERE tipo.sensor = base.sensor_id ORDER BY sensor_id, registered_date;"
humidity_df = pd.read_csv("humidity.csv")
humidity_df = pd.read_sql_query(consulta_sql_hum, conn)
humidity_df['type_name'] = humidity_df['type_name'].replace('Soil moisture ', '', regex=True)


# Datos de temperatura del suelo
consulta_sql_temp ="SELECT * FROM base, reg_sensor_3 as tipo WHERE tipo.sensor = base.sensor_id UNION SELECT * FROM base, reg_sensor_4 as tipo WHERE tipo.sensor = base.sensor_id UNION SELECT * FROM base, reg_sensor_5 as tipo WHERE tipo.sensor = base.sensor_id UNION SELECT * FROM base, reg_sensor_6 as tipo WHERE tipo.sensor = base.sensor_id UNION SELECT * FROM base, reg_sensor_7 as tipo WHERE tipo.sensor = base.sensor_id UNION SELECT * FROM base, reg_sensor_8 as tipo WHERE tipo.sensor = base.sensor_id ORDER BY sensor_id, registered_date;"
temp_df = pd.read_csv("temperature.csv")
temp_df = pd.read_sql_query(consulta_sql_temp, conn)
temp_df['type_name'] = temp_df['type_name'].replace('Soil temperature', 'Sensor', regex=True)


# PASO 3.2.- ESPECIFICACIÓN DE LAS COLUMNAS TEMPORALES

# Pasamos la columna temporal de los datos a variables de fecha
def to_date(dataframe):
    dataframe['registered_date'] = pd.to_datetime(dataframe['registered_date'])

to_date(df)
to_date(ion_content_df)
to_date(voltage_df)
to_date(humidity_df)
to_date(temp_df)

# PASO 4.- CONFIGURACIÓN DE FILTROS 
# ----------------------------------

# PASO 4.1- FILTROS EN LA BARRA LATERAL

# Definimos la función que nos permitirá realizar los filtros necesarios
def apply_filters(data_frame, column_name, filter_values):
    if not filter_values:
        return data_frame
    return data_frame[data_frame[column_name]==filter_values]

# Añadimos la selección de filtros en la barra lateral
st.sidebar.title("Elige un filtro")

# Filtramos los datos según el proveedor a través de una caja de selección
provider = st.sidebar.selectbox("Elige un proveedor", df["provider"].unique())
df_filtered = apply_filters(df, "provider", provider)
ion_content_filtered = apply_filters(ion_content_df, "provider", provider)
voltage_filtered = apply_filters(voltage_df, "provider", provider)
humidity_filtered = apply_filters(humidity_df, "provider", provider)
temp_filtered = apply_filters(temp_df, "provider", provider)

# Filtramos los datos según la estación a través de una caja de selección
station = st.sidebar.selectbox("Elige una estación", df_filtered["station_name"].unique())
df_filtered = apply_filters(df_filtered, "station_name", station)
ion_content_filtered = apply_filters(ion_content_filtered, "station_name", station)
voltage_filtered = apply_filters(voltage_filtered, "station_name", station)
humidity_filtered = apply_filters(humidity_filtered, "station_name", station)
temp_filtered = apply_filters(temp_filtered, "station_name", station)


# Después de aplicar todos los filtros salvo el de fecha guardamos el resultado en una variable
# Este dataframe nos servirá más adelante para calcular el estado actual de una medida
df_media = df_filtered.copy()
ion_content_mean = ion_content_filtered.copy()
voltage_mean = voltage_filtered.copy()
humidity_mean = humidity_filtered.copy()
temp_mean = temp_filtered.copy()

# PASO 4.2- OTROS FILTROS

# Definimos la función de filtrado por fecha que se utilizará en la página de visualización
def date_filter(dataframe, date1, date2):
        return dataframe[(dataframe['registered_date']>=date1) & (dataframe['registered_date']<(date2+timedelta(days=1)))].copy()

# Definimos los rangos de cada medida para los indicadores de semáforos
diameter_range = [8300, 8700]
voltage_range = [3400, 3500]
ion_content_range = [0, 1700]
humidity_range = [0, 15]

# PASO 5.- DEFINICIÓN DE OBJETOS VISUALES PARA REPRESENTACIÓN DE INDICADORES y GRÁFICAS 
# ---------------------------------------------------------------------------------------

# Indicador en forma de círculo con un color diferente según el estado de una variable en base a unos umbrales determinados
def semaforo(valor, rango=None):

    # Si no se especifica ningún rango el color será gris y no tendrá ningún estado específico
    if rango is None:
        color = "#9E9E9E"
        estado = '-'
    
    # Si se establece un rango, los estados se determinan en función del valor dentro de los intevalos
    else:  
        color = "#C73E01"  # rojo
        estado = "Malo"
        if valor > rango[1]:
            color = "#3F7E44"  # verde
            estado = "Bueno"
        elif valor > rango[0]:
            color = "#F59500" # amarillo
            estado = "Medio"
    
    # Guardamos el estilo del círculo en una variable
    style = f'''
        background-color: {color};
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 20px;
        margin: 0 auto;
        margin-top: 10px;
        margin-bottom: 20px;
        color: white;
    '''
    
    # Devolvemos finalmente el indicador con forma de círculo
    return f'<div style="{style}">{estado}</div>'

# Indicador que muestra un valor determinado y su variación respecto a otro valor
def indicador_metrica(valor, delta, unidad=''):
    
    # Color y flecha de la variación en función de su valor
    color = '#3F7E44' if delta > 0 else '#C73E01'
    flecha = '↑' if delta > 0 else '↓'

    # Formateamos los valores a mostrar
    valor_f = "{:.4f}".format(valor)
    delta_f = "{:.4f}".format(abs(delta))

    # Creamos el container que contendrá todos los elementos del indicador
    st.markdown(
    f"""
    <style>
    .css-5rimss p{{
        
    }}
    @font-face {{
        font-family: 'Inter';
        src: url('Inter-VariableFont_slnt,wght.ttf') format('opentype');
        /* Reemplaza 'ruta/a/tu/fuente' con la ruta real de la fuente en tu proyecto */
        font-weight: normal;
        font-style: normal;
    }}
    #bui155val-0 {{
        color: red; /* Cambia el color a tu preferencia */
    }}
    .css-1629p8f h1{{
        color:white;

    }}
    .css-vk3wp9 h1, p{{
        color:black;
    }}
    .st-et {{
        border-bottom-color: white;
    }}

    .st-es {{
        border-top-color: white;
    }}

    .st-er {{
        border-right-color: white;
    }}


    .st-eq {{
        border-left-color: white;
    }}
    .css-6qob1r{{
        background-color: #3F7E44;
    }}
    p, .label{{
        
        font-family: 'Inter', sans-serif;
    }}

    .st-hy::after  {{
        background-color: #3F7E44;
    }}
    .st-h4::after  {{
        background-color: #3F7E44;
    }}
    .st-hs::after  {{
        border-color: #3F7E44;
    }}
    .st-gy::after {{
        border-color: #3F7E44;
    }}
    .st-gx::after {{
        border-color: #3F7E44;
    }}
    .st-gw::after {{
        border-color: #3F7E44;
    }}
    .st-gv::after {{
        border-color: #3F7E44;
    }}
    

    .css-5rimss img{{
        width:30%;
        margin-left: -1.3rem;
    }}
    @media (max-width: 600px) {{
        .css-5rimss img {{
            width: 100%;
            margin-left: -0.5rem;
        }}
    }}
    stMarkdownContainer{{
        
    }}
    .st-ev {{
        background-color: rgb(240, 242, 246);
        
    }}

    .st-ev p{{
        color:rgb(60, 26, 11);
    }}

    .css-2n7b7j {{
        display: flex;
        -webkit-box-align: center;
        align-items: center;
        padding-top: 0px;
        padding-bottom: 0px;
        background: #3F7E44;
    }}
    img.icon {{
        max-width: 60px;
        width: 100%; 
        height: auto; 
        margin-right:20px;
    }}
    .css-de76by ul, li{{
        border-radius: 0px;
        color:#3F7E44;

    }}
    css-1bdkhir{{
        background-color:#3F7E44;
    }}
    .css-164nlkn{{
        display:none
    }}
    .st-dw {{
        background-color: rgb(225 241 229);
    }}

    .st-dv {{
        background-color: rgb(225 241 229);
    }}
    
    .st-dl {{
        background-color: #3C1A0B;
    }}
    .st-dp{{
        border-bottom-left-radius: 0px;
    }}
    .st-do{{
        border-bottom-right-radius: 0px;
    }}
    .st-dn{{
        border-top-right-radius: 0px;
    }}
    .st-dm{{
        border-top-left-radius: 0px;
    }}
    .st-dn {{
        border-top-left-radius: 0;
    }}
    
    .st-aw{{
        border-bottom-right-radius: 0px;
    }}
    .st-av{{
        border-top-right-radius: 0px;
    }}
    .st-au{{
        border-top-left-radius: 0px;
    }}
    .st-ax{{
        border-bottom-left-radius: 0px;
    }}
    .css-vk3wp9{{
        background-color:#3F7E44;
        color:white;
    }}
    .css-vk3wp9 h1,p{{
        
        color:white;
    }}
    .css-1pp4qrt{{
        color:#3C1A0B;
    }}
    .css-10trblm{{
        color: #3F7E44;
        font-family: 'Barlow', sans-serif;
        font-weight: 600; /* Semibold o Bold según tus necesidades */
    }}

    .metric-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        margin: auto;
    }}
    .value{{
        font-size: 30px;
        margin-top: 5px;
        text-align: center;
    }}
    .delta {{
        margin-bottom: 4px;
    }}
    .label {{
    /* Alinear el label a la derecha  align-self: flex-start;*/
    }}
    .span{{
        color:red;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
    
    # Devolvemos el indidcador de métricas con el estilo deseado
    return f"""
        <div class="metric-container">
            <div class="label">Estado&nbsp;actual</div>
            <div class="value">{valor_f} {unidad}</div>
            <div class="delta" style="color: {color}"> {flecha}&nbsp;{delta_f}&nbsp;{unidad}</div>
        </div>
        """

# Muestra los dos indicadores anteriores en el dashboard
def indicadores(df_media, rango_semaforo=None):

    # Agrupamos los datos por día
    df_media_diaria = df_media.groupby(pd.Grouper(key='registered_date', freq='D'))['average'].mean().reset_index()
    #st.write(df_media_diaria['registered_date'] == pd.date_range(start=startDate, end=endDate, freq='D'))

    # Localizamos la media del día de datos más reciente
    valor = round(df_media_diaria.iloc[-1, -1], 4)

    # Calculamos la variación con respecto al día anterior
    delta = round(valor - df_media_diaria.iloc[-2, -1], 4)

    # Mostramos los indicadores de métroca y de semáforo correspondendiente a los datos
    metrica = indicador_metrica(valor, delta, unidad=df_media['unit'].unique()[0])
    st.markdown(metrica, unsafe_allow_html=True)
    indicador_html = semaforo(valor, rango=rango_semaforo)
    st.markdown(indicador_html, unsafe_allow_html=True)

# Gráfico interactivo de la serie temporal de cada medida      
def grafico_linea(dataframe, frecuencia, marcador, date1, date2, text='Medida'):
    
    # Guardamos la unidad de medida de la variable a representar
    unidad = dataframe['unit'].unique()[0]

    # Agrupamos los datos por la frecuencia indicada para su representación
    linechart = dataframe.groupby(['type_name', pd.Grouper(key='registered_date', freq=frecuencia)])['average'].mean().reset_index()

    # Escogemos todas las combinaciones posibles que deberia haber idealmente de tipos y fechas si se hubiesen registrado todas las fechas
    categorias_unicas = linechart['type_name'].unique()
    fechas_unicas = pd.date_range(start=linechart['registered_date'].min(), end=df['registered_date'].max(), freq=frecuencia)
    combinaciones = pd.MultiIndex.from_product([categorias_unicas, fechas_unicas], names=['type_name', 'registered_date'])
    combinaciones_df = pd.DataFrame(index=combinaciones).reset_index()

    # Hacemos un join de los datos a representar con todas las combinaciones posibles, de forma que se rellenen como
    # valores ausentes todas aquellas fechas que no presenten datos
    df_combinado = pd.merge(combinaciones_df, linechart, how='left', on=['type_name', 'registered_date'])

    # Dibujamos el gráfico de lineas de la medida en cuestión en función de la fecha, distinguiendo por colores
    fig2 = px.line(df_combinado, x='registered_date', y='average',color='type_name', color_discrete_sequence=['#3F7E44', '#C73E01', '#F59500', '#273E8A', '#3C1A0B', '#631675'], 
                   labels={'average': text + f' ({unidad})', 'registered_date': 'Fecha', 'type_name': 'Tipo'},
                   height=525, width=1000, hover_data=['type_name']) #, template='gridon')
    
    # Definir el rango deseado para el eje de las fechas

    if frecuencia == 'D':
        x_range = [date1, date2]
    else:
        x_range = [date1, date2+timedelta(days=1)]
    fig2.update_xaxes(range=x_range, fixedrange=True)
    
    # Configuramos formato del tooltipo
    fig2.update_traces(
        hovertemplate='<b>Tipo</b>: %{customdata[0]}' +
                    '<br><b>Fecha</b>: %{x}' +
                    f'<br><b>{text}</b>: %{{y:.2f}} {unidad}',
        hoverlabel=dict(namelength=0,
                        align='left',
                        font_size=16)    
    )

    # Establecemos marcadores en caso de haber sido seleccionado 
    if marcador == 'Si':
        fig2.update_traces(mode="markers+lines", marker=dict(size=7))
    else:
        fig2.update_traces(mode="lines")
    
    # Configuración de la leyenda de colores
    fig2.update_layout(legend=dict(
        orientation="h",    # Orientación horizontal
        yanchor="top",  # Anclaje en la parte superior
        y=1.10, # 1 es la parte de arriba de la gráfica
        xanchor="center",   # Anclaje en el centro
        x = 0.5, # en el medio de la gráfica
        title=''    # No le asignamos título
    ))

    # Ajustamos el ancho de la gráfica al ancho del contenedor
    st.plotly_chart(fig2, use_container_width=True)

    return linechart

# Cajas de selección para la frecuencia de la visualización y la introducción de marcadores en los datos
def selectbox_freq_marcadores(key):
    # Lista de las distintas opciones a mostrar en la caja de seleccion de frecuencias
    opciones = ['Datos en bruto', 'Cada 30 minutos', 'Cada hora', 'Cada dia']

    # Diccionario que relaciona las opcionas con las frecuencias
    dic_opc = {opciones[0]: '15T', opciones[1]: '30T', opciones[2]: 'H', opciones[3]: 'D'}
    
    # Selección de la frecuencia deseada
    # Por defecto se agrupan los datos cada hora
    opcion = st.selectbox(label='Agrupación de los datos', options=opciones, index=2, key=key+'_opcion')
    freq = dic_opc[opcion]

    # Selección acerca del uso de marcadores en la gráfica de visualización
    # Por defecto se utilizan sí se muestran los marcadores en la gráfica
    marcador = st.selectbox(label='Uso de marcadores', options=['Si', 'No'], index=0, key=key+'_marcador')

    return freq, marcador

# Objeto expandible que permite descargar los datos que se muestran en el gráfico de líneas
#def download_data_expander(data, name):
#    with st.expander("Datos"):
#        # st.write(data.style.background_gradient(cmap='Blues'))
#        csv = data.to_csv(index=False).encode('utf-8')
#        elemento = st.download_button("Descarga", data=csv, file_name=name, mime="text/csv",
#                           help='Click here to download the data as a CSV file')

# Dashboard de una medida que reune todos los elementos visuales anteriores
# Esta función se utilizará particularmente en la página de 'Visualización'
def show_dashboard(df_filtered, df_media, date1, date2, key, rango_semaforo=None):
    
    # Si no hay datos después de aplicar los filtos se lanza una advertencia 
    if len(df_filtered)==0:
        st.warning('No hay datos que mostrar')

    else: 
        # Creamos dos columnas, una más grande que la otra
        columna1, columna2 = st.columns([3.5,1], gap='medium')

        # En esta columna añadimos la caja de seleccion de frecuencia, marcador y los indicadores
        with columna2:
            #st.markdown('<h1 style="text-align:center; font-size: 24px;">Diámetro medio</h1>', unsafe_allow_html=True)
            contenedor = st.container()
            with contenedor:      
                freq, marcador = selectbox_freq_marcadores(key=key)
                indicadores(df_media, rango_semaforo=rango_semaforo)
        
        # En esta columna solo insertamos la gráfica de la medida como serie temporal
        with columna1:
            linechart = grafico_linea(df_filtered, freq, marcador, date1, date2, text=key)

        # Añadimos el expandible con botón de descarga de los datos de la gráfica
        #with columna2:
            #download_data_expander(linechart, 'data.csv')

# Resumen segun los dos indicadores anteriores de una medida
# Esta función se utilizará particularmente en la página de 'Resumen'
def show_summary(df_mean, nombre='Medida', rango_semaforo=None):
    
    # Mostramos como título el nombre de la medida
    st.markdown(f'<h3 style="text-align: center;"> {nombre} </h3>', unsafe_allow_html=True)
    
    # Si hay datos mostramos los indicadores, si no, se lanza una advertencia
    if len(df_mean) == 0:
        st.warning('No hay datos que mostrar')
    else:
        indicadores(df_mean, rango_semaforo=rango_semaforo)
        
    st.markdown('---')

# PASO 6.- DEFINIMOS LOS CONTENIDOS DE DENTRO DE CADA UNA DE LAS PÁGINAS
# ----------------------------------------------------------------------

# Definimos la página de 'Visualización'
# Guardamos las fechas en la que están comprendidos los datos
startDate = df['registered_date'].min()
endDate = df['registered_date'].max() 
#endDate = datetime.date(2023, 10, 9)
# Por defecto, pretendemos mostrar los gráficos desde un rango temporal de 4 días antes a la fecha actual
startDate_def = endDate -timedelta(days=4)

def page_analysis():
    st.markdown(f'<h2> Visualización de datos</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#3C1A0B; font-family: "Barlow", sans-serif; font-weight: 600;"> Esta es la página donde se muestran las gráficas interactivas de los datos en determinados rangos temporales.</p>', unsafe_allow_html=True)
    #st.write('Esta es la página donde se muestran las gráficas interactivas de los datos en determinados rangos temporales.')
    st.markdown('---')

    st.markdown(f'<h4>Selección de fechas</h4>', unsafe_allow_html=True)
    # Creamos dos columnas del mismo tamaño, donde cada uno será una entrada de fecha
    col1, col2 = st.columns((2))

    # Añadimos las entradas de fecha de incio y fin respectivamente dentro de las columnas correspondientes
    with col1:
        date1 = pd.to_datetime(st.date_input("Fecha de inicio", 
                                            value=startDate_def, min_value=startDate, max_value=endDate))
    with col2:
        date2 = pd.to_datetime(st.date_input("Fecha de fin", 
                                            value=endDate, min_value=date1, max_value=endDate))

    # Finalmente, filtramos según las fechas del calendario
    df_f = date_filter(df_filtered, date1, date2)
    ion_content_f= date_filter(ion_content_filtered, date1, date2)
    voltage_f = date_filter(voltage_filtered, date1, date2)
    humidity_f = date_filter(humidity_filtered, date1, date2)
    temp_f = date_filter(temp_filtered, date1, date2)

    diameter_icon = 'https://dsm01pap006files.storage.live.com/y4m0WZgNK5hOL5p6Pxv65wY5mehxL3_wzXhhgW6S5bi625udGC9wtgqcfsbB9hCdIsbFp4k5IyqWPpF-jdzO8t4Ieb6_uVF0G7IAsBrs5-mNQNwug04O1KPJTXZolpjor1tGNi8LG-0T42j4AG6Ros0uow3WKNkL2HsNutjZLKhML3Fued-nCVuxG9XoBEYstVSpFN2zeQvL1RHzkfyG4KpOw?encodeFailures=1&width=802&height=801'
    #st.markdown('---')
    #st.markdown('## :herb: Diámetro del tallo')
    # Resto de tu código
    st.markdown('---')
    st.markdown(f'## <img class="icon" src="{diameter_icon}"> Diámetro del tallo', unsafe_allow_html=True)
    show_dashboard(df_f, df_media, key='Diámetro', rango_semaforo=diameter_range, 
                   date1=date1, date2=date2)
    st.markdown('---')
 
    #st.markdown('## :battery: Voltaje de la batería y del panel solar')
    voltage_icon = 'https://dsm01pap006files.storage.live.com/y4m2uhXoUxFybxswWw41UdfrzJ5KKU0gnxG7b0R5ptetKut2AvnQQjtOmeu9NygdVYn5vjtFiSoVELVlVTG149hiaTOCC8GRjTC08CpozW5di8UQTp8ausqWIhxP7J6rJziI8_EiB_b0jBVH0cPHdkSRP9uDq9NdZ3cXe_Et_QacXrnW8QFKgT1ieBgdy97aJVIvZzgmwZPwhO9RPRZaHCiuA?encodeFailures=1&width=488&height=810'  # Reemplaza con la ruta de tu ícono
    st.markdown(f'## <img class="icon" style="width:40px;" src="{voltage_icon}"> Voltaje de la batería y del panel solar', unsafe_allow_html=True)
    show_dashboard(voltage_f, voltage_mean, key='Voltaje', rango_semaforo=voltage_range,
                   date1=date1, date2=date2)
    st.markdown('---')

    #st.markdown('## :zap: Contenido iónico volumétrico en suelo')
    vic_icon = 'https://dsm01pap006files.storage.live.com/y4mQiChhqFco_7phcEikijv_H6BqdTnVPMRgxJ02UZ8x9Or6j9pPIcpmVqOvTEUBX-GaDt8RsDr_EtrqsnXgeOnOWmpM80QVPZr1gr_W9D5FW7ddkTJLghU0i9DmF1QjHtK8AtkmibvUwaZ6SJhtyLE16vV3y_vtyBog4hC8ZOKhwS2DoIUER5hm3Sn3DYF6G2pUL1bB9M8725IAXZe6-tNHg?encodeFailures=1&width=602&height=603'
    st.markdown(f'## <img class="icon" src="{vic_icon}"> Contenido iónico volumétrico en suelo', unsafe_allow_html=True)
    show_dashboard(ion_content_f, ion_content_mean, key='VIC', rango_semaforo=ion_content_range,
                   date1=date1, date2=date2)
    st.markdown('---')

    humidity_icon = 'https://dsm01pap006files.storage.live.com/y4mnLNsaqguhsfFukAYV-2SPQLnyB28aCf6VpPM_Z038pg1v7SM3Q7mhpFbN4bE0PCflCrO75TPkuxFdgCfMysdttKww0rX-WjHZEI_iZsx9-hwEKWn6zExWhD6Up54nT2XsLYkeZQ1cEJMy7z4E-EtjGn1VwoC3Lijv9ysv7Jz3K7m6OmQey3YOUKBOui0WgPN3KGN4ARijUlLYWw4RDQuvQ?encodeFailures=1&width=598&height=800'
    #st.markdown('## :droplet: Concentración de humedad en suelo')
    st.markdown(f'## <img class="icon" style="width:40px;" src="{humidity_icon}"> Humedad en suelo', unsafe_allow_html=True)
    show_dashboard(humidity_f, humidity_mean, key='Humedad', rango_semaforo=humidity_range, 
                   date1=date1, date2=date2)
    st.markdown('---')

    temp_icon = 'https://dsm01pap006files.storage.live.com/y4mrEz_57VGq_1bMMB0w9q78-uORaywcwBi4AOQuoZkoU7ee1Gqk5HLrRY0h_TrVJ3guBHB3ZswhQJufQp-KB4peBwjF7vo3ZPqnT9sh2wtL-Ii1FftzPJ3RbiDBoF7N_mRKJkvfhdC3ZbHYV4Hw0Tw0oo278NMAtB7JGVVErqr8VmBbmAPN0NJ6gzD9doAnpRol5Inr_0Hjau5G0N2rs5qRw?encodeFailures=1&width=439&height=810'
    #st.markdown('## :thermometer: Temperatura del suelo')
    st.markdown(f'## <img class="icon" style="width:30px;" src="{temp_icon}"> Temperatura en suelo', unsafe_allow_html=True)
    show_dashboard(temp_f, temp_mean, key='Temperatura', rango_semaforo=None,
                   date1=date1, date2=date2)
    st.markdown('---')

# Definimos la página de 'Resumen'
def page_summary():
    st.markdown(f'<h2> Resumen de estado de las medidas</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#3C1A0B; font-family: "Barlow", sans-serif; font-weight: 600;"> Esta es la página donde se muestra la media de las medidas obtenidas el último día de datos y el estado según los umbrales preestablecidos.</p>', unsafe_allow_html=True)
    #st.write("Esta es la página donde se muestra la media de las medidas obtenidas el último día de datos y el estado según los umbrales preestablecidos.")
    st.markdown('---')
    columnas = st.columns(3, gap="large")
    with columnas[0]:
        show_summary(df_media, nombre='Diametro', rango_semaforo=diameter_range)
    with columnas[1]:
        show_summary(voltage_mean, nombre='Voltaje', rango_semaforo=voltage_range)
    with columnas[2]:
        show_summary(ion_content_mean, nombre='VIC', rango_semaforo=ion_content_range)
    columnas = st.columns(3, gap="medium")
    with columnas[0]:
        show_summary(humidity_mean, nombre='Humedad', rango_semaforo=humidity_range)
    with columnas[1]:
        show_summary(temp_mean, nombre='Temperatura', rango_semaforo=None)
    #with columnas[2]:
    #    show_summary(temp_mean, nombre='Temperatura', rango_semaforo=None)



# Configuramos la navegacción por páginas el sidebar
# Cabe notar que por defecto la primera en mostrarse es la primera definida en el diccionario
st.sidebar.title("Navegación")
pages = {
    "Resumen": page_summary,
    "Visualización": page_analysis 
}

# Seleccionamos una página en una lista de selección en el sidebar
selected_page = st.sidebar.radio("Selecciona una página", tuple(pages.keys()))



# Mostramos el contenido de la página seleccionada
pages[selected_page]()

conn.close()