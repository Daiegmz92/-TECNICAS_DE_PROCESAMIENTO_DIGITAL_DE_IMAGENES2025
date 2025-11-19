import streamlit as st
from huggingface_hub import InferenceClient
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import io
import os
import requests
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Restaurador AI - TP2", layout="wide", page_icon="✨")

# --- TÍTULO Y DESCRIPCIÓN ---
st.title("✨ Restaurador de Fotos Antiguas con IA")
st.markdown("""
**Trabajo Integrador N°2** | Restauración Inteligente + Análisis Semántico.
*Sube tu foto, aplica filtros y deja que la IA haga su magia.*
""")

# --- BARRA LATERAL (CONFIGURACIÓN Y FILTROS) ---
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Token
    api_token = os.getenv("HF_TOKEN")
    if not api_token:
        st.warning("⚠️ Token no detectado.")
        api_token = st.text_input("Hugging Face Token:", type="password")
    else:
        st.success("✅ Token Conectado")
    
    st.divider()
    
    st.header("🎨 Estilo Final")
    filtro_seleccionado = st.selectbox(
        "Aplicar filtro post-procesamiento:",
        ["Original (Color Restaurado)", "Blanco y Negro Clásico", "Sepia Nostálgico", "Alto Contraste"]
    )

# --- FUNCIONES DE PROCESAMIENTO ---

def aplicar_filtro_creativo(img, estilo):
    """Aplica filtros estéticos usando PIL (Procesamiento Digital Clásico)"""
    if estilo == "Blanco y Negro Clásico":
        return img.convert("L")
    elif estilo == "Sepia Nostálgico":
        # Conversión manual a sepia para control total
        width, height = img.size
        pixels = img.load() 
        for py in range(height):
            for px in range(width):
                r, g, b = img.getpixel((px, py))
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                pixels[px, py] = (min(tr, 255), min(tg, 255), min(tb, 255))
        return img
    elif estilo == "Alto Contraste":
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(1.5)
    return img

def procesar_localmente(image_pil):
    """
    PLAN Z (AJUSTADO): Prioriza limpieza de rayones sobre nitidez.
    """
    # 1. Filtro Mediana MÁS FUERTE para borrar las rayas blancas gruesas
    # (Size 3 es suave, Size 5 es fuerte. Usamos 3 para no perder rasgos, pero repetimos si hace falta)
    img_mod = image_pil.filter(ImageFilter.MedianFilter(size=3))
    
    # 2. Suavizado extra para piel de porcelana
    img_mod = img_mod.filter(ImageFilter.SMOOTH_MORE)
    
    # 3. Nitidez SUAVE (Bajamos de 2.5 a 1.3 para no resaltar ruido)
    enhancer_sharpness = ImageEnhance.Sharpness(img_mod)
    img_mod = enhancer_sharpness.enhance(1.3) 
    
    # 4. Color VIVO (Para quitar el tono sepia muerto)
    enhancer_color = ImageEnhance.Color(img_mod)
    img_mod = enhancer_color.enhance(1.5)
    
    # 5. Contraste y Brillo automático
    img_mod = ImageOps.autocontrast(img_mod, cutoff=1)
    
    return img_mod

def mejorar_imagen(image_bytes, image_pil_original, token):
    """Restauración con IA + Failover"""
    # Modelos específicos de restauración
    modelos = ["mir-fan/SwinIR_4x", "Eugenius/swin2SR-classical-sr-x2-64"]
    headers = {"Authorization": f"Bearer {token}"}
    status_placeholder = st.empty()

    for repo_id in modelos:
        API_URL = f"https://api-inference.huggingface.co/models/{repo_id}"
        # Intentamos 2 veces por modelo
        for i in range(2): 
            try:
                status_placeholder.info(f"⏳ Conectando con IA ({repo_id})... Intento {i+1}")
                # Subí el timeout a 60s para darle más chance a la IA real
                response = requests.post(API_URL, headers=headers, data=image_bytes, timeout=60)
                
                if response.status_code == 200:
                    status_placeholder.empty()
                    return Image.open(io.BytesIO(response.content)), f"Modelo IA ({repo_id})"
                elif "503" in str(response.status_code):
                    time.sleep(2)
                    continue
            except Exception as e:
                print(f"Error conectando a {repo_id}: {e}")
                continue
    
    status_placeholder.empty()
    st.warning("⚠️ Aviso: Los servidores de IA están saturados. Se aplicó una restauración algorítmica local de emergencia.")
    return procesar_localmente(image_pil_original), "Modo Local (Backup)"

def analizar_imagen(image_pil, token):
    repo_id = "Salesforce/blip-image-captioning-large"
    client = InferenceClient(token=token)
    try:
        return client.image_to_text(image_pil, model=repo_id)
    except:
        return "Análisis no disponible."

# --- INTERFAZ PRINCIPAL ---

uploaded_file = st.file_uploader("Sube tu foto:", type=["jpg", "jpeg", "png"])

if uploaded_file and api_token:
    image_original = Image.open(uploaded_file).convert("RGB")
    
    # Layout de Columnas
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📷 Original")
        st.image(image_original, width=450)

    # Contenedor vacío para el resultado
    with col2:
        st.subheader("✨ Resultado")
        resultado_placeholder = st.empty()
        resultado_placeholder.info("Esperando procesamiento...")

    # Preparar bytes
    buf = io.BytesIO()
    image_original.save(buf, format="JPEG")
    img_bytes = buf.getvalue()

    if st.button("🚀 Procesar Imagen", type="primary"):
        with st.spinner("Restaurando detalles..."):
            
            # 1. Restauración (IA o Local)
            img_restaurada, fuente = mejorar_imagen(img_bytes, image_original, api_token)
            
            if img_restaurada:
                # 2. Aplicar Filtro Creativo (Seleccionado en Sidebar)
                img_final = aplicar_filtro_creativo(img_restaurada.copy(), filtro_seleccionado)
                
                # 3. Análisis
                descripcion = analizar_imagen(img_final, api_token)
                
                # ACTUALIZAR INTERFAZ
                resultado_placeholder.image(img_final, width=450, caption=f"Fuente: {fuente} | Filtro: {filtro_seleccionado}")
                
                st.success("✅ ¡Listo!")
                st.divider()
                st.subheader("🔍 La IA dice:")
                st.info(descripcion)
                
                # Descarga
                buf_out = io.BytesIO()
                img_final.save(buf_out, format="PNG")
                st.download_button("⬇️ Descargar Imagen", buf_out.getvalue(), "resultado.png", "image/png")
            else:
                st.error("Error en el procesamiento.")

elif not api_token:
    st.info("👈 Por favor, ingresa tu token en la barra lateral.")