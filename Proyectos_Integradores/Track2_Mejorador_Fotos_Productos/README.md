<<<<<<< HEAD
# 🚀 Restaurador de Imágenes MVP (TP Integrador N°2)

Este es un Producto Mínimo Viable (MVP) para el Trabajo Práctico Integrador N°2 de la materia "Procesamiento Digital de Imágenes e Introducción a Visión por Computadora" (IFTS 24, Prof. Matías Barreto).

El sistema utiliza un pipeline de IA generativa para cumplir con el **Track 2: Restauración y Enhancement**.

**Link a la App Desplegada:** [Pega tu link de Hugging Face Spaces aquí]

## 1. Descripción del Problema y User Persona

Este proyecto sigue una filosofía de MVP centrada en un usuario específico.

* **User Persona:** "Laura, vendedora de e-commerce."
* **Contexto:** Laura saca fotos de sus productos con su celular para su tienda online.
* **Problema:** Sus fotos a menudo salen **oscuras, opacas o con mal balance de blancos**. No tiene tiempo ni conocimientos de software de edición complejo como Photoshop.
* **Solución (Este MVP):** Una herramienta web simple donde Laura sube su foto. La IA la procesa y le devuelve una versión **más brillante, nítida y con colores vibrantes**, lista para usar en su tienda.

## 2. Arquitectura del Sistema y Stack Tecnológico

El pipeline completo (Req. 4) sigue esta arquitectura:

1. **UI (Streamlit)**: El usuario sube una imagen.
2. **Procesamiento (Difusión)**: La imagen se pasa a un pipeline `Img2Img` de **Stable Diffusion 1.5** acelerado con **LCM-LoRA**. Un prompt positivo (`"foto profesional, colores vibrantes..."`) guía al modelo para mejorarla.
3. **Análisis (Visión)**: La imagen *mejorada* se envía a **Hugging Face CLIP** para un análisis de clasificación "zero-shot".
4. **Análisis (LLM - Bonus)**: La imagen *original* y la *mejorada* se envían a **Gemini 1.5 Flash** para generar una descripción en lenguaje natural de las mejoras.
5. **Resultados**: La UI muestra la comparación lado a lado (Req. 5) y los resultados de ambos análisis (Req. 3).

**Stack Tecnológico (Req. 8):**
* **UI:** Streamlit
* **Modelo de Difusión:** `runwayml/stable-diffusion-v1-5` + `latent-consistency/lcm-lora-sdv1-5` (vía `diffusers`)
* **Modelo de Análisis:** `openai/clip-vit-base-patch32` (vía `transformers`)
* **Modelo LLM (Bonus):** `gemini-1.5-flash` (vía `google-generativeai`)
* **Deployment:** Hugging Face Spaces

## 3. Decisiones de Diseño (Principios HAI)

El diseño está justificado desde la interacción Humano-IA (HAI):

* **Transparencia (Req. 8):** El usuario sabe qué está pasando mediante `st.spinner` (ej. "Procesando con Difusión...").
* **Control (Req. 8):** El usuario tiene el control de iniciar el proceso con un botón claro ("¡Mejorar Imagen!").
* **Explicabilidad (Req. 8):** Este es el punto clave. No solo mostramos la imagen.
    1. **CLIP** provee una "etiqueta" de calidad (ej. "foto profesional").
    2. **Gemini (Bonus)** explica *por qué* es mejor en lenguaje natural (ej. "La iluminación es más uniforme").
* **Manejo de Errores (Req. 8):** El código verifica la presencia de API keys y muestra un `st.error` claro si faltan.

## 4. Conceptos de Procesamiento Digital Aplicados (Req. 9)

Este proyecto aplica los siguientes conceptos de la materia:

* **Transformaciones de Intensidad:** El pipeline `img2img` ajusta el brillo y el contraste de la imagen para que coincida con el prompt de "iluminación de estudio".
* **Filtros de Realce (Sharpening):** El modelo de difusión aplica un realce de nitidez para cumplir con la solicitud de "alta definición" y "nitidez" del prompt.
* **Ecualización de Histograma (Conceptual):** El proceso de mejora de iluminación y contraste es una forma avanzada de ecualización, donde la IA redistribuye la intensidad de los píxeles de forma inteligente.

## 5. Instalación y Ejecución Local

1. Clonar el repositorio:
    ```bash
    git clone [TU_URL_DE_GITHUB]
    cd tu-proyecto
    ```
2. Crear un entorno virtual e instalar dependencias:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3. Crear un archivo `.env` para tus API keys (NO subas este archivo a GitHub):
    ```
    HF_TOKEN="hf_TuTokenDeHuggingFace"
    GEMINI_API_KEY="TuTokenDeGoogleAI"
    ```
4. Ejecutar la aplicación:
    ```bash
    streamlit run app.py
    ```

## 6. Limitaciones Conocidas (Req. 8)

* **Velocidad:** Al correr en el *tier* gratuito de HF Spaces (CPU), el proceso puede tardar entre 30 y 60 segundos.
* **Identidad:** El modelo `SD 1.5` puede alterar ligeramente los detalles finos del producto. No es un `ControlNet` o `InstantID` (que serían una mejora futura).
* **Calidad de LCM:** LCM-LoRA es extremadamente rápido pero puede ser ligeramente de menor calidad que SD 1.5 estándar.
=======
# 🧠 Procesamiento de Imágenes Digitales y Visión por Computadora

Este repositorio reúne contenidos y prácticas de la materia, desde fundamentos ópticos hasta técnicas modernas de visión por computadora y generación de imágenes.

## 🧪 Temas principales

- Representación y adquisición de imágenes digitales
- Procesamiento elemental: realce, bordes, ruido
- Operaciones geométricas y análisis de textura
- Segmentación y clasificación de objetos
- Redes neuronales convolucionales (CNNs), Transformers
- Generación de imágenes: GANs, Stable Diffusion
- Reconstrucción 3D y detección de anomalías

## 🛠️ Herramientas utilizadas

- **Google Colab** para desarrollo y ejecución
- **Python** como lenguaje principal
- **Librerías**:
  - `OpenCV`, `scikit-image`, `PIL` para procesamiento
  - `NumPy`, `Matplotlib`, `Seaborn` para análisis y visualización
  - `PyTorch`, `TensorFlow`, `Keras` para modelos de aprendizaje profundo
- **Markdown** para documentación técnica
- **GitHub** para control de versiones y entrega colaborativa

>>>>>>> 1afe7da5624bd767c3f0c09a2e28255b95c69007
