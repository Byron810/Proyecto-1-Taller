import os
import tkinter as tk
import random



# Modo creación de crucigramas
def modo_creacion():
    """
    Función que inicia el modo de creación de crucigramas 3D.
    Permite al usuario definir dimensiones y añadir palabras.
    """
    while True:
        print("Dimensiones:\n1 - 6x6x6 \n2 - 7x7x7 \n3 - 8x8x8")
        cuadricula = input("Ingrese las dimensiones de la cuadricula: ")
        
        
        if cuadricula == "1":
            cuadricula = 6
            break
        elif cuadricula == "2":
            cuadricula = 7
            break
        elif cuadricula == "3":
            cuadricula = 8
            break
        else:
            print("Opción no válida. Intente de nuevo.")

           
   
def agregar_palabra(palabras, descripcion):
    palabra = input("Ingresa una palabra: ").upper()
    descripcion = input(f"Ingresa una pequeña descripción para '{palabra}': ")
    palabras.append((palabra, descripcion))

def buscar_letra_comun(palabra1, palabra2):
    for i, letra1 in enumerate(palabra1):
        for j, letra2 in enumerate(palabra2):
            if letra1 == letra2:
                return i, j  # Retorna las posiciones donde las letras coinciden
    return None

def colocar_primera_palabra(grid, palabra):
    fila_inicio = len(grid) // 2
    col_inicio = len(grid[0]) // 2
    for i, letra in enumerate(palabra):
        grid[fila_inicio][col_inicio + i] = letra

def verificar_colocacion(grid, fila, col, palabra, direccion):
    """Verifica si se puede colocar la palabra en la dirección dada sin superponer mal las letras"""
    if direccion == 'horizontal':
        if col + len(palabra) > len(grid[0]):  # Se sale de la cuadrícula
            return False
        return all(grid[fila][col + i] in [' ', palabra[i]] for i in range(len(palabra)))
    elif direccion == 'vertical':
        if fila + len(palabra) > len(grid):  # Se sale de la cuadrícula
            return False
        return all(grid[fila + i][col] in [' ', palabra[i]] for i in range(len(palabra)))

def colocar_palabra_conexion(grid, palabra, fila, col, indice_palabra, indice_existente, direccion):
    if direccion == 'vertical':
        # La palabra nueva será colocada verticalmente
        fila -= indice_palabra
        if verificar_colocacion(grid, fila, col, palabra, direccion):
            for i, letra in enumerate(palabra):
                grid[fila + i][col] = letra
            return True
    elif direccion == 'horizontal':
        # La palabra nueva será colocada horizontalmente
        col -= indice_palabra
        if verificar_colocacion(grid, fila, col, palabra, direccion):
            for i, letra in enumerate(palabra):
                grid[fila][col + i] = letra
            return True
    return False

def mostrar_crucigrama(palabras):
    print("\nCrucigrama generado:\n")
    grid_size = 15  # Tamaño fijo de la cuadrícula para simplificar
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]

    # Colocar la primera palabra en el centro
    primera_palabra = palabras[0][0]
    colocar_primera_palabra(grid, primera_palabra)

    # Colocar las palabras restantes
    for palabra, descripcion in palabras[1:]:
        palabra_colocada = False
        for fila in range(grid_size):
            for col in range(grid_size):
                if grid[fila][col] in palabra:
                    indice_palabra = palabra.find(grid[fila][col])
                    # Probar colocar horizontal o vertical
                    if colocar_palabra_conexion(grid, palabra, fila, col, indice_palabra, None, 'vertical') or \
                       colocar_palabra_conexion(grid, palabra, fila, col, indice_palabra, None, 'horizontal'):
                        palabra_colocada = True
                        break
            if palabra_colocada:
                break

    for fila in grid:
        print(' '.join(fila))

def mostrar_pistas(palabras):
    print("\nPistas:")
    for i, (_, descripcion) in enumerate(palabras, 1):
        print(f"{i}. {descripcion}")

def main():
    palabras = []

    while True:
        agregar_palabra(palabras, None)
        
        continuar = input("¿Quieres agregar otra palabra? (s/n): ").lower()
        if continuar != 's':
            break

    mostrar_crucigrama(palabras)
    mostrar_pistas(palabras)

if __name__ == "__main__":
    main()