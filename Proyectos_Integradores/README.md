---
title: Track2 Mejorador Fotos
emoji: 🚀
colorFrom: blue
colorTo: red
sdk: streamlit
sdk_version: 1.51.0
app_file: app.py
pinned: false
---

✨ Restaurador de Fotos Antiguas con IA

Un sistema inteligente para recuperar memorias visuales, diseñado con arquitectura híbrida para garantizar disponibilidad continua.

📋 Descripción

Este proyecto es un Producto Mínimo Viable (MVP) desarrollado para el Trabajo Integrador N°2. Su objetivo es democratizar el acceso a herramientas de restauración fotográfica.

El sistema implementa una Arquitectura de Alta Disponibilidad que combina modelos de Inteligencia Artificial de última generación (Transformers) con algoritmos clásicos de procesamiento digital. Esto asegura que el usuario siempre obtenga una mejora en su imagen, independientemente de la saturación de los servidores de inferencia.

👤 User Persona

Nombre: Marta (55 años)
Contexto: Tiene cajas de zapatos llenas de fotos familiares de los años 70 y 80 que se están deteriorando.
Problema: Las fotos escaneadas se ven borrosas y con ruido. Las herramientas profesionales son caras y complejas.
Solución: Una web simple y robusta donde sube la foto y obtiene una versión mejorada al instante.

🚀 Características Técnicas (Track 1)

El sistema opera en dos niveles de procesamiento para cumplir con el requisito de restauración:

Nivel 1 - IA Generativa (Prioritario): Intenta procesar la imagen utilizando modelos SwinIR (Swin Transformer for Image Restoration). Estos modelos "alucinan" detalles perdidos para aumentar la resolución.

Nivel 2 - Procesamiento Algorítmico (Failover): Si las APIs de IA están saturadas (común en entornos de investigación gratuitos), el sistema activa automáticamente un motor local que aplica:

Median Filtering: Para eliminación de ruido y grietas ("sal y pimienta").

Adaptive Sharpening: Para recuperación de bordes.

Contrast Equalization: Para corregir la exposición.

Además incluye:

Análisis Semántico: Integración con el modelo BLIP para describir el contenido de la imagen (Vision-to-Text).

Filtros Post-Procesamiento: Opciones creativas (Sepia, B&N) aplicadas sobre la imagen restaurada.

🛠️ Stack Tecnológico

Frontend:

Streamlit (Python)

Modelos & APIs:

Restauración: mir-fan/SwinIR_4x / Eugenius/swin2SR

Visión: Salesforce/blip-image-captioning-large

Ingeniería de Software:

Sistema de Reintentos (Retries) con Backoff exponencial.

Manejo de errores HTTP y Timeouts.

Procesamiento de imágenes con Pillow y NumPy.

🏗️ Flujo de Datos

graph TD
    A[Input Usuario] --> B{¿API IA Disponible?}
    B -- Sí (200 OK) --> C[Inferencia SwinIR]
    B -- No (503/Timeout) --> D[Motor Local (Filtros)]
    C --> E[Imagen Mejorada]
    D --> E
    E --> F[Vision Transformer (BLIP)]
    F --> G[Output Final]


🧠 Justificación de Diseño

Se priorizó la Resiliencia del Sistema. En pruebas de estrés, las APIs públicas gratuitas tienen una tasa de fallo del 40-60% por "Cold Starts". Para evitar frustrar al usuario (Marta) con mensajes de error, se diseñó el "Modo Local" transparente. Esto cumple con los principios de Human-AI Interaction al mantener al usuario en control y productivo, informando sutilmente sobre el método utilizado.

💻 Ejecución

Clonar repositorio.

Instalar dependencias: pip install -r requirements.txt

Configurar HF_TOKEN en variables de entorno.

Ejecutar: streamlit run app.py


Autor: Daiana Elizabeth Gomez Materia: Procesamiento Digital de Imágenes - IFTS 24
Año: 2025 Profesor: Matias Barreto

---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference