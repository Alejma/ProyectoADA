import ingenua
def menu():

    # Después de calcular la liga con 'find_all(N)'
    league, cost = ingenua.find_all(ingenua.N)
    # print(solution)
    match_matrix = ingenua.build_match_matrix(league, ingenua.N)

    # Imprimir la matriz de enfrentamientos

    for week in match_matrix:
        print(week)
    print(f'El costo total es de: {cost} \ncon la solución ingenua')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    menu()

