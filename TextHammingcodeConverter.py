import numpy as np
from random import randint as rnd

def chars_to_bin(text):
    binlist = []
    for symbol in text:
        codes = ord(symbol.encode('utf-8'))
        binary = bin(codes)[2:].zfill(26)
        binlist.append(binary)
    return binlist

def bin_to_chars(binlist):
    text = ''.join(binlist)
    ministr = bytes([int(text[i: i+26], 2) for i in range(0, len(text), 26)])
    result = ministr.decode('utf-8')
    return result

def AppEND(data, matrix):
    ministr = bytes([int(data[i: i+26], 2) for i in range(0, len(data), 26)])
    letter = ministr.decode('utf-8')
    text = list(data)
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
    with open('stats(31,26).txt', 'a') as file:
        file.write(f'Символ: "{letter}"\n'
                    f'Блок сообщения: {data}\n'
                    f'Размер блока сообщения до кодирования: {len(data)} бит\n'
                   f'Код Хемминга для данного блока: {syndrome}\n'
                   f'Сообщение имеет вид: {text}\n'
                   f'Размер сообщения с проверочными битами: {len(text)} бит\n'
                   '\n')
    return text

def check(text, matrix):
    with open('Errors(31,26).txt', 'a') as file:
        file.write(f'Полученное блок сообщения на проверку: {text}\n')
    syndrome = np.remainder(np.dot(matrix, text), 2)
    if np.count_nonzero(syndrome) == 0:
        return text
    else:
        error_bit = np.sum(syndrome * 2 ** np.arange(syndrome.size))
        text[error_bit - 1] ^= 1
        with open('Errors(31,26).txt', 'a') as file:
            file.write(f'Найдена ошибка в бите {error_bit}. Исправляем...\n'
                       f'Исправленное сообщение: {text}\n'
                       '\n')
        return text
    
def accept(text):
    wrong = [0,1,3,7,15]
    text = np.array2string(text)
    text = text.replace(' ', '')
    text = text.replace('[', '')
    text = text.replace(']', '')
    data = list(text)
    for i in sorted(wrong, reverse = True):
        del data[i]
    text = ''.join(data)
    return text

if __name__ == "__main__":

    binres = []

    M = np.array([[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
                [0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1],
                [0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1],
                [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]], 
                dtype = 'int')
    with open('text_26_kb.txt', encoding = 'utf-8') as file:
        data = file.read()
    bindata = chars_to_bin(data)
    for element in bindata:
        #Добавляем коды Хемминга
        message = AppEND(element, M)
        #Добавим ошибку
        err = rnd(0,30)
        message[err] ^= 1

        checking = check(message, M)

        ending = accept(checking)
        binres.append(ending)

        result = bin_to_chars(binres)
    
    with open('result(31,26).txt', 'w') as file:
        file.write(result)


