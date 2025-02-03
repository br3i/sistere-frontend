import colorsys

# Colores pasteles primarios y sus contrastes (en tonos pasteles)
colors_allowed = [
    "#FFEB3B",  # Amarillo Brillante
    "#FF4081",  # Rosa Brillante
    "#2196F3",  # Azul Brillante
    "#4CAF50",  # Verde Brillante
    "#FF9800",  # Naranja Brillante
    "#9C27B0",  # Púrpura Brillante
]


def get_opposite_bright_color(hex_color):
    # Convertir hex a RGB
    r, g, b = [int(hex_color[i : i + 2], 16) for i in (1, 3, 5)]

    # Convertir RGB a HLS
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)

    # Invertir el color en el círculo cromático (opuesto)
    h_opposite = (h + 0.5) % 1.0  # Desplazar el tono 180 grados

    # Asegurar que la saturación y la luminosidad se mantengan altas para colores brillantes
    l_bright = 0.8  # Luminosidad alta (80%)
    s_bright = 1.0  # Saturación máxima

    # Convertir de vuelta a RGB
    r_opposite, g_opposite, b_opposite = colorsys.hls_to_rgb(
        h_opposite, l_bright, s_bright
    )

    # Convertir a valores entre 0-255
    r_opposite, g_opposite, b_opposite = (
        int(r_opposite * 255),
        int(g_opposite * 255),
        int(b_opposite * 255),
    )

    # Convertir a hex
    opposite_color = f"#{r_opposite:02X}{g_opposite:02X}{b_opposite:02X}"
    return opposite_color
