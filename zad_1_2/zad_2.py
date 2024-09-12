files = ['A.txt', 'B.txt']

def max_mul(file_with_data):
    with open(file_with_data, "r") as file:
        data = file.read()
        data = data.split("\n")
        data = data[:(int(data[0])+1)]   # "срез" числа эелементов и лишних пробелов 
    len_of_data = int(data[0])
    data = data[1:]                      # убираем цифру отвечающую за число элементов
    data = list(map(int, data))          # делаем массив целочисленным
    #print(f"{len_of_data} - {data}")

    # идея следующая - пройтись по всему массиву 
    # и для каждого элемента найти максимальный элемент, 
    # отстающий от текущего влево на >= 8позиций. 
    # Перемножить текущий элемент с найденным максимальным и пойти дальше, запомнив значение. 
    # Итого: алгоритм должен работаь за линейное время (ну почти :) )

    max_mul_value = 0
    max_prefix = [0] * len_of_data #для текущего элемента
    for i in range(8, len_of_data):
         # Обновляем максимальный префикс на расстоянии min_distance от текущего элемента
        max_prefix[i] = max(max_prefix[i - 1], data[i - 8])
         # Проверяем произведение текущего элемента и максимального префикса
        max_mul_value = max(max_mul_value, data[i] * max_prefix[i])

    return max_mul_value

for file in files:
    print(max_mul(file))