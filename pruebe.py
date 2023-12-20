def invertir_localia(jornada):
    return [-equipo for equipo in jornada]
def generar_calendario(n):
    if n % 2 != 0:
        raise ValueError("El número de equipos debe ser par")

    calendario = []

    for fecha in range(1, n):
        jornada = []
        for i in range(n // 2):
            local = (fecha + i) % n
            visitante = (fecha - i - 1 + n) % n
            if i == 0:
                visitante = n - 1

            # Representar al equipo local como positivo y al visitante como negativo
            jornada.append(local + 1)  # +1 para cambiar de índice base 0 a base 1
            jornada.append(-(visitante + 1))  # +1 para cambiar de índice base 0 a base 1
        calendario.append(jornada)

    # Segunda mitad del calendario con localías invertidas
    calendario_completo = calendario + [invertir_localia(jornada) for jornada in calendario]

    return calendario_completo



def calcular_giras(calendario, matriz_distancias):
    n = len(matriz_distancias)
    giras = {equipo: {'giras': [], 'costo_total': 0} for equipo in range(n)}

    for equipo in range(n):
        gira_actual = []
        costo_gira_actual = 0
        equipo_actual = equipo + 1  # +1 para cambiar de índice base 0 a base 1

        for jornada in calendario:
            if -equipo_actual in jornada:
                local_index = jornada.index(-equipo_actual)
                local_equipo = abs(jornada[local_index]) - 1  # Convertir a índice base 0
                if not gira_actual:
                    gira_actual.append(local_equipo)
                else:
                    # Sumar el costo de viajar desde el último equipo de la gira hasta el actual
                    ultimo_equipo = gira_actual[-1]
                    costo_gira_actual += matriz_distancias[ultimo_equipo][local_equipo]
                    gira_actual.append(local_equipo)

        # Verificar si la última secuencia es una gira
        if len(gira_actual) > 1:
            giras[equipo]['giras'].append(gira_actual)
            giras[equipo]['costo_total'] += costo_gira_actual

    return giras

def procesar_archivo_torneo(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        lineas = archivo.readlines()

    n = int(lineas[0].strip())
    distancias = [list(map(int, linea.strip().split())) for linea in lineas[1:]]

    calendario = generar_calendario(n)
    giras = calcular_giras(calendario, distancias)

    return calendario, giras

def imprimir_calendario_giras(calendario, giras):
    print("Calendario de Partidos:")
    for partidos in (calendario):
        print(f"{partidos}")

    print("\nGiras y Costos:")
    for equipo, info in giras.items():
        print(f" {equipo + 1}: Giras: {info['giras']}, Costo Total: {info['costo_total']}")


calendario_completo, giras = procesar_archivo_torneo('Pruebas/prueba1.txt')
imprimir_calendario_giras(calendario_completo, giras)