import itertools

def permute(bits, perm):
    return [bits[i - 1] for i in perm]

def shift_left(bits, shifts):
    return bits[shifts:] + bits[:shifts]

def xor(bits1, bits2):
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
P4 = [2, 4, 3, 1]
IP = [2, 6, 3, 1, 4, 8, 5, 7]
IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]
EP = [4, 1, 2, 3, 2, 3, 4, 1]
S0 = [[1, 0, 3, 2],
      [3, 2, 1, 0],
      [0, 2, 1, 3],
      [3, 1, 3, 2]]
S1 = [[0, 1, 2, 3],
      [2, 0, 1, 3],
      [3, 0, 1, 0],
      [2, 1, 0, 3]]

def generate_keys(key):
    key = permute(key, P10)
    left, right = key[:5], key[5:]
    left, right = shift_left(left, 1), shift_left(right, 1)
    k1 = permute(left + right, P8)
    left, right = shift_left(left, 2), shift_left(right, 2)
    k2 = permute(left + right, P8)
    return k1, k2

def sbox_substitution(bits, sbox):
    row = (bits[0] << 1) + bits[3]
    col = (bits[1] << 1) + bits[2]
    val = sbox[row][col]
    return [val >> 1, val & 1]

def fk(bits, key):
    left, right = bits[:4], bits[4:]
    right_expanded = permute(right, EP)
    right_xor = xor(right_expanded, key)
    s0_out = sbox_substitution(right_xor[:4], S0)
    s1_out = sbox_substitution(right_xor[4:], S1)
    sbox_out = permute(s0_out + s1_out, P4)
    return xor(left, sbox_out) + right

def sdes_encrypt(plain_bits, key):
    k1, k2 = generate_keys(key)
    bits = permute(plain_bits, IP)
    bits = fk(bits, k1)
    bits = bits[4:] + bits[:4]
    bits = fk(bits, k2)
    return permute(bits, IP_INV)

def sdes_decrypt(cipher_bits, key):
    k1, k2 = generate_keys(key)
    bits = permute(cipher_bits, IP)
    bits = fk(bits, k2)
    bits = bits[4:] + bits[:4]
    bits = fk(bits, k1)
    return permute(bits, IP_INV)

def text_to_bits(text):
    return [int(b) for char in text for b in format(ord(char), '08b')]

def bits_to_text(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(''.join(map(str, c)), 2)) for c in chars)

# Зчитування вхідного повідомлення з файлу
with open("message.txt", "r", encoding="utf-8") as f:
    message = f.read().strip()

key_input = input("Введіть 10-бітний ключ: ")
key = [int(b) for b in key_input.strip()]

plaintext_bits = text_to_bits(message)
print(f"Текст переведений в біти: {plaintext_bits}")

# Шифрування
encrypted_bits = []
for i in range(0, len(plaintext_bits), 8):
    block = plaintext_bits[i:i+8]
    if len(block) < 8:
        block += [0] * (8 - len(block))  # Додаємо нулі до 8 біт
    encrypted_bits.extend(sdes_encrypt(block, key))

encrypted_text = bits_to_text(encrypted_bits)
with open("encrypted.txt", "w", encoding="utf-8") as f:
    f.write(encrypted_text)
print(f"Зашифровано: {encrypted_text}")

# Розшифрування
decrypted_bits = []
for i in range(0, len(encrypted_bits), 8):
    block = encrypted_bits[i:i+8]
    decrypted_bits.extend(sdes_decrypt(block, key))

decrypted_text = bits_to_text(decrypted_bits)
with open("decrypted.txt", "w", encoding="utf-8") as f:
    f.write(decrypted_text)
print(f"Розшифровано: {decrypted_text}")
