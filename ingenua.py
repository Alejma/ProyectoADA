import tkinter as tk
from tkinter import filedialog

import tkinter as tk
from tkinter import filedialog
"""
@author: Alejandro Marin Hoyos
@author: Cristian David Zuñiga
@date: 19-12-2023
"""

def seleccionar_y_leer_archivo():
    """
    Abre una interfaz gráfica para que el usuario seleccione un archivo de texto.

    Args:
        none

    return:
        string: Ruta del archivo seleccionado
    """
    # Inicializar la interfaz gráfica de Tkinter
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter

    # Abrir el diálogo de selección de archivos y obtener la ruta del archivo
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

    print(ruta_archivo)
    return ruta_archivo

def get_input(filename):
    """
    Lee y procesa el archivo especificado, extrayendo datos
    como el número de equipos y la matriz de costos de viaje.

    Args:
        string: La ruta del archivo a leer.

    return:
        int: Número de equipos.
        list(list(int)) :  Matriz de costos de viaje entre equipos.
    """
    cost = []
    try:
        with open(filename, 'r') as f:
            N = [int(x) for x in f.readline().split()][0]
            for i in range(N):
                a = [int(x) for x in f.readline().split()]
                cost.append(a)
        return N, cost
    except FileNotFoundError:
        print("Archivo no encontrado.")
        return None, None
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return None, None

# Ejemplo de uso
ruta_archivo = seleccionar_y_leer_archivo()
if ruta_archivo:
    N, cost_matrix = get_input(ruta_archivo)
    if N is not None:
        print("Número de equipos:", N)
        print("Matriz de costos:", cost_matrix)

count = 0
played = [False] * (N)
current_pos = [x for x in range(N)]
pre_pos = [x for x in range(N)]
travel = [0 for _ in range(N)]
remainning_matches = []
Team = [x for x in range(N)]

for i in range(N):
    tmp = [i] * (N - 2)
    for j in range(N):
        tmp.append(j)
    remainning_matches.append(tmp)


# -------------------------------------------- one-week ----------------------------------------------------#


def check(rs, temp):
    for i in rs:
        if temp == i[0]:
            return False
    return True


def backtrack(n, remainning_matches, rs=[], tmp=set()):
    """
    Extiende la lógica de backtracking para encontrar la combinación
    óptima de partidos para todas las semanas de la liga.

    Args:
        int:  Número total de equipos..
        list(list()): Lista de partidos pendientes.
        list: Resultados acumulados (inicialmente vacío).
        set(): Conjunto temporal para almacenar combinaciones de partidos (inicialmente vacío).

    return:
        list: Lista de combinaciones óptimas de partidos para todas las semanas.
    """
    if n == 0:
        temp = sorted(list(tmp), key=lambda x: x[0])
        if check(rs, temp):
            rs.append((temp, sum(travel)))

    else:
        for team in Team:
            # Verifica si el equipo aún no ha jugado en esta iteración
            if played[team] == False and team in remainning_matches[team]:
                played[team] = True # Marca el equipo como jugado
                n -= 2 # Reduce el contador de partidos por asignar
                for enemy in Team:
                    # Continúa si el equipo enemigo es diferente y aún no ha jugado
                    if enemy != team and team in remainning_matches[enemy] and played[enemy] == False:
                        played[enemy] = True

                        travel[enemy] += cost_matrix[current_pos[enemy]][team]
                        travel[team] += cost_matrix[current_pos[team]][team]

                        remainning_matches[team].remove(team)
                        remainning_matches[enemy].remove(team)

                        pre_pos[team] = current_pos[team]
                        pre_pos[enemy] = current_pos[enemy]

                        current_pos[team] = team
                        current_pos[enemy] = team

                        tmp.add((team, enemy))
                        backtrack(n, remainning_matches, rs, tmp)

                        tmp.discard((team, enemy))
                        played[enemy] = False

                        remainning_matches[enemy].append(team)
                        remainning_matches[team].append(team)

                        current_pos[enemy] = pre_pos[enemy]
                        current_pos[team] = pre_pos[team]

                        travel[team] -= cost_matrix[current_pos[team]][team]
                        travel[enemy] -= cost_matrix[current_pos[enemy]][team]

                n += 2
                played[team] = False
    return rs


# ------------------------------------------------- all-week-----------------------------------------------#

def find_sum():
    pass


f_opt = float('inf')
solution = None
f_recent = 0
m = 0


def find_all(N, k=0, res=[], tmp=[]):
    """
    Extiende la lógica de backtracking para encontrar la combinación
    óptima de partidos para todas las semanas de la liga.

    Args:
        int: Número total de equipos.
        int: Contador de semanas (inicialmente 0).
        list(): Resultados acumulados para todas las semanas (inicialmente vacío).
        list(): Lista temporal para almacenar combinaciones de partidos (inicialmente vacía).

    return:
        list(): Lista de combinaciones óptimas de partidos para todas las semanas.
        float: Costo total mínimo de viaje.
    """
    global f_opt, solution, f_recent, m
    m += 1
    if k == 2 * N - 2:
        if f_recent < f_opt:
            f_opt = f_recent
            solution = list(res)

    else:
        k += 1
        rs = backtrack(N, remainning_matches, rs=list())
        for week in rs:
            matches, travel = week
            f_recent += travel
            res.append(matches)
            for match in matches:
                host, enemy = match

                pre_pos[host] = current_pos[host]
                pre_pos[enemy] = current_pos[enemy]

                current_pos[host] = host
                current_pos[enemy] = host

                remainning_matches[host].remove(host)
                remainning_matches[enemy].remove(host)

            find_all(N, k)

            res.pop(-1)
            f_recent -= travel
            for match in matches:
                host, enemy = match

                current_pos[host] = pre_pos[host]
                current_pos[enemy] = pre_pos[enemy]

                remainning_matches[host].append(host)
                remainning_matches[enemy].append(host)
        k -= 1
    return solution, f_opt


def build_match_matrix(league, N):
    """
    Construye una matriz representando los partidos de la liga, mostrando
    qué equipo juega en casa y cuál es el visitante en cada partido.

    Args:
        list(list([][])): Lista de partidos por semana.
        int: Número total de equipos.

    return:
        list(list()): Matriz con la información de los partidos.
    """
    # Inicializar la matriz de enfrentamientos con ceros
    match_matrix = [[0 for _ in range(N)] for _ in range(len(league))]

    for week_index, week_matches in enumerate(league):
        for match in week_matches:
            host, enemy = match
            # Asignar el equipo local en su columna con el número del equipo visitante (positivo)
            match_matrix[week_index][host] = enemy + 1
            # Asignar el equipo visitante en su columna con el número del equipo local (negativo)
            match_matrix[week_index][enemy] = -(host + 1)

    return match_matrix


# Después de calcular la liga con 'find_all(N)'
#league, cost = find_all(N)
# print(solution)
#match_matrix = build_match_matrix(league, N)

# Imprimir la matriz de enfrentamientos










