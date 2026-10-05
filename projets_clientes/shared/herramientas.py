import os

# DICCIONARIO: cada color tiene su etiqueta y su código de consola
COLORES = {
    "ROJO": "\033[91m",
    "VERDE": "\033[92m",
    "AZUL": "\033[94m",
    "AMARILLO": "\033[93m",
    "CYAN": "\033[96m",
    "BLANCO": "\033[97m",
    "RESET": "\033[0m",
}

# TUPLA: respuestas afirmativas aceptadas. Es fija, por eso no es lista.
RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")


def limpiar_pantalla():
    os.system("clear" if os.name == "posix" else "cls")


def imprimir_color(texto, color):
    codigo = COLORES.get(color, COLORES["BLANCO"])   # .get evita el error si el color no existe
    print(f"{codigo}{texto}{COLORES['RESET']}")

imprimir_color()
def imprimir_titulo(texto):
    limpiar_pantalla()
    imprimir_color("=" * 60, "AZUL")
    print(f"  {texto}".center(60))
    imprimir_color("=" * 60, "AZUL")
    print()


def imprimir_exito(mensaje):
    imprimir_color(f"✓ {mensaje}", "VERDE")


def imprimir_error(mensaje):
    imprimir_color(f"✗ {mensaje}", "ROJO")


def imprimir_info(mensaje):
    imprimir_color(f"ℹ {mensaje}", "CYAN")


def confirmar(pregunta):
    # Devuelve True si el usuario respondió algo de la tupla RESPUESTAS_SI
    respuesta = input(f"{pregunta} (si/no): ").strip().lower()
    return respuesta in RESPUESTAS_SI


def es_email_valido(texto):
    # Validación mínima: un @, algo antes, algo después y un punto al final
    texto = texto.strip()
    if texto.count("@") != 1:
        return False
    usuario, dominio = texto.split("@")
    return len(usuario) > 0 and "." in dominio and not dominio.endswith(".")

if __name__ == "__main__":
    # Pruebas rápidas: se ejecutan solo al correr este archivo directamente
    imprimir_titulo("PRUEBA DE HERRAMIENTAS")

    # Colores: incluye uno inexistente para comprobar la validación
    for color in ("ROJO", "VERDE", "AZUL", "AMARILLO", "MORADO"):
        imprimir_color(f"Texto en {color}", color)
    print()

    # Tipos de mensajes
    imprimir_exito("Operación realizada correctamente")
    imprimir_error("Algo salió mal")
    imprimir_info("Mensaje informativo")
    print()

    # Emails: los válidos salen en verde y los inválidos en rojo
    emails = (
        "juan@gmail.com",
        " ana.perez@unemi.edu.ec ",
        "sinarroba.com",
        "dos@@gmail.com",
        "@gmail.com",
        "juan@gmail",
        "juan@gmail.",
    )

    for email in emails:
        if es_email_valido(email):
            imprimir_exito(f"Email válido: {email}")
        else:
            imprimir_error(f"Email inválido: {email}")
    print()

    # confirmar pide entrada del usuario
    if confirmar("¿La prueba funcionó?"):
        imprimir_exito("Respondiste que sí")
    else:
        imprimir_info("Respondiste que no")
es_email_valido()
