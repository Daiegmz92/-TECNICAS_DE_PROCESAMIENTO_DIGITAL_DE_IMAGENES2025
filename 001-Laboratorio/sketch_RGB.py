import py5

def setup():
    py5.size(400, 400)                 # Lienzo de 400x400
    py5.color_mode(py5.RGB)            # Modo de color RGB
    py5.background(255)                # Fondo blanco

    py5.no_stroke()                    # Sin borde

    py5.fill(64, 224, 208)             # Turquesa-verde (RGB)
    py5.triangle(200, 100, 100, 300, 300, 300)  # Triángulo centrado

    py5.save_frame("figura_rgb.jpg")   # Guardar imagen como JPEG

py5.run_sketch()