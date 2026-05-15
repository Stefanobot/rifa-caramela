import streamlit as st
from supabase import create_client

# --- CONFIGURACIÓN DE SUPABASE ---
url = "https://gybjcpbytkailuiqdshy.supabase.co"
key = "sb_publishable_EF7_0Gbks04Lw_mC0j1CzA_HsBMNTwk"

# Inicializar cliente de Supabase
supabase = create_client(url, key)

# --- CONFIGURACIÓN VISUAL DE LA PÁGINA ---
st.set_page_config(page_title="Rifa para Caramela", page_icon="🐾", layout="centered")

# Título de la app
st.title("🐾 Rifa para Caramela")

# --- MENSAJE EMOTIVO DE CARAMELA ---
st.warning("""
### 🐶 ¡Hola! Soy Caramela...
Tengo un problema muy grave en mi **patita trasera derecha** que no me permite apoyarla, por lo que ando caminado cojita y me duele bastante. 
Mis papitos están haciendo esta rifa porque necesito un **tratamiento médico muy costoso** para poderme recuperar y volver a correr feliz. 

¡Ayúdame a sanar mi patita comprando una boleta! Cada granito de arena cuenta muchísimo para mí. ❤️
""")

# --- INFORMACIÓN DEL SORTEO Y PAGO ---
st.info("""
**💰 Valor de la boleta:** $20.000 COP  
**🏆 Premio:** $500.000 COP al número ganador  
**📅 Fecha del sorteo:** Sábado 13 de Junio  
**🎰 Lotería:** Boyacá (últimos 2 números del premio mayor)  
**🔢 Rango:** Del 00 al 99  

---

### 💳 ¿Cómo pagar y reportar?
1. Realiza tu transferencia a **Nequi** o **Daviplata** al número: **350 565 1851**
2. Una vez reserves tu número abajo, **es obligatorio** enviar el comprobante de pago por WhatsApp al mismo número (**350 565 1851**) para asegurar tu cupo.
""")

st.write("### Escoge un número disponible ❤️")

# --- LÓGICA DE DATOS ---
try:
    # Consultar números ya reservados en Supabase
    datos = supabase.table("rifa").select("numero").execute()
    # Guardamos los números ocupados como strings de dos dígitos para comparar fácilmente
    ocupados = [str(fila["numero"]).zfill(2) for fila in datos.data] if datos.data else []
except Exception as e:
    st.error(f"Error al conectar con la base de datos: {e}")
    ocupados = []

# --- INTERFAZ DE GRILLA (Consola de números) ---
# Creamos una cuadrícula de 10 columnas
cols = st.columns(10)

# Generar números del 00 al 99
for i in range(100):
    num_str = str(i).zfill(2)  # Convierte 1 en "01", 9 en "09", etc.
    
    with cols[i % 10]:
        if num_str in ocupados:
            # Botón deshabilitado si ya está vendido
            st.button(num_str, key=f"btn_{num_str}", disabled=True, use_container_width=True)
        else:
            # Botón activo para seleccionar
            if st.button(num_str, key=f"btn_{num_str}", use_container_width=True):
                st.session_state.seleccionado = num_str

# --- FORMULARIO DE RESERVA ---
if "seleccionado" in st.session_state:
    num_elegido = st.session_state.seleccionado
    st.markdown(f"---")
    st.subheader(f"📍 Reservando el número: {num_elegido}")
    
    with st.form("form_reserva", clear_on_submit=True):
        nombre = st.text_input("Nombre completo")
        celular = st.text_input("Número de celular (WhatsApp)")
        
        btn_confirmar = st.form_submit_button("Confirmar Reserva")
        
        if btn_confirmar:
            if nombre and celular:
                try:
                    # Insertar en Supabase
                    supabase.table("rifa").insert({
                        "numero": num_elegido,
                        "nombre": nombre,
                        "celular": celular
                    }).execute()
                    
                    st.balloons()
                    st.success(f"¡Excelente! El número {num_elegido} ha sido apartado. Recuerda enviar el soporte de los $20.000 al WhatsApp 3505651851.")
                    
                    # Limpiar selección y recargar la página para actualizar la grilla
                    del st.session_state.seleccionado
                    st.rerun()
                except Exception as e:
                    st.error(f"Hubo un error al guardar: {e}")
            else:
                st.warning("Por favor, completa tu nombre y celular para reservar.")