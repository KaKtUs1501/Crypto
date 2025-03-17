import numpy as np

table = {
    'А': 0, 'Б': 1, 'В': 2, 'Г': 3, 'Д': 4, 'Е': 5, 'Ж': 6, 'З': 7, 'И': 8, 'Й': 9, 'К': 10, 'Л': 11, 'М': 12, 'Н': 13,
    'О': 14, 'П': 15, 'Р': 16, 'С': 17,
    'Т': 18, 'У': 19, 'Ф': 20, 'Х': 21, 'Ц': 22, 'Ч': 23, 'Ш': 24, 'Щ': 25, 'Ъ': 26, 'Ы': 27, 'Ь': 28, 'Э': 29, 'Ю': 30,
    'Я': 31
}
inverse_table = {v: k for k, v in table.items()}


def generate_gamma(length, key):
    gamma = [key[0], key[1], key[2]]
    for t in range(3, length + 1):
        gamma.append((gamma[t - 1] + gamma[t - 3]) % 32)
    result_gamma = [(gamma[t] + gamma[t + 1]) % 32 for t in range(length)]
    print("Згенерована гамма:", result_gamma)
    return result_gamma


def encrypt(text, key):
    text_numbers = [table[char] for char in text if char in table]
    gamma = generate_gamma(len(text_numbers), key)
    encrypted_numbers = [(text_numbers[i] + gamma[i]) % 32 for i in range(len(text_numbers))]
    encrypted_text = ''.join(inverse_table[num] for num in encrypted_numbers)
    return encrypted_numbers, encrypted_text


def decrypt(encrypted_numbers, key):
    gamma = generate_gamma(len(encrypted_numbers), key)
    decrypted_numbers = [(encrypted_numbers[i] + (32 - gamma[i])) % 32 for i in range(len(encrypted_numbers))]
    decrypted_text = ''.join(inverse_table[num] for num in decrypted_numbers)
    return decrypted_text


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().strip()


def write_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


def main():
    while True:
        choice = input("Шифрування (E), Розшифрування (D) або Вихід (Q): ").strip().upper()
        if choice == 'Q':
            print("Програма завершена.")
            break
        key = list(map(int, input("Введіть 3 числа ключа через пробіл: ").split()))

        if choice == 'E':
            plaintext = read_file('plaintext.txt').upper()
            encrypted_numbers, encrypted_text = encrypt(plaintext, key)
            encrypted_str = ' '.join(map(str, encrypted_numbers))
            write_file('encrypted.txt', encrypted_str)
            print("Зашифроване повідомлення записано у encrypted.txt")
            print("Зашифроване повідомлення:", encrypted_text)
        elif choice == 'D':
            encrypted_numbers = list(map(int, read_file('encrypted.txt').split()))
            decrypted_text = decrypt(encrypted_numbers, key)
            write_file('decrypted.txt', decrypted_text)
            print("Розшифроване повідомлення:", decrypted_text)
        else:
            print("Невідомий вибір. Будь ласка, виберіть E, D або Q.")


if __name__ == "__main__":
    main()
