import collections
import string

# Додаємо підтримку кирилиці
ukrainian_alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
full_alphabet = ukrainian_alphabet + string.ascii_lowercase


def caesar_cipher(text, shift):
    shifted_alphabet = full_alphabet[shift:] + full_alphabet[:shift]
    table = str.maketrans(full_alphabet + full_alphabet.upper(), shifted_alphabet + shifted_alphabet.upper())
    return text.translate(table)


def caesar_decipher(text, shift):
    return caesar_cipher(text, -shift)


def frequency_analysis(text):
    text = text.lower()
    letter_counts = collections.Counter(c for c in text if c in full_alphabet)
    total_letters = sum(letter_counts.values())
    frequencies = {letter: count / total_letters for letter, count in
                   letter_counts.items()} if total_letters > 0 else {}
    return frequencies


def break_caesar_cipher(text):
    frequencies = frequency_analysis(text)
    print("Частоти літер у зашифрованому тексті:")
    for char, freq in sorted(frequencies.items(), key=lambda x: x[1], reverse=True):
        print(f"{char}: {freq:.4f}")
    if not frequencies:
        return 0  # Якщо не знайдено літер

    most_common_letter = max(frequencies, key=frequencies.get)

    # Визначаємо алфавіт, у якому знаходиться символ
    if most_common_letter in ukrainian_alphabet:
        alphabet = ukrainian_alphabet
        most_common_in_language = 'о'  # Найпоширеніша літера в українській мові
    elif most_common_letter in string.ascii_lowercase:
        alphabet = string.ascii_lowercase
        most_common_in_language = 'e'  # Найпоширеніша літера в англійській мові
    else:
        return 0  # Якщо символ не знайдено в алфавіті

    # Коригуємо обчислення зміщення
    shift = (alphabet.index(most_common_letter) - alphabet.index(most_common_in_language)) % len(alphabet)
    return shift



def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


def write_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


if __name__ == "__main__":
    input_filename = "input.txt"
    encrypted_filename = "encrypted.txt"
    decrypted_filename = "decrypted.txt"

    shift = int(input("Введіть зміщення для шифру Цезаря: "))
    text = read_file(input_filename)

    encrypted_text = caesar_cipher(text, shift)
    write_file(encrypted_filename, encrypted_text)
    print("Текст зашифровано та збережено у", encrypted_filename)

    decrypted_text = caesar_decipher(encrypted_text, shift)
    write_file(decrypted_filename, decrypted_text)
    print("Текст розшифровано та збережено у", decrypted_filename)

    guessed_shift = break_caesar_cipher(encrypted_text)
    print("Ймовірне зміщення, знайдене методом частотного аналізу:", guessed_shift)

    cracked_text = caesar_decipher(encrypted_text, guessed_shift)
    print("Розшифрований текст:")
    print(cracked_text)
