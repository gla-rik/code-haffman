probabilities = []


def compute_code(probability):
    global final_code
    num = len(probability)  # количество уникальных символов
    huffman_code = [''] * num

    for i in range(num - 2):
        val = probability[num - i - 1] + probability[num - i - 2]

        """Если оба последних элемента не пустые"""
        if (huffman_code[-1] != '' and huffman_code[num - i - 2] != ''):
            huffman_code[-1] = ['0' + symbol for symbol in huffman_code[-1]]
            huffman_code[-2] = ['1' + symbol for symbol in huffman_code[-2]]
            """если только последний элемент НЕ пустой"""
        elif (huffman_code[-1] != ''):
            huffman_code[-2] = '1'
            huffman_code[-1] = ['0' + symbol for symbol in huffman_code[-1]]
            """если только ПРЕДпоследний элемент НЕ пустой"""
        elif (huffman_code[-2] != ''):
            huffman_code[-1] = '0'
            huffman_code[-2] = ['1' + symbol for symbol in huffman_code[-2]]
            """первый раз просто добавляем 1 и о соответсвенно вероятностям, или же
                последние два элемента пустые"""
        else:
            huffman_code[-1] = '0'
            huffman_code[-2] = '1'

        def position(value, index, probability):
            for j in range(len(probability)):
                if (value >= probability[j]):
                    return j
            return index - 1

        position = position(val, i, probability)  # ставляем новую вероятность в список

        probability = probability[0:(len(probability) - 2)]  # убираем два последних веса
        probability.insert(position, val)  # вместо них вставляем новый на свое место

        """проверка на то, являютёя ли элементы над которыми производились вычисления списком
            complete_code - уже готовые концы кодов"""

        if (isinstance(huffman_code[-2], list) and isinstance(huffman_code[-1], list)):
            """если последний и предпоследний списки"""
            complete_code = huffman_code[-1] + huffman_code[-2]
        elif (isinstance(huffman_code[-2], list)):
            """если предпоследний список"""
            complete_code = huffman_code[-2] + [huffman_code[-1]]
        elif (isinstance(huffman_code[-1], list)):
            """если последний список"""
            complete_code = huffman_code[-1] + [huffman_code[-2]]
        else:
            """если последний и предпослений не списки"""
            complete_code = [huffman_code[-2], huffman_code[-1]]
        """сокращаем список с кодами на два элемента"""
        huffman_code = huffman_code[0:(len(huffman_code) - 2)]
        """вставляем готовые коды на место новой вероятности"""
        huffman_code.insert(position, complete_code)

    huffman_code[0] = ['1' + symbol for symbol in huffman_code[0]]
    huffman_code[1] = ['0' + symbol for symbol in huffman_code[1]]


    if (len(huffman_code[1]) == 0):
        huffman_code[1] = '0'

    count = 0
    final_code = [''] * num

    for i in range(2):
        for j in range(len(huffman_code[i])):
            final_code[count] = huffman_code[i][j]
            count += 1

    final_code = sorted(final_code, key=len)


""" НАЧАЛО """
letter = input("Введите строку для вычисления кода Хаффмана: ")

quantity = {}
# находим количество каждой уникальной буквы
for char in letter:
    if char in quantity:
        quantity[char] += 1
    else:
        quantity[char] = 1


# сортируем от большего к меньшему
quantity = sorted(quantity.items(), key=lambda x: x[1], reverse=True)
# количество символов в сообщении
length = len(letter)

# из пары ключ:значение берем значение и находим вероятности
probabilities = [float("{:.2f}".format(frequency[1] / length)) for frequency in quantity]
# сортируем вероятности от большего к меньшему
probabilities = sorted(probabilities, reverse=True)

if len(quantity) == 2:
    final_code = ['0', '1']
elif len(quantity) == 1:
    final_code = ['0']
else:
    compute_code(probabilities)

code_letter = {}
for i in range(len(quantity)):
    print(quantity[i][0], "|", final_code[i])
    code_letter[quantity[i][0]] = final_code[i]

print("Готовый код: ", end='')
for i in letter:
    print(code_letter[i], end=" ")
