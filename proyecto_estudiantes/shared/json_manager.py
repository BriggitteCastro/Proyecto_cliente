# shared/json_manager.py
import json
import os


class GestorJSON:
    """Clase encargada de la lectura y escritura de datos en formato JSON."""

    def __init__(self, ruta_archivo="data/estudiantes.json"):
        self.ruta_archivo = ruta_archivo
        self._asegurar_directorio()

    def _asegurar_directorio(self):
        """Crea la carpeta contenedora si no existe para evitar errores de ruta."""
        directorio = os.path.dirname(self.ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)

    def leer(self):
        """
        Lee los registros desde el archivo JSON.
        Si el archivo no existe o está dañado, retorna una lista vacía.
        """
        if not os.path.exists(self.ruta_archivo):
            return []

        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, OSError):
            return []

    def guardar(self, datos):
        """
        Guarda la lista de diccionarios en el archivo JSON con formato indentado.
        
        Soporta la conversión automática de 'set' a 'list' si algún objeto
        contiene conjuntos de datos.
        """
        self._asegurar_directorio()

        def convertidor_custom(objeto):
            # Convierte los objetos de tipo set a list para ser serializados a JSON
            if isinstance(objeto, set):
                return sorted(list(objeto))
            raise TypeError(f"El objeto de tipo {type(objeto).__name__} no es serializable a JSON")

        try:
            with open(self.ruta_archivo, "w", encoding="utf-8") as archivo:
                json.dump(
                    datos,
                    archivo,
                    ensure_ascii=False,
                    indent=4,
                    default=convertidor_custom
                )
            return True
        except Exception as error:
            print(f"Error al guardar datos en JSON: {error}")
            return False


if __name__ == "__main__":
    # Prueba rápida del gestor de JSON
    from herramientas import imprimir_titulo, imprimir_exito, imprimir_info

    imprimir_titulo("PRUEBA DE JSON MANAGER")

    gestor_prueba = GestorJSON("data/prueba_estudiantes.json")

    # Datos de ejemplo incluyendo un 'set'
    estudiantes_ejemplo = [
        {
            "id": 1,
            "nombre": "Ana",
            "apellido": "Pérez",
            "email": "ana@escuela.edu",
            "carnet": "EST2026001",
            "notas": {"Matemática": [18, 19, 20]},
            "materias": {"Matemática", "Inglés"}  # Se guarda como Set
        }
    ]

    if gestor_prueba.guardar(estudiantes_ejemplo):
        imprimir_exito("Datos guardados con éxito en data/prueba_estudiantes.json")

    datos_leidos = gestor_prueba.leer()
    imprimir_info(f"Registros leídos: {len(datos_leidos)}")
    print(datos_leidos)