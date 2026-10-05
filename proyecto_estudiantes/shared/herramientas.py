# shared/herramientas.py
import os

# DICCIONARIO: Cada color tiene su etiqueta y código de consola
COLORES = {
    "ROJO": "\033[91m",
    "VERDE": "\033[92m",
    "AZUL": "\033[94m",
    "AMARILLO": "\033[93m",
    "CYAN": "\033[96m",
    "BLANCO": "\033[97m",
    "RESET": "\033[0m",
}

# TUPLA: Respuestas afirmativas aceptadas (inmutable)
RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")


def limpiar_pantalla():
    """Limpia la consola dependiendo del sistema operativo."""
    os.system("clear" if os.name == "posix" else "cls")


def imprimir_color(texto, color="BLANCO"):
    """Imprime un texto aplicándole el color indicado según el diccionario COLORES."""
    codigo = COLORES.get(color, COLORES["BLANCO"])  # .get evita errores si el color no existe
    print(f"{codigo}{texto}{COLORES['RESET']}")


def imprimir_titulo(texto):
    """Limpia la pantalla y muestra un encabezado centrado."""
    limpiar_pantalla()
    imprimir_color("=" * 60, "AZUL")
    print(f"  {texto}".center(60))
    imprimir_color("=" * 60, "AZUL")
    print()


def imprimir_exito(mensaje):
    """Muestra mensajes de éxito en verde."""
    imprimir_color(f"✓ {mensaje}", "VERDE")


def imprimir_error(mensaje):
    """Muestra mensajes de error en rojo."""
    imprimir_color(f"✗ Error: {mensaje}", "ROJO")


def imprimir_info(mensaje):
    """Muestra mensajes informativos en cyan."""
    imprimir_color(f"ℹ {mensaje}", "CYAN")


def confirmar(pregunta):
    """Pide confirmación al usuario (si/no) usando la tupla RESPUESTAS_SI."""
    respuesta = input(f"{pregunta} (si/no): ").strip().lower()
    return respuesta in RESPUESTAS_SI


def es_email_valido(texto):
    """Validación mínima de formato de correo electrónico."""
    texto = texto.strip()
    if texto.count("@") != 1:
        return False
    usuario, dominio = texto.split("@")
    return len(usuario) > 0 and "." in dominio and not dominio.endswith(".")


def es_carnet_valido(carnet):
    """
    Validación básica del carnet de estudiante.
    Debe tener al menos 4 caracteres y contener letras/números (ejemplo: EST2026001).
    """
    carnet = carnet.strip()
    return len(carnet) >= 4 and carnet.isalnum()


if __name__ == "__main__":
    # Bloque de pruebas directas del módulo de herramientas
    imprimir_titulo("PRUEBAS DE HERRAMIENTAS - SISTEMA DE ESTUDIANTES")

    # Prueba 1: Colores
    for c in ("ROJO", "VERDE", "AZUL", "AMARILLO", "CYAN", "DESCONOCIDO"):
        imprimir_color(f"Probandocolor {c}", c)
    print()

    # Prueba 2: Tipos de mensajes
    imprimir_exito("Estudiante registrado correctamente")
    imprimir_error("No se pudo agregar la nota (fuera de rango)")
    imprimir_info("Mostrando materias en común")
    print()

    # Prueba 3: Validación de Emails
    emails_prueba = ("ana@escuela.edu", "estudiante@unemi.edu.ec", "correo_invalido.com")
    for email in emails_prueba:
        if es_email_valido(email):
            imprimir_exito(f"Email válido: {email}")
        else:
            imprimir_error(f"Email inválido: {email}")
    print()

    # Prueba 4: Validación de Carnets
    carnets_prueba = ("EST2026001", "A1", "  ")
    for carnet in carnets_prueba:
        if es_carnet_valido(carnet):
            imprimir_exito(f"Carnet válido: {carnet}")
        else:
            imprimir_error(f"Carnet inválido: '{carnet}'")
    print()

    # Prueba 5: Confirmación
    if confirmar("¿Deseas guardar los cambios?"):
        imprimir_exito("Cambios guardados.")
    else:
        imprimir_info("Acción cancelada.")