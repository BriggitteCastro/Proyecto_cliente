# views.py
from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

gestor = GestorJSON("data/estudiantes.json")


def carnets_registrados(excepto_id=None):
    """Uso de SET para validar duplicados de carnet en tiempo constante."""
    return {
        registro["carnet"].upper()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def emails_registrados(excepto_id=None):
    """Uso de SET para validar duplicados de email."""
    return {
        registro["email"].lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def siguiente_id():
    ids = [registro["id"] for registro in gestor.leer()]
    return max(ids) + 1 if ids else 1


# --- OPERACIONES CRUD ---

def crear_estudiante(datos):
    try:
        valores = {campo: str(datos.get(campo, "")).strip() for campo in CAMPOS_ESTUDIANTE}

        faltantes = [campo for campo in CAMPOS_ESTUDIANTE if not valores[campo]]
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no es válido"

        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya está registrado"

        # Validación del carnet usando SET
        if valores["carnet"].upper() in carnets_registrados():
            return False, f"El carnet '{valores['carnet']}' ya se encuentra registrado"

        valores["carnet"] = valores["carnet"].upper()
        estudiante = Estudiante(siguiente_id(), **valores)

        registros = gestor.leer()
        registros.append(estudiante.a_diccionario())
        gestor.guardar(registros)

        return True, f"Estudiante {estudiante.obtener_nombre_completo()} creado con éxito"

    except Exception as error:
        return False, f"Error: {error}"


def obtener_todos():
    return [Estudiante.desde_diccionario(reg) for reg in gestor.leer()]


def obtener_por_id(id_estudiante):
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante
    return None


def buscar_estudiantes(termino):
    termino = termino.strip().lower()
    if not termino:
        return []

    encontrados = []
    for registro in gestor.leer():
        for campo in CAMPOS_ESTUDIANTE:
            if termino in str(registro.get(campo, "")).lower():
                encontrados.append(Estudiante.desde_diccionario(registro))
                break
    return encontrados


def actualizar_estudiante(id_estudiante, cambios):
    try:
        if not cambios:
            return False, "No se especificó ningún cambio"

        if "email" in cambios:
            if not es_email_valido(cambios["email"]):
                return False, "El email no es válido"
            if cambios["email"].lower() in emails_registrados(excepto_id=id_estudiante):
                return False, "Ese email ya está en uso"

        if "carnet" in cambios:
            carnet_nuevo = cambios["carnet"].upper()
            if carnet_nuevo in carnets_registrados(excepto_id=id_estudiante):
                return False, "Ese carnet ya está en uso"
            cambios["carnet"] = carnet_nuevo

        registros = gestor.leer()
        posicion = None
        for i, reg in enumerate(registros):
            if reg["id"] == id_estudiante:
                posicion = i
                break

        if posicion is None:
            return False, f"No existe un estudiante con id {id_estudiante}"

        registros[posicion].update(cambios)
        gestor.guardar(registros)
        return True, f"Estudiante {id_estudiante} actualizado"

    except Exception as error:
        return False, f"Error: {error}"


def eliminar_estudiante(id_estudiante):
    registros = gestor.leer()
    quedan = [r for r in registros if r["id"] != id_estudiante]

    if len(quedan) == len(registros):
        return False, f"No existe el estudiante con ID {id_estudiante}"

    gestor.guardar(quedan)
    return True, f"Estudiante {id_estudiante} eliminado correctamente"


# --- FUNCIONES ADICIONALES PEDIDAS EN LA GUÍA ---

def agregar_nota(id_estudiante, materia, nota):
    """Agrega una nota validando que esté entre 0 y 20."""
    # Validación de nota fuera de rango (Rúbrica)
    if not isinstance(nota, (int, float)) or not (0 <= nota <= 20):
        return False, "La nota debe ser un número entre 0 y 20"

    materia = materia.strip().title()
    if not materia:
        return False, "El nombre de la materia no puede estar vacío"

    registros = gestor.leer()
    estudiante = None

    for reg in registros:
        if reg["id"] == id_estudiante:
            estudiante = Estudiante.desde_diccionario(reg)
            break

    if not estudiante:
        return False, f"No existe el estudiante con ID {id_estudiante}"

    estudiante.agregar_nota(materia, nota)

    nuevos_registros = [
        estudiante.a_diccionario() if r["id"] == id_estudiante else r
        for r in registros
    ]

    gestor.guardar(nuevos_registros)
    return True, f"Nota {nota} añadida en {materia} a {estudiante.obtener_nombre_completo()}"


def materias_ofertadas():
    """Devuelve un SET con todas las materias inscritas por todos los estudiantes."""
    todas_las_materias = set()
    for est in obtener_todos():
        todas_las_materias |= est.materias  # Unión de conjuntos
    return todas_las_materias


def estudiantes_en_comun(id_a, id_b):
    """Devuelve la intersección de conjuntos de materias entre dos estudiantes."""
    est_a = obtener_por_id(id_a)
    est_b = obtener_por_id(id_b)

    if not est_a or not est_b:
        return None, "Uno o ambos estudiantes no existen"

    compartidas = est_a.materias_en_comun(est_b)
    return compartidas, f"Materias en común entre {est_a.nombre} y {est_b.nombre}"