import random
# for pretty visualization of the field
# pip install tabulate
from tabulate import tabulate

"""
В темній кімнаті розміром  n x n клітинок знаходяться механічний кіт і певна кількість випадково розташованих нерухомих коробок.
Напишіть програму, що дозволить коту знайти і залізти в кожну з коробок, бажано за меншу кількість ходів.
Умови наступні:
1. Кіт і коробка займають одну клітинку в кімнаті
2. Кіт бачить не більш ніж на 3 клітинки навколо себе.
3. Кіт може переміщуватись по кімнаті на 1 клітинку за хід у любому напрямку включно с діагональним
4. Кіт починає пошук з довільної клітинки в кімнаті.
"""


TABLE = 'simple'
# TABLE = 'simple_grid'


class BoxFinder:
    """
    Для вывода следующего шага - ввести в консоли любой символ или нажать Enter
    Сложность алгоритма, полагаю, O(n^2) от начальной точки не зависит.
    """
    def __init__(self, n=15, view=3):

        self.n = n
        self.room = []

        self.view = view
        self.empty = ' '
        self.box = 'B'
        self.cat = 'C'
        self.explored_fields = '.'
        self.track = '+'

        self.found_box_coord = []
        self.direction_coord = []

        # generate room(NxN) with random location of boxes and cat
        for i in range(self.n):
            row = []
            for j in range(self.n):
                row.append(self.empty)
            self.room.append(row)

        if self.n % 2 == 0:
            m = self.n
        else:
            m = self.n + 1

        m += 1
        m += random.randint(1, 2)

        for i in range(m):
            x = random.randint(0, self.n - 1)
            y = random.randint(0, self.n - 1)
            self.room[x][y] = self.box
            if i == range(m)[-1]:
                self.room[x][y] = self.cat
                self.cat_coord = [x, y]

    def frame(self):
        """Если кот не видит ящиков он будет двигаться в сторону неисследованной территории.
        Если неисследованной территории больше нет программа останавливается"""
        self.discover_fields()
        if self.found_box_coord == []:
            undiscovered = self.find_undiscovered_fields()
            if undiscovered == []:
                BoxFinder.visualization(self.room)
                print("Don't have any steps!")
                return True
            self.direction_coord = self.find_nearest_coordinate(self.cat_coord, undiscovered)
        else:
            self.direction_coord = self.find_nearest_coordinate(self.cat_coord, self.found_box_coord)
        BoxFinder.visualization(self.room)
        return False

    def processing(self):
        self.frame()
        while True:
            self.make_step(self.define_next_step(self.direction_coord))
            stop = self.frame()
            if stop:
                break

    def find_undiscovered_fields(self):
        undiscovered = []
        for i in range(self.n):
            for j in range(self.n):
                if self.room[i][j] == self.empty:
                    undiscovered.append([i, j])
        return undiscovered

    @staticmethod
    def visualization(room):
        print(tabulate(room, tablefmt=TABLE))
        input()

    def discover_fields(self):
        """Отмечаю ячейки, которые видит кот и запоминаю расположение коробок в рамках поля"""
        for i in range(self.cat_coord[0] - self.view, self.cat_coord[0] + self.view + 1):
            if i < 0 or i >= self.n:
                continue
            for j in range(self.cat_coord[1] - self.view, self.cat_coord[1] + self.view + 1):
                if j < 0 or j >= self.n:
                    continue
                if self.room[i][j] == self.empty:
                    self.room[i][j] = self.explored_fields
                if self.room[i][j] == self.box:
                    coord = [i, j]
                    # avoid duplicates
                    if coord not in self.found_box_coord:
                        self.found_box_coord.append(coord)

    @staticmethod
    def find_nearest_coordinate(start_coord, list_destination_coordinates):
        """
        Здесь нахожу ближайшую координату из списка list_destination_coordinates по отношению к стартовой.
        Из-за того, что Кот может передвигаться диагонально - дистанция перемещения определяется только
        большей стороной условного треугольника
        """
        distance = []
        for l_b in list_destination_coordinates:
            distance_x = abs(start_coord[0] - l_b[0])
            distance_y = abs(start_coord[1] - l_b[1])
            if distance_y > distance_x:
                distance.append(distance_y)
            else:
                distance.append(distance_x)

        list_destination_coordinates = [x for _, x in sorted(zip(distance, list_destination_coordinates))]

        return list_destination_coordinates[0]

    def define_next_step(self, target_coord):
        """Определяю минимальное расстояние к целевой координате от 8-ми возможных ходов кота"""
        list_of_possible_steps = self.define_possible_steps()
        next_step = self.find_nearest_coordinate(target_coord, list_of_possible_steps)
        return next_step

    def define_possible_steps(self):
        list_of_possible_steps = []
        for i in range(self.cat_coord[0] - 1, self.cat_coord[0] + 2):
            if i < 0 or i >= self.n:
                continue
            for j in range(self.cat_coord[1] - 1, self.cat_coord[1] + 2):
                if j < 0 or j >= self.n:
                    continue
                if self.room[i][j] != self.cat:
                    list_of_possible_steps.append([i, j])
        return list_of_possible_steps

    def make_step(self, next_step):
        self.room[next_step[0]][next_step[1]] = self.cat
        self.room[self.cat_coord[0]][self.cat_coord[1]] = self.track
        self.cat_coord = next_step
        # delete founded box
        self.found_box_coord = [x for x in self.found_box_coord if x != self.cat_coord]


if __name__ == '__main__':
    test = BoxFinder()
    test.processing()
