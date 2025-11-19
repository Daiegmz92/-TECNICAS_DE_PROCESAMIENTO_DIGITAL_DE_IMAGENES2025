Markdown

# 🧠 Técnicas de Procesamiento Digital de Imágenes (2025)

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-5C3EE8?style=flat&logo=opencv&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep_Learning-EE4C2C?style=flat&logo=pytorch&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![HuggingFace](https://img.shields.io/badge/Hugging_Face-Inference-FFD21E?style=flat&logo=huggingface&logoColor=black)

> **Repositorio Oficial de Cursada**
> **Tecnicatura Superior en Ciencia de Datos e IA - IFTS N°24**

Este repositorio consolida el trabajo práctico, laboratorios y proyectos integradores desarrollados durante el ciclo lectivo 2025. Abarca desde los fundamentos matemáticos de la imagen digital hasta la implementación de pipelines de Deep Learning y Generación de Imágenes en la nube.

---

## 👩‍💻 Información del Estudiante
* **Desarrolladora:** Daiana Elizabeth Gomez
* **Profesor:** Matías Barreto
* **Año:** 2025
* **Materia:** Técnicas de Procesamiento Digital de Imágenes

---

## 🌟 Proyectos Destacados (Integradores)

### 🏆 Trabajo Integrador Final: Restaurador de Fotos Antiguas con IA
**Descripción:** Sistema híbrido y resiliente para la recuperación de patrimonio fotográfico. Combina modelos de Super-Resolución en la nube (SwinIR) con procesamiento local de respaldo.
* **Features:** Restauración facial, análisis semántico con BLIP, filtros estéticos y fallback automático.
* **Stack:** Streamlit, Hugging Face Inference API, PIL.
* **Deploy:** [Ver Demo en Hugging Face Spaces](https://huggingface.co/spaces/daiegmz92/Restaurador_de_Fotos_Antiguas_MVP) *(Agregar tu link real)*

### 📄 Trabajo Integrador N°1: Análisis de Documentos Digitales
**Descripción:** Pipeline de visión clásica para preprocesamiento y corrección de documentos escaneados con defectos.
* **Técnicas:** Corrección de perspectiva (Homografía), Detección de bordes (Canny), Mejora de iluminación (CLAHE) y Segmentación por color (K-Means/HSV).
* **Caso de éxito:** Rectificación automática de documentos rotados y recuperación de textos con sombras severas.

---

## 🧪 Laboratorios y Prácticas (TPs)

Colección de experimentos y mini-proyectos organizados por unidad temática:

| Unidad | Proyecto / Práctica | Tecnologías Clave |
| :--- | :--- | :--- |
| **Biometría** | **Detector de Landmarks Faciales**<br>Mapeo de 478 puntos faciales en tiempo real para análisis de expresiones. | `MediaPipe`, `Streamlit` |
| **Accesibilidad** | **Asistente Visual (Image-to-Speech)**<br>Comparación entre modelos pre-entrenados (DETR+CLIP) vs personalizados. | `Transformers`, `Teachable Machine`, `gTTS` |
| **Deep Learning** | **Clasificación & Transfer Learning**<br>Implementación de ResNet18 para clasificación de imágenes. | `PyTorch`, `Torchvision` |
| **GenAI** | **Difusión Estable & Estilo**<br>Experimentos con Stable Diffusion y Neural Style Transfer. | `Diffusers`, `Keras` |
| **Fundamentos** | **Manipulación de Pixeles**<br>Operaciones morfológicas, histogramas y filtros de convolución. | `NumPy`, `Matplotlib` |

---

## 🛠️ Stack Tecnológico

Las herramientas y librerías utilizadas a lo largo del curso incluyen:

* **Lenguaje:** `Python 3.x`
* **Visión Clásica:** `OpenCV`, `scikit-image`, `PIL (Pillow)`
* **Análisis de Datos:** `NumPy`, `Pandas`, `Matplotlib`, `Seaborn`
* **Deep Learning:** `PyTorch`, `TensorFlow`, `Keras`
* **Despliegue & UI:** `Streamlit`, `Gradio`
* **Cloud AI:** `Hugging Face Hub`, `Google Colab`

---

## 📂 Estructura del Repositorio

```bash
├── 01_Fundamentos/          # Introducción, histogramas y filtros básicos
├── 02_Vision_Clasica/       # Operaciones morfológicas, bordes y segmentación
├── 03_Deep_Learning/        # CNNs, Transfer Learning (ResNet)
├── 04_Proyectos_Streamlit/  # Código fuente de las apps (Landmarks, Restaurador)
├── Integrador_1/            # Notebooks e informes del TI 1
├── Integrador_2/            # Archivos del proyecto final
└── README.md
📢 Contacto & Redes
Si te interesa alguno de estos proyectos o quieres colaborar:

(Agrega tu link)

Repositorio creado con fines académicos - 2025


### ✨ ¿Qué mejoró?
1.  **Badges al inicio:** Le da un look muy "developer pro".
2.  **Tabla para los Labs:** Es mucho más fácil de leer que una lista plana.
3.  **Jerarquía:** Separé claramente los **Integradores** (que son lo más importante) del resto de las prácticas.
4.  **Links:** Dejé espacios listos para que pongas tus links reales (a la demo, a tu LinkedIn).
5.  **Estructura de carpetas:** Agregué un árbol de directorios sugerido para mostrar orden.

Copia el código dentro del bloque, pégalo en tu archivo `README.md` en GitHub, ¡y recu
