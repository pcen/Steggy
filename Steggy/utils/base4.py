# encodes values to a base-4 representation

# convert string to a list representing bits
def encode_binary(string):
    binary = []
    for char in string:
        bits = [int(bit) for bit in format(ord(char), 'b')]
        binary.append(bits)
    return binary

# convert list representing bits to a string
def decode_binary(binary):
    string = ''
    for bits in binary:
        bs = ''.join([str(bit) for bit in bits])
        string += chr(int('0b' + bs, 2))
    return string

# convert an integer to a base-4 representation
def int_to_b4(n):
    base4 = []
    q, r = (n // 4, n % 4)
    while q != 0:
        base4.append(r)
        q, r = (q // 4, q % 4)
    base4.append(r)
    while True:
        if len(base4) < 4:
            base4.append(0)
        else:
            return base4

# convert a base-4 byte representation to an integer
def b4_to_int(digits):
    unicode = 0
    for exp, digit in enumerate(digits):
        unicode += digit * (4 ** exp)
    return unicode

# convert a string to a base-4 representation
def encode(string):
    unicodes = [ord(char) for char in string]
    b4_encoding = []
    for n in unicodes:
        b4_encoding.append(int_to_b4(n))
    return b4_encoding

# convert a base-4 sequence of bytes to a string
def decode(encoded):
    string = ''
    unicodes = []
    for word in encoded:
        unicodes.append(b4_to_int(word))
    return string.join(chr(char) for char in unicodes)
