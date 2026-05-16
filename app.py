import streamlit as st
from supabase import create_client

# --- CONFIGURACIÓN DE SUPABASE ---
url = "https://gybjcpbytkailuiqdshy.supabase.co"
key = "sb_publishable_EF7_0Gbks04Lw_mC0j1CzA_HsBMNTwk"

# Inicializar cliente de Supabase
supabase = create_client(url, key)

# --- CONFIGURACIÓN VISUAL DE LA PÁGINA ---
st.set_page_config(page_title="Rifa para Caramela", page_icon="🐾", layout="centered")

# --- ESTILOS PERSONALIZADOS (CSS) ---
st.markdown("""
    <style>
    /* 1. Estilo para botones OCUPADOS (Deshabilitados) */
    div[data-testid="stButton"] button:disabled {
        background-color: #FFC0CB !important; /* Rosado claro */
        color: #D81B60 !important; /* Texto fucsia oscuro */
        border: 2px solid #FF69B4 !important;
        opacity: 1 !important;
        font-weight: bold !important;
    }

    /* 2. Estilo para botones DISPONIBLES */
    div[data-testid="stButton"] button {
        border-radius: 8px;
        border: 1px solid #dcdcdc;
        transition: 0.3s;
    }

    /* 3. Estilo para el botón seleccionado */
    div[data-testid="stButton"] button:active, div[data-testid="stButton"] button:focus {
        background-color: #007BFF !important;
        color: white !important;
        border: 2px solid #0056b3 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Título de la app
st.title("🐾 Rifa para Caramela")

# --- MENSAJE EMOTIVO ---
st.warning("""
### 🐶 ¡Hola! Soy Caramela...
Tengo un problema muy grave en mi **patita trasera derecha** que no me permite apoyarla, por lo que ando caminado cojita y me duele bastante. 
Mis papitos están haciendo esta rifa porque necesito un **tratamiento médico muy costoso** para poderme recuperar y volver a correr feliz. 

¡Ayúdame a sanar mi patita comprando una boleta! Cada granito de arena cuenta muchísimo para mí. ❤️
""")

# --- INFORMACIÓN DEL SORTEO ---
st.info("""
**💰 Valor de la boleta:** $20.000 COP  
**🏆 Premio:** $500.000 COP al número ganador  
**📅 Fecha del sorteo:** Sábado 13 de Junio  
**🎰 Lotería:** Boyacá (últimos 2 números del premio mayor)  
**🔢 Rango:** Del 00 al 99  

---

### 💳 ¿Cómo pagar?
1. Realiza tu transferencia a **Nequi** o **Daviplata** al número: **350 565 1851**
""")

st.write("### Escoge un número disponible ❤️")

# --- LÓGICA DE DATOS ---
try:
    datos = supabase.table("rifa").select("numero").execute()
    ocupados = [str(fila["numero"]).zfill(2) for fila in datos.data] if datos.data else []
except Exception as e:
    st.error(f"Error al conectar con la base de datos: {e}")
    ocupados = []

# --- INTERFAZ DE GRILLA ---
cols = st.columns(10)

for i in range(100):
    num_str = str(i).zfill(2)
    
    with cols[i % 10]:
        if num_str in ocupados:
            st.button(num_str, key=f"btn_{num_str}", disabled=True, use_container_width=True)
        else:
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
        
        # NUEVO: Check list (Radio) para que el cliente elija su estado
        opcion_pago = st.radio(
            "¿Ya realizaste el pago?",
            ["Pendiente de pago", "Ya realicé el pago"],
            help="Selecciona una opción para reportar tu estado actual."
        )
        
        btn_confirmar = st.form_submit_button("Confirmar Reserva")
        
        if btn_confirmar:
            if nombre and celular:
                try:
                    # Guardamos según lo que el usuario seleccionó
                    estado_para_base = "Pagado" if opcion_pago == "Ya realicé el pago" else "Pendiente"
                    
                    supabase.table("rifa").insert({
                        "numero": num_elegido,
                        "nombre": nombre,
                        "celular": celular,
                        "estado_pago": estado_para_base
                    }).execute()
                    
                    st.balloons()
                    st.success(f"¡Excelente! El número {num_elegido} ha sido apartado.")
                    
                    # Mensaje condicional según lo que marcó
                    if estado_para_base == "Pagado":
                        st.info("✅ Gracias por tu pago. Por favor envía el soporte al WhatsApp 3505651851 para validar.")
                    else:
                        st.warning("⏳ Tu reserva está pendiente. Recuerda pagar y enviar el soporte al WhatsApp 3505651851.")
                    
                    del st.session_state.seleccionado
                    st.rerun()
                except Exception as e:
                    st.error(f"Hubo un error al guardar: {e}")
            else:
                st.warning("Por favor, completa tu nombre y celular para reservar.")

    # Mensaje recordatorio fijo debajo del formulario
    st.caption("⚠️ Si ya realizaste el pago envía soporte al Whatsapp 3505651851")
