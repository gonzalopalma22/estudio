#ejercicio prueba 3

import json
from datetime import datetime
archivo_datos = "registro datos"

def cargar_datos():
    try:
        with open(archivo_datos, "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []
def guardar_datos(datos):
    with open(archivo_datos, 'w') as archivo:
        json.dump(datos, archivo, indent=4)

def agregar_gasto():
    descripcion = input("Descripción del gasto: ")
    categoria = input("Categoría del gasto: ")
    fecha_str = input("Fecha del gasto (YYYY-MM-DD): ")
    monto = float(input("Monto del gasto: "))

    fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()

    nuevo_gasto = {
        'descripcion': descripcion,
        'categoria': categoria,
        'fecha': fecha_str,
        'monto': monto
    }

    datos = cargar_datos()
    datos.append(nuevo_gasto)
    guardar_datos(datos)
    print("Gasto registrado correctamente.")


def buscar_gastos():
    datos = cargar_datos()
    categoria_buscar = input("Ingrese la categoría a buscar (deje en blanco para ignorar): ").strip().lower()
    fecha_inicio_str = input("Ingrese la fecha de inicio (YYYY-MM-DD) para búsqueda (deje en blanco para ignorar): ").strip()
    fecha_fin_str = input("Ingrese la fecha de fin (YYYY-MM-DD) para búsqueda (deje en blanco para ignorar): ").strip()

    if fecha_inicio_str:
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
    else:
        fecha_inicio = None
    
    if fecha_fin_str:
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
    else:
        fecha_fin = None

    resultados = []
    for gasto in datos:
        fecha_gasto = datetime.strptime(gasto['fecha'], '%Y-%m-%d').date()

        if (not categoria_buscar or categoria_buscar == gasto['categoria'].lower()) and \
           (not fecha_inicio or fecha_inicio <= fecha_gasto) and \
           (not fecha_fin or fecha_gasto <= fecha_fin):
            resultados.append(gasto)

    if resultados:
        print("\nResultados de la búsqueda:")
        for gasto in resultados:
            print(f"Descripción: {gasto['descripcion']}, Categoría: {gasto['categoria']}, Fecha: {gasto['fecha']}, Monto: ${gasto['monto']}")
    else:
        print("No se encontraron gastos que coincidan con los criterios de búsqueda.")

# Función para calcular estadísticas de gastos
def calcular_estadisticas():
    datos = cargar_datos()

    total_gastos = sum(gasto['monto'] for gasto in datos)
    promedio_diario = total_gastos / len(set(gasto['fecha'] for gasto in datos))
    
    categorias = {}
    for gasto in datos:
        categoria = gasto['categoria']
        if categoria in categorias:
            categorias[categoria] += gasto['monto']
        else:
            categorias[categoria] = gasto['monto']
    
    categoria_max_gasto = max(categorias, key=categorias.get)

    print(f"\nTotal de gastos: ${total_gastos:.2f}")
    print(f"Promedio diario de gastos: ${promedio_diario:.2f}")
    print(f"Categoría con mayor gasto acumulado: {categoria_max_gasto} (${categorias[categoria_max_gasto]:.2f})")

def actualizar_gasto():
    datos = cargar_datos()
    if not datos:
        print("No hay gastos registrados para actualizar.")
        return
    
    print("Lista de gastos:")
    for i, gasto in enumerate(datos):
        print(f"{i+1}. Descripción: {gasto['descripcion']}, Categoría: {gasto['categoria']}, Fecha: {gasto['fecha']}, Monto: ${gasto['monto']}")
    
    indice_actualizar = int(input("Ingrese el número del gasto que desea actualizar: ")) - 1
    gasto_actualizado = datos.pop(indice_actualizar)

    print("\nIngrese los nuevos datos del gasto:")
    agregar_gasto()

    datos.append(gasto_actualizado)
    guardar_datos(datos)
    print("Gasto actualizado correctamente.")

def eliminar_gasto():
    datos = cargar_datos()
    if not datos:
        print("No hay gastos registrados para eliminar.")
        return
    
    print("Lista de gastos:")
    for i, gasto in enumerate(datos):
        print(f"{i+1}. Descripción: {gasto['descripcion']}, Categoría: {gasto['categoria']}, Fecha: {gasto['fecha']}, Monto: ${gasto['monto']}")
    
    indice_eliminar = int(input("Ingrese el número del gasto que desea eliminar: ")) - 1
    gasto_eliminado = datos.pop(indice_eliminar)

    guardar_datos(datos)
    print("Gasto eliminado correctamente.")

def main():
    while True:
        print("\nBienvenido al sistema de registro de gastos personales")
        print("1. Agregar un nuevo gasto")
        print("2. Buscar gastos por categoría o rango de fechas")
        print("3. Calcular estadísticas de gastos")
        print("4. Actualizar un gasto")
        print("5. Eliminar un gasto")
        print("6. Salir del programa")

        opcion = input("\nIngrese el número de la acción que desea realizar: ")

        if opcion == '1':
            agregar_gasto()
        elif opcion == '2':
            buscar_gastos()
        elif opcion == '3':
            calcular_estadisticas()
        elif opcion == '4':
            actualizar_gasto()
        elif opcion == '5':
            eliminar_gasto()
        elif opcion == '6':
            print("Gracias por usar el sistema de registro de gastos. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, ingrese un número del 1 al 6.")

if __name__ == "__main__":
    main()

