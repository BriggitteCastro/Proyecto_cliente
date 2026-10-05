from models import CAMPOS_ESTUDIANTE
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import (
    crear_estudiante, obtener_todos, obtener_por_id, buscar_estudiantes,
    actualizar_estudiante, eliminar_estudiante, agregar_nota,
    materias_ofertadas, estudiantes_en_comun
)


def pausa():
    input("\nPresione Enter para continuar...")


def mostrar_tabla(estudiantes):
    print(f"{'ID':<5}{'CARNET':<15}{'NOMBRE':<25}{'EMAIL':<25}{'PROMEDIO':<10}")
    print("-" * 80)
    for est in estudiantes:
        print(f"{est.id:<5}{est.carnet:<15}{est.obtener_nombre_completo():<25}"
              f"{est.email:<25}{est.obtener_promedio():<10}")
    print("-" * 80)


def opcion_crear():
    imprimir_titulo("CREAR NUEVO ESTUDIANTE")
    datos = {}
    for campo in CAMPOS_ESTUDIANTE:
        datos[campo] = input(f"{campo.capitalize()}: ")

    exito, mensaje = crear_estudiante(datos)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_ver_todos():
    imprimir_titulo("LISTA DE ESTUDIANTES")
    estudiantes = obtener_todos()
    if not estudiantes:
        imprimir_info("No hay estudiantes registrados.")
    else:
        mostrar_tabla(estudiantes)
    pausa()


def opcion_buscar():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Término de búsqueda: ")
    resultados = buscar_estudiantes(termino)
    if not resultados:
        imprimir_info("No se encontraron coincidencias.")
    else:
        mostrar_tabla(resultados)
    pausa()


def opcion_ver_promedio():
    imprimir_titulo("VER PROMEDIO Y DETALLE")
    try:
        id_est = int(input("ID del estudiante: "))
    except ValueError:
        imprimir_error("ID no válido")
        return pausa()

    est = obtener_por_id(id_est)
    if not est:
        imprimir_error("Estudiante inexistente")
    else:
        print(f"Estudiante: {est.obtener_nombre_completo()}")
        print(f"Carnet    : {est.carnet}")
        print(f"Promedio  : {est.obtener_promedio()}")
        print("Notas por materia:")
        for mat, notas in est.notas.items():
            print(f"  - {mat}: {notas}")
    pausa()


def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    try:
        id_est = int(input("ID del estudiante a editar: "))
    except ValueError:
        imprimir_error("ID no válido")
        return pausa()

    est = obtener_por_id(id_est)
    if not est:
        imprimir_error("Estudiante inexistente")
        return pausa()

    cambios = {}
    for campo in CAMPOS_ESTUDIANTE:
        actual = getattr(est, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    exito, mensaje = actualizar_estudiante(id_est, cambios)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_eliminar():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    try:
        id_est = int(input("ID del estudiante a eliminar: "))
    except ValueError:
        imprimir_error("ID no válido")
        return pausa()

    est = obtener_por_id(id_est)
    if not est:
        imprimir_error("Estudiante inexistente")
        return pausa()

    if confirmar(f"¿Desea eliminar a {est.obtener_nombre_completo()}?"):
        exito, mensaje = eliminar_estudiante(id_est)
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)
    pausa()


def opcion_agregar_nota():
    imprimir_titulo("AGREGAR NOTA")
    try:
        id_est = int(input("ID del estudiante: "))
        materia = input("Materia: ")
        nota = float(input("Nota (0-20): "))
    except ValueError:
        imprimir_error("Error: Entrada numérica no válida")
        return pausa()

    exito, mensaje = agregar_nota(id_est, materia, nota)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_materias_ofertadas():
    imprimir_titulo("TODAS LAS MATERIAS (SET)")
    materias = materias_ofertadas()
    if not materias:
        imprimir_info("No hay materias inscritas aún.")
    else:
        print("Materias ofertadas/inscritas:")
        for m in sorted(materias):
            print(f"  • {m}")
    pausa()


def opcion_materias_en_comun():
    imprimir_titulo("MATERIAS EN COMÚN (INTERSECCIÓN DE CONJUNTOS)")
    try:
        id_a = int(input("ID Primer estudiante: "))
        id_b = int(input("ID Segundo estudiante: "))
    except ValueError:
        imprimir_error("IDs no válidos")
        return pausa()

    compartidas, mensaje = estudiantes_en_comun(id_a, id_b)
    if compartidas is None:
        imprimir_error(mensaje)
    elif not compartidas:
        imprimir_info("No tienen ninguna materia en común.")
    else:
        imprimir_exito(mensaje)
        for m in sorted(compartidas):
            print(f"  ✓ {m}")
    pausa()


OPCIONES = {
    "1": ("Crear estudiante", opcion_crear),
    "2": ("Ver todos", opcion_ver_todos),
    "3": ("Buscar estudiante", opcion_buscar),
    "4": ("Ver promedio y detalle", opcion_ver_promedio),
    "5": ("Actualizar estudiante", opcion_actualizar),
    "6": ("Eliminar estudiante", opcion_eliminar),
    "7": ("Agregar nota", opcion_agregar_nota),
    "8": ("Ver materias ofertadas", opcion_materias_ofertadas),
    "9": ("Materias en común", opcion_materias_en_comun),
    "0": ("Salir", lambda: "salir"),
}


def main():
    while True:
        imprimir_titulo("SISTEMA DE GESTIÓN DE ESTUDIANTES")
        for k, (texto, _) in OPCIONES.items():
            print(f"  {k}. {texto}")
        print()

        op = input("Seleccione una opción: ").strip()
        if op in OPCIONES:
            res = OPCIONES[op][1]()
            if res == "salir":
                break
        else:
            imprimir_error("Opción inválida")
            pausa()


if __name__ == "__main__":
    main()