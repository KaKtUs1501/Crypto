import math


# Функція для знаходження оберненого числа a^(-1) (mod m)
def mod_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None


# Функція для обчислення таблиці заміни
def generate_substitution_table(a, b, m=26):
    table = {}
    for x in range(m):
        encrypted_char = (a * x + b) % m
        table[chr(x + ord('A'))] = chr(encrypted_char + ord('A'))
    return table


# Функція шифрування
def affine_encrypt(text, a, b, m=26):
    if math.gcd(a, m) != 1:
        raise ValueError("a і m повинні бути взаємно простими числами!")

    encrypted_text = ""
    for char in text.upper():
        if char.isalpha():
            x = ord(char) - ord('A')
            encrypted_char = (a * x + b) % m
            encrypted_text += chr(encrypted_char + ord('A'))
        else:
            encrypted_text += char  # Залишаємо символи без змін
    return encrypted_text


# Функція дешифрування
def affine_decrypt(ciphertext, a, b, m=26):
    a_inv = mod_inverse(a, m)
    if a_inv is None:
        raise ValueError("Не існує оберненого для a мод m!")

    decrypted_text = ""
    for char in ciphertext.upper():
        if char.isalpha():
            y = ord(char) - ord('A')
            decrypted_char = (a_inv * (y - b)) % m
            decrypted_text += chr(decrypted_char + ord('A'))
        else:
            decrypted_text += char  # Залишаємо символи без змін
    return decrypted_text


# Зчитування тексту з файлу
def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


# Запис тексту у файл
def write_file(filename, text):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)


# Основний блок виконання
if __name__ == "__main__":
    input_filename = "input.txt"
    encrypted_filename = "encrypted.txt"
    decrypted_filename = "decrypted.txt"

    # Введення ключів
    a = int(input("Введіть значення a: "))
    b = int(input("Введіть значення b: "))

    # Генерація та виведення таблиці заміни
    substitution_table = generate_substitution_table(a, b)
    print("Таблиця заміни:")
    for k, v in substitution_table.items():
        print(f"{k} -> {v}")

    # Читаємо вхідний текст
    plaintext = read_file(input_filename)

    # Шифруємо текст
    encrypted_text = affine_encrypt(plaintext, a, b)
    write_file(encrypted_filename, encrypted_text)
    print(f"Зашифрований текст збережено у {encrypted_filename}")

    # Дешифруємо текст
    decrypted_text = affine_decrypt(encrypted_text, a, b)
    write_file(decrypted_filename, decrypted_text)
    print(f"Розшифрований текст: {decrypted_text}")
