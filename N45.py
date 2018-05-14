
def m_create():
    while True:
        try:
            x = int(input('input x: '))
            y = int(input('input y: '))
        except BaseException:
            print('values input error. please try again')
        else:
            break

    while True:
        matrix = []
        try:
            for i in range(y):
                row = []
                for j in range(x):
                    row.append(float(input(f'input ({j},{i}): ')))
                matrix.append(row)
        except BaseException:
            print('values input error. please try again')
        else:
            break
    return matrix


def m_add(m1, m2):
    result = []
    if len(m1) != len(m2):
        print('matrices are not equal')
        return None
    for idx, row in enumerate(m1):
        add_row = []
        len_row = len(row)
        if len_row == len(m2[idx]):
            add_row = [row[i] + m2[idx][i] for i in range(len_row)]
        else:
            print('matrices are not equal')
            return None
        result.append(add_row)
    return result


def m_sub(m1, m2):
    result = []
    if len(m1) != len(m2):
        print('matrices are not equal')
        return None
    for idx, row in enumerate(m1):
        add_row = []
        len_row = len(row)
        if len_row == len(m2[idx]):
            add_row = [row[i] - m2[idx][i] for i in range(len_row)]
        else:
            print('matrices are not equal')
            return None
        result.append(add_row)
    return result


def m_mul(m1, m2):
    result = []
    if len(m1) != len(m2):
        print('matrices are not equal')
        return None
    for idx, row in enumerate(m1):
        add_row = []
        len_row = len(row)
        if len_row == len(m2[idx]):
            add_row = [row[i] * m2[idx][i] for i in range(len_row)]
        else:
            print('matrices are not equal')
            return None
        result.append(add_row)
    return result


if __name__ == '__main__':
    pass
    #m1 = m_create()
    #m2 = m_create()
    #result_add = m_add(m1,m2)
    # print(result_add)

    #result_sub = m_sub(m2,m1)
    # print(result_sub)

    #result_mul = m_mul(m2,m1)
    # print(result_mul)