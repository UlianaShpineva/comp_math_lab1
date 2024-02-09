def read_data():
    size = 0
    accuracy = 0
    dat = []
    matrix = []
    b = []
    inp_type = input("Выберете способ ввода данных (f/c): ")
    if inp_type == "f":
        filename = input("Введите имя файла: ")
        with open(filename, "r") as f:
            accuracy = float(f.readline())
            size = int(f.readline())
            for i in range(size):
                matrix.append(list(map(float, f.readline().split(" "))))
    elif inp_type == "c":
        accuracy = float(input("Введите точность: "))
        size = int(input("Введите размерность: "))
        print("Введите матрицу:")
        for i in range(size):
            matrix.append(list(map(float, input().split())))
    else:
        print("Некорректный ввод")
        read_data()

    for i in range(size):
        b.append(matrix[i].pop())

    dat.append(accuracy)
    dat.append(size)
    dat.append(matrix)
    dat.append(b)
    return dat


class Solver:
    def __init__(self, accuracy, size, matrix, b):
        self.accuracy = accuracy
        self.size = size
        self.matrix = matrix
        self.b = b

    M: int = 100

    def is_diag(self) -> bool:
        flag = False
        for i in range(self.size):
            if sum(map(abs, self.matrix[i])) - 2 * abs(self.matrix[i][i]) < 0:
                flag = True
            elif sum(map(abs, self.matrix[i])) - 2 * abs(self.matrix[i][i]) > 0:
                return False
        return flag

    def to_diag(self) -> None:
        for i in range(self.size):
            max_in_line = max(map(abs, self.matrix[i][i:]))
            max_in_column = max(map(abs, self.get_column(i)[i:]))
            if max_in_column >= max_in_line:
                line = self.get_column(i)[i:].index(max_in_line) + i
                self.matrix[i], self.matrix[line] = self.matrix[line], self.matrix[i]
                self.b[i], self.b[line] = self.b[line], self.b[i]
            else:
                column = self.matrix[i].index(max_in_column)
                tmp_column = self.get_column(column)
                self.set_column(column, self.get_column(i))
                self.set_column(i, tmp_column)

    def get_column(self, i: int) -> list[float]:
        return [line[i] for line in self.matrix]

    def set_column(self, i: int, column: list[float]):
        for j in range(self.size):
            self.matrix[j][i] = column[j]

    def print(self):
        for i, row in enumerate(self.matrix):
            for element in row:
                print("{:8}".format(element), end='')
            print(" | ", end='')
            print("{:8}".format(self.b[i]))
        print()

    def solve(self) -> (list[float], int, list[float]):
        d = [num / self.matrix[i][i] for i, num in enumerate(self.b)]
        x = d.copy()
        cnt = 0

        while True:
            cnt += 1
            if cnt >= self.M:
                print("Превышено максимальное количество итераций")
                break

            x_new = x.copy()
            for i in range(self.size):
                s1 = sum(self.matrix[i][j] * x_new[j] for j in range(i))
                s2 = sum(self.matrix[i][j] * x[j] for j in range(i + 1, self.size))
                x_new[i] = (self.b[i] - s1 - s2) / self.matrix[i][i]

            if all(abs(x_new[i] - x[i]) <= self.accuracy for i in range(self.size)):
                return x_new, cnt, list(abs(x_new[i] - x[i]) for i in range(self.size))

            x = x_new


if __name__ == '__main__':
    data = read_data()
    solver = Solver(data[0], data[1], data[2], data[3])
    print("Получена матрица:")
    solver.print()
    if not solver.is_diag():
        solver.to_diag()
        print("Приведение к матрице диагонального преобладания:")
        solver.print()
        if not solver.is_diag():
            print("Приведение к матрице диагонального преобладания невозможно")
            exit()
    x_res, cnt_res, accuracy_vect = solver.solve()
    print("Вектор неизвестных:")
    print(x_res, "\n")
    print("Количество итераций: ", cnt_res, "\n")
    print("Вектор погрешностей:")
    print(accuracy_vect)
