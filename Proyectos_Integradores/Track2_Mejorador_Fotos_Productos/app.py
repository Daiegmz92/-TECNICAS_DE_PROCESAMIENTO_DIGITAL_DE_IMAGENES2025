import streamlit as st
from diffusers import AutoPipelineForText2Image, EulerAncestralDiscreteScheduler
from transformers import pipeline as hf_pipeline
import google.generativeai as genai
import torch
from PIL import Image, PngImagePlugin
import os
from dotenv import load_dotenv
import io

# Carga las variables del archivo .env
load_dotenv()

# --- 1. Configuración de Página (Más Profesional) ---
st.set_page_config(
    page_title="Mejorador de Fotos Pro",
    page_icon="✨",
    layout="wide"
)

# --- 2. Carga y Verificación de API Keys ---
HF_TOKEN = os.environ.get("HF_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Verificación de claves (solo desde .env para desarrollo local)
# En producción usar st.secrets para Hugging Face Spaces
pass

if not HF_TOKEN or not GEMINI_API_KEY:
    st.error("🚨 ERROR: Faltan las API Keys (HF_TOKEN o GEMINI_API_KEY).", icon="🚨")
    st.warning(
        "Asegúrate de configurar los 'Secrets' en Hugging Face Spaces "
        "o tu archivo `.env` local.",
        icon="📄"
    )
    st.stop()

# Configura la API de Gemini
try:
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    st.error(f"Error al configurar Gemini: {e}", icon="🚨")
    st.stop()

# --- 3. Carga de Modelos (con Caching) ---

# Requisito 2: Modelo de Difusión (Cambiado a SDXL-Turbo)
@st.cache_resource
def cargar_pipeline_difusion():
    model_id = "stabilityai/sdxl-turbo" # Modelo más rápido y de mayor calidad
    try:
        # Usamos AutoPipelineForText2Image que también maneja img2img
        pipe = AutoPipelineForText2Image.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            token=HF_TOKEN,
            variant="fp16"
        )

        # Configurar scheduler correcto para SDXL-Turbo
        pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)

        pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
        return pipe
    except Exception as e:
        st.error(f"Error al cargar el modelo de difusión (SDXL-Turbo): {e}", icon="🚨")
        st.stop()

# Requisito 3: Modelo de Análisis (CLIP)
@st.cache_resource
def cargar_pipeline_analisis():
    try:
        analizador = hf_pipeline(
            "zero-shot-image-classification",
            model="openai/clip-vit-base-patch32",
            token=HF_TOKEN
        )
        return analizador
    except Exception as e:
        st.error(f"Error al cargar el modelo de análisis (CLIP): {e}", icon="🚨")
        st.stop()

# Opcional (Bonus): Modelo LLM (Gemini)
@st.cache_resource
def cargar_modelo_gemini():
    # Usamos el modelo multimodal recomendado
    model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')
    return model

# --- 4. Funciones del Pipeline ---

# Requisito 4 (Parte A): Procesamiento con SDXL-Turbo
def mejorar_imagen(pipe, imagen_original, strength=0.5):
    prompt = "foto de producto profesional, 8k, alta definicion, colores vibrantes, iluminacion de estudio, nitidez, sin sombras, alta calidad"
    negative_prompt = "oscuro, borroso, baja calidad, pixelado, feo, sombras, deformado"

    # Redimensionamos a 512x512 (SDXL-Turbo funciona bien en esta resolución)
    # Usamos thumbnail para MANTENER PROPORCIÓN y evitar deformaciones
    img_para_procesar = imagen_original.copy()
    img_para_procesar.thumbnail((512, 512))

    imagen_mejorada = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=img_para_procesar,
        num_inference_steps=4, # Más pasos para estabilidad
        guidance_scale=2.0,    # Guidance bajo pero no cero
        strength=strength      # Controla cuánto respeta la imagen original
    ).images[0]
    return imagen_mejorada, prompt # Devolvemos el prompt usado

# Requisito 4 (Parte B): Análisis Visual con CLIP
def analizar_calidad_clip(analizador, imagen):
    etiquetas_calidad = ["foto profesional", "foto brillante y clara", "foto de producto", "foto oscura", "foto borrosa", "foto de baja calidad"]
    resultado = analizador(imagen, candidate_labels=etiquetas_calidad)
    # Devolver la etiqueta con mayor puntaje
    return resultado[0]

# Función Profesional (Bonus): Guardar con Metadata (del Colab)
def preparar_descarga(imagen_mejorada, prompt_usado, strength):
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("prompt", prompt_usado)
    metadata.add_text("model", "stabilityai/sdxl-turbo")
    metadata.add_text("strength", str(strength))

    # Guardamos la imagen en memoria
    buffer = io.BytesIO()
    imagen_mejorada.save(buffer, format="PNG", pnginfo=metadata)
    buffer.seek(0)
    return buffer

# Opcional (Bonus): Análisis con Gemini
def analizar_mejoras_gemini(modelo_gemini, img_original, img_mejorada):
    try:
        prompt_gemini = [
            "Actúa como un experto en fotografía.\n",
            "Imagen Original:", img_original,
            "Imagen Mejorada:", img_mejorada,
            "\nCompara ambas imágenes. Describe en 2 o 3 frases cortas qué mejoras visuales se lograron en la 'Imagen Mejorada' (iluminación, contraste, colores).",
            "Responde en español."
        ]
        response = modelo_gemini.generate_content(prompt_gemini)
        return response.text
    except Exception as e:
        # Manejamos el error de cuota (429) u otros
        st.warning(f"No se pudo obtener el análisis de Gemini (Error: {e})", icon="⚠️")
        return "El análisis de Gemini no está disponible en este momento."

# --- 5. Lógica Principal de la UI (Diseño centrado en Laura) ---

# --- Controles en la Barra Lateral (Sidebar) ---
with st.sidebar:
    st.header("1. Carga tu Imagen")
    archivo_subido = st.file_uploader("Sube tu foto", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

    st.divider()

    st.header("2. Ajusta la Mejora")

    # Slider de Strength (más intuitivo para Laura)
    strength = st.slider(
        "Nivel de Creatividad",
        min_value=0.1,
        max_value=0.7,
        value=0.4, # Valor bajo (0.4) = Mejora sutil (respeta la original)
        step=0.05,
        help="Controla qué tanto cambia la IA tu imagen. **Valores bajos (0.2-0.4)** son mejores para mejoras sutiles. Valores altos (0.5-0.7) cambiarán más la imagen (más creativo)."
    )

    st.divider()

    # Checkbox para el Bonus de Gemini (Evita error 429)
    st.header("3. Análisis (Opcional)")
    generar_descripcion_gemini = st.checkbox(
        "Generar Descripción con IA (Bonus)",
        value=False,
        help="Si marcas esto, la IA de Gemini analizará la mejora y escribirá una descripción. (Puede fallar si se excede la cuota gratuita)."
    )

# --- Área Principal de Visualización ---
if not archivo_subido:
    st.info("Por favor, sube una imagen usando la barra lateral izquierda.")
    st.stop()

# Si hay imagen, cargamos modelos y mostramos
with st.spinner("Cargando modelos de IA (esto puede tardar un minuto)..."):
    pipe_difusion = cargar_pipeline_difusion()
    pipe_analisis_clip = cargar_pipeline_analisis()
    modelo_gemini = cargar_modelo_gemini()

st.success("¡Modelos cargados!")
st.divider()

img_original = Image.open(archivo_subido).convert("RGB")

# Requisito 5: Comparación Visual
col1, col2 = st.columns(2)
with col1:
    st.image(img_original, caption="Imagen Original", use_container_width=True)

# Botón para iniciar el pipeline
if st.button("✨ ¡Mejorar Imagen! ✨", use_container_width=True):

        # Requisito 4: Ejecución del Pipeline
        with st.spinner("Procesando con IA de Difusión (SDXL-Turbo)..."):
            img_mejorada, prompt_usado = mejorar_imagen(pipe_difusion, img_original, strength)

        with st.spinner("Analizando calidad con IA (CLIP)..."):
            analisis_clip = analizar_calidad_clip(pipe_analisis_clip, img_mejorada)

        # Solo corremos Gemini si el usuario lo pidió
        if generar_descripcion_gemini:
            with st.spinner("Generando descripción de mejoras (Gemini)..."):
                descripcion_gemini = analizar_mejoras_gemini(modelo_gemini, img_original, img_mejorada)
        else:
            descripcion_gemini = "Análisis opcional no solicitado."

        # Mostrar resultados
        with col2:
            st.image(img_mejorada, caption="Imagen Mejorada", use_column_width=True)

            # Preparamos los bytes para la descarga
            bytes_descarga = preparar_descarga(img_mejorada, prompt_usado, strength)

            # Botón de Descarga Profesional (Bonus)
            st.download_button(
                label="Descargar Imagen Mejorada (con Metadata)",
                data=bytes_descarga,
                file_name=f"mejorada_{archivo_subido.name}.png",
                mime="image/png",
                use_container_width=True
            )

        st.divider()
        st.subheader("🤖 Análisis de la IA")

        # Resultado del Análisis Obligatorio (CLIP)
        st.markdown("#### ✅ Análisis de Calidad (Req. 3)")
        st.write(f"El modelo de análisis (CLIP) clasifica la nueva imagen como:")
        st.success(f"**{analisis_clip['label'].capitalize()}** (Confianza: {analisis_clip['score']:.1%})")

        # Resultado del Análisis Opcional (Gemini)
        if generar_descripcion_gemini:
            st.markdown("#### 💬 Descripción de Mejoras (Bonus)")
            st.info(descripcion_gemini)