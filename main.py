# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

import pruebe


def menu():

            calendario_completo, giras = pruebe.procesar_archivo_torneo('Pruebas/prueba1.txt')
            pruebe.imprimir_calendario_giras(calendario_completo, giras)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    menu()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
