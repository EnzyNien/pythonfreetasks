def main():

    m = int(input('size of the square matrix: '))

    # создаем пустую матрицу
    matrix = [[0 for i in range(m)] for j in range(m)]

    side = m
    offset = 0

    k = 1
    while True:
        # верхняя граница
        for i in range(side):
            matrix[offset][offset + i] = k
            k += 1
        if k > m*m:
            break

        # правая граница
        for i in range(side - 2):
            matrix[1 + offset + i][side - (1 - offset)] = k
            k += 1

        # нижняя граница
        for i in range(side):
            matrix[side - (1 - offset)][side - i -
                                        (1 - offset)] = k
            k += 1

        # левая граница
        for i in range(side - 2):
            matrix[side - i - (2 - offset)][offset] = k
            k += 1

        # уменьшение текущей стороны после прохода
        side -= 2
        # увеличение отсутпа
        offset += 1

    [print(*row) for row in matrix]


if __name__ == '__main__':
    main()
