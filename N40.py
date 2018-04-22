def main():

    def print_row(line):
        print(' '.join(line))

    m = int(input('size of the square matrix: '))

    # создаем пустую матрицу
    matrix = [['0' for i in range(m)] for j in range(m)]

    side = m

    offset = 0
    digit = 1

    while offset < m / 2:
        # верхняя граница
        for i in range(side):
            matrix[offset][offset + i] = str(digit)
            digit += 1

        # правая граница
        for i in range(side - 2):
            matrix[1 + offset + i][side - (1 - offset)] = str(digit)
            digit += 1

        # нижняя граница
        if (side / 2 - offset) >= 0:
            for i in range(side):
                matrix[side - (1 - offset)][side - i -
                                            (1 - offset)] = str(digit)
                digit += 1

        # левая граница
        for i in range(side - 2):
            matrix[side - i - (2 - offset)][offset] = str(digit)
            digit += 1

        # уменьшение текущей стороны после прохода
        side -= 2
        # увеличение отсутпа
        offset += 1

    [print_row(row) for row in matrix]


if __name__ == '__main__':
    main()
