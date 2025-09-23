import py5

def setup():
    py5.size(400, 400)  # Tamaño del lienzo
    py5.background(255)

    # Cargar imagen
    img = py5.load_image("imagen1.jpg")

    # Mostrar imagen en la ventana
    py5.image(img, 0, 0, 400, 400)  # Escalar a tamaño del lienzo

py5.run_sketch()