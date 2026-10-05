# models.py
# USO DE TUPLES: CAMPOS_ESTUDIANTE es una tupla inmutable con las claves principales
CAMPOS_ESTUDIANTE = ("nombre", "apellido", "email", "carnet")


class Estudiante:
    """MODELO: Representa la entidad Estudiante y sus métodos."""

    def __init__(self, id_estudiante, nombre, apellido, email, carnet, notas=None, materias=None):
        self.id = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carnet = carnet
        # USO DE DICCIONARIO Y LISTA: Dicc de materias que apunta a una lista de notas [18, 19, 20]
        self.notas = notas if notas else {}
        # USO DE SET: Conjunto de materias sin elementos duplicados
        self.materias = set(materias) if materias else set()

    def obtener_nombre_completo(self):
        return "{self.nombre} {self.apellido}"

    def inscribir_materia(self, materia):
        self.materias.add(materia)

    def agregar_nota(self, materia, nota):
        self.inscribir_materia(materia)
        self.notas.setdefault(materia, []).append(nota)

    def obtener_promedio(self):
        todas_las_notas = []
        for lista_notas in self.notas.values():
            todas_las_notas.extend(lista_notas)
        if not todas_las_notas:
            return 0.0
        return round(sum(todas_las_notas) / len(todas_las_notas), 2)

    def materias_en_comun(self, otro_estudiante):
        # Operación de intersección con CONJUNTOS (set & set)
        return self.materias & otro_estudiante.materias

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
            "notas": self.notas,
            # JSON no soporta sets, por lo que se convierte a una lista ordenada al guardar
            "materias": sorted(self.materias),
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["carnet"],
            notas=datos.get("notas", {}),
            # Al leer del JSON, la lista vuelve a convertirse en un set
            materias=set(datos.get("materias", [])),
        )

    def __str__(self):
        return f"[{self.carnet}] {self.obtener_nombre_completo()} - Promedio: {self.obtener_promedio()}"