import py5

def setup():
    # Crear lienzo de 400x400 píxeles
    py5.size(400, 400)

    # Cambiar modo de color a HSV 
    py5.color_mode(py5.HSB, 360, 100, 100)

    # Fondo blanco (en HSV: matiz no importa si saturación y brillo son 0)
    py5.background(0, 0, 100)

    py5.no_stroke()  # Sin borde

    # Dibujar Cuadrado
    py5.rect_mode(py5.CENTER)

    # 5. Asignar color de relleno en HSV
    py5.fill(200, 80, 90)  # Matiz 180 = cian, saturación 80%, brillo 90%
    py5.rect(200, 200, 150, 150)

    # Guardar imagen 
    py5.save_frame("figura_hsv.jpg")

py5.run_sketch()