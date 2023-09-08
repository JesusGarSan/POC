import streamlit as st
import numpy as np
from streamlit_image_coordinates import streamlit_image_coordinates
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

st.set_page_config(layout='wide')


# Escogemos la fuente emisora
def elegir_fuente():
    fuentes = ['Dragado', 'Voladura', 'Buque partiendo']
    fuente = st.selectbox('Escoge qué fuente quieres colocar', fuentes)
    if fuente =='Dragado': color = 'red'; numero = 1
    if fuente =='Voladura': color = 'purple'; numero = 2
    if fuente =='Buque partiendo': color = 'green'; numero = 3

    return fuente, color, numero


def coords_manual(coords_geo):
    column = st.columns(2)
    long = column[0].number_input('Longitud (º)', value = coords_geo[0], disabled=True, format="%.8f" )
    lat  = column[1].number_input('Latitud (º)', value = coords_geo[1],  disabled=True, format="%.8f")
    coords = (long, lat)
    return coords


def get_ellipse_coords(point: tuple[int, int], radius = 5) -> tuple[int, int, int, int]:
    center = point
    return (
        center[0] - radius,
        center[1] - radius,
        center[0] + radius,
        center[1] + radius,
    )


def mapa_clickable(coords, color_fuente):
    st.write('Pincha donde quieras colocar la fuente:')
    from PIL import Image, ImageDraw
    with Image.open("puerto.png") as img:
        draw = ImageDraw.Draw(img)

        # Draw an ellipse at each coordinate in points
        if st.session_state["coords"] != None:

            coords = get_ellipse_coords(st.session_state["coords"])
            draw.ellipse(coords, fill=color_fuente)
        

        value = streamlit_image_coordinates(img, key="pil")

        if value is not None:
            coords = value["x"], value["y"]
        else: coords=None

        if coords != st.session_state["coords"]:
            st.session_state["coords"]  = coords
            st.experimental_rerun()
    return coords




def colorbar():
    # Definir los extremos de la barra de colores
    extremo_inferior = 40
    extremo_superior = 140

    # Crear una figura y un eje con fondo transparente
    fig, ax = plt.subplots(figsize=(8, 1), facecolor='none')  # Establece el fondo como transparente

    # Crear la barra de colores horizontal
    cmap = plt.get_cmap('viridis')  # Puedes elegir cualquier mapa de colores que desees
    norm = plt.Normalize(extremo_inferior, extremo_superior)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # Esto es necesario para que la barra de colores se muestre correctamente

    # Dibujar la barra de colores
    barra_colores = plt.colorbar(sm, ax=ax, orientation='horizontal')

    # Personalizar la barra de colores y el eje
    barra_colores.set_label('SPL (dB)')  # Agregar una etiqueta a la barra de colores
    ax.set_axis_off()  # Ocultar los ejes

    # Guardar la figura en un archivo PNG con fondo transparente y sin espacio en blanco
    plt.savefig('barra_colores.png', transparent=True, bbox_inches='tight', pad_inches=0, dpi=300)

    st.image('barra_colores.png')
    
    return


def random_heatmap_generator(numero_fuente, color_fuente, coords, img='puerto.png'):

    st.subheader('Mapa de ruido')

    opacity = st.slider('Opacidad', min_value=0.0, max_value=1.0, value=0.5)

    xrange = st.session_state.corners_geo[0][1], st.session_state.corners_geo[1][1] 
    yrange = st.session_state.corners_geo[0][0], st.session_state.corners_geo[1][0] 
    fig, ax = plt.subplots(figsize = (8,6))
    imagen_puerto = mpimg.imread('puerto.png')
    ax.imshow(imagen_puerto, extent= [xrange[0], xrange[1], yrange[1], yrange[0]])
    ax.set_xlabel('Longitud (º)')
    ax.set_ylabel('Latitud (º)')

    # Dibujamos la fuente emisora
    geo_coords = px_to_coords(st.session_state.coords)
    plt.scatter(geo_coords[0], geo_coords[1], c = color_fuente, edgecolor='black')


    # Semilla para reproducibilidad
    long, lat = coords
    semilla = int(numero_fuente * 1e6 + long*1e3 + lat)
    np.random.seed(semilla)
    # Dimensiones del mapa de calor
    filas, columnas = 10, 20
    # Generar datos aleatorios
    datos_aleatorios = np.random.rand(filas, columnas) * 140 #140 dB máximo
    datos_aleatorios = np.clip(datos_aleatorios, a_min=40, a_max=140)
    # Dibujar el mapa de calor con transparencia
    imagen = ax.imshow(datos_aleatorios, cmap='plasma', alpha=opacity, extent= [xrange[0], xrange[1], yrange[1], yrange[0]])  # Ajusta el valor de alpha según la transparencia deseada

    barra_de_color = fig.colorbar(imagen)
    barra_de_color.set_label('Nivel de Intensidad del ruido (dB)')


    st.pyplot(fig)


def px_to_coords(coords_px):


    resolution_px = st.session_state.resolution_px
    corner_geo    = st.session_state.corners_geo


    px_x, px_y = coords_px

    x_geo = px_x/resolution_px[0] * (corner_geo[1][1] - corner_geo[0][1]) + corner_geo[0][1]
    y_geo = px_y/resolution_px[1] * (corner_geo[1][0] - corner_geo[0][0]) + corner_geo[0][0]

    coords_geo = [x_geo, y_geo]

    return coords_geo


def coords_to_px(coords_geo):
    resolution_px = st.session_state.resolution_px
    corner_geo    = st.session_state.corners_geo

    geo_x = coords_geo[0]
    geo_y = coords_geo[1]
    
    x_px = (geo_x - corner_geo[0][1]) /(corner_geo[1][1] - corner_geo[0][1]) *resolution_px[0]
    y_px = (geo_y - corner_geo[0][0]) /(corner_geo[1][0] - corner_geo[0][0]) *resolution_px[1]

    coords_px = (round(x_px,0), round(y_px,0))

    return coords_px
#----------------------------------------------------

# ---- DECLARACIÓN DE VARIABLES GLOBALES DE SESIÓN -------

if 'manual_coords' not in st.session_state:
    st.session_state.manual_coords = None

if 'coords' not in st.session_state:
    st.session_state.coords = None

#if 'skip_map' not in st.session_state:
#    st.session_state.skip_map = False




st.session_state.corners_geo = [[43.354826, -8.539946],[43.3325442, -8.497632]]
st.session_state.resolution_px = [789, 604]

# ---------------------------------------------------------

column = st.columns(2)

with column[0]:

    fuente, color_fuente, numero_fuente = elegir_fuente()
    new_coords = mapa_clickable(st.session_state.coords, color_fuente)

    if new_coords!= None:# and st.session_state.skip_map != True:
        st.session_state.coords = new_coords    
    #elif st.session_state.skip_map == True: st.session_state.skip_map = False
    
if st.session_state.coords != None:    
    #colorbar()
    with column[0]:
        st.session_state.manual_coords = coords_manual(px_to_coords(st.session_state.coords))
        #st.write(st.session_state.coords)
        #st.write(st.session_state.manual_coords)
        #st.write(coords_to_px(st.session_state.manual_coords))
        #st.write(coords_to_px(st.session_state.manual_coords) == st.session_state.coords)
        #if coords_to_px(st.session_state.manual_coords) != st.session_state.coords:
        #    st.session_state.coords = coords_to_px(st.session_state.manual_coords)
        #    st.session_state.skip_map = True
        #    st.experimental_rerun()



    with column[1]:
        random_heatmap_generator(numero_fuente, color_fuente, st.session_state.coords)


