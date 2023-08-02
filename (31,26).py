#Program: Hamming coding (31,26) by Kovalev V.D. 5.107-2 ASU student
#Copyright 2023.
#Уравнения для нахождения проверочных битов основаны на формуле bM = 0, 
#где b - код с проверочными битами (неизвестными еще), M - проверочная матрица из 2-ных чисел от 1 до 31
#Уравнений всего 5 штук для данных кодов и они имеют вид:
#b1 = b3 + b5 + b7 + b9 + b11 + b13 + b15 + b17+ b19 + b21 + b23 + b25 + b27 + b29 + b31
#b2 = b3 + b6 + b7 + b10 + b11 + b14 + b15 + b18 + b19 + b22 + b23 + b26 + b27 + b30 + b31
#b4 = b5 + b6 + b7 + b12 + b13 + b14 + b15 + b20 + b21 + b22 + b23 + b28 + b29 + b30 + b31
#b8 = b9 + b10 + b11 + b12 + b13 + b14 + b15 + b24 + b25 + b26 + b27 + b28 + b29 + b30 + b31
#b16 = b17 + b18 + b19 + b20 + b21 + b22 + b23 + b24 + b25 + b26 + b27 + b28 + b29 + b20 + b31
#Для проверки на наличие ошибок используется формула (b + e)M = bM + eM = eM, где e - ошибка
#В месте, где присутствует ошибка, не будет выполняться условие bM = 0, соответственно код сделает следующее:
#1)Обнаружит
#2)Устранит

import numpy as np
from random import randint as rnd

def AppEND(text, matrix):
    print('Демонстрация кодов Хемминга (31,26)')
    print(f'Размер сообщения до кодирования: {len(text)} бит')
    text = list(text)
    for i in range(len(text)):
        if i == 0 or i == 1 or i == 3 or i == 7 or i == 15:
           text.insert(i, '0')
    text = np.array(text, dtype = 'int').T
    syndrome = np.remainder(np.dot(matrix, text), 2)
    for i in range(matrix.shape[0]):
        if syndrome[i] % 2 != 0:
            text[2**i - 1] ^= 1
        else:
            pass
    print('Код Хемминга: ', syndrome)
    print('Сообщение имеет вид: ', text)
    print(f'Размер сообщения с проверочными битами: {len(text)} бит')
    return text

def accept(text):
    wrong = [0,1,3,7,15]
    text = np.array2string(text)
    text = text.replace(' ', '')
    text = text.replace('[', '')
    text = text.replace(']', '')
    data = list(text)
    print(data)
    for i in sorted(wrong, reverse = True):
        del data[i]
    text = ''.join(data)
    print(f'Полученное сообщение: {text}')
    return text

def check(text, matrix):
    syndrome = np.remainder(np.dot(matrix, text), 2)
    if np.count_nonzero(syndrome) == 0:
        print('Errors not found')
        return text
    else:
        error_bit = np.sum(syndrome * 2 ** np.arange(syndrome.size))
        print(f'Ошибка в бите {error_bit}')
        text[error_bit - 1] ^= 1
        print(f'Исправленное сообщение: {text}')
        return text


if __name__ == "__main__":
    text = '10101101111000111001011010'

    M = np.array([[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
                [0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1],
                [0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1],
                [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]], 
                dtype = 'int')
    result = AppEND(text, M)
    test = accept(result)
    err = rnd(0,30)
    result[err] ^= 1
    print(f'Добавим ошибку в {err+1}-й бит: {result}')
    checking = check(result, M)






