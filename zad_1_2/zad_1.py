def count_odd_non_decreasing_numbers():
    count = 0
    # 99 < ... < 10000
    for num in range(100, 10000):
        if num % 2 == 1:  # Проверяем, что число нечётное
            octal_str = oct(num)[2:]  # Получаем восьмеричное представление числа
            if is_non_decreasing(octal_str):  
                #print(f"{num} - {octal_str}")
                count += 1
    return count

# Проверка, что цифры числа в восьмеричной системе идут в неубывающем порядкe
def is_non_decreasing(octal_str):    
    for i in range(len(octal_str)-1):
        if octal_str[i] > octal_str[i+1]:
            return 0
    return 1


result = count_odd_non_decreasing_numbers()
print(f"Ответ: {result}")
