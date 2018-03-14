S_BOX = [
    [7, 14, 4, 13],
    [12, 1, 0, 6],
    [9, 8, 5, 3],
    [10, 15, 11, 2]
]

P_BOX_MSG = [
    5, 15, 7, 2, 4, 0, 9, 8, 12, 1, 10, 14, 3, 6, 11, 13
]

P_BOX_KEY = [
    12, 6, 46, 11, 14, 50, 22, 33, 20, 24, 19, 34, 63, 25, 9, 31, 29, 13, 54, 7,
    47, 28, 32, 3, 52, 53, 61, 40, 26, 41, 2, 43, 35, 21, 39, 48, 27, 44, 45, 42,
    62, 55, 10, 36, 49, 58, 15, 5, 37, 59, 38, 60, 0, 8, 16, 4, 1, 17, 23, 18, 30,
    56, 57, 51
]

def separate_to_blocks(input_text):
    # Chagen an input text into 128 bit block
     bin_str = ''.join('{0:08b}'.format(ord(x), 'b') for x in input_text)
     count = 0
     block = ""
     blocks = []
     for i, c in enumerate(bin_str):
         if (len(block) < 128):
             block += c
         else:
             blocks.append(block)
             block = ""

     # Pad message if it's not divisible by 128
     if (block != ""):
         while (len(block) != 128):
             block += "0" #dummy padding
         blocks.append(block)
     return blocks

def separate_text(block_text):
    left_block = ""
    right_block = ""
    for i, c in enumerate(block_text):
        if (i < 64):
            left_block += c
        else:
            right_block += c
    return (left_block, right_block)

def separate_key(key):
    bin_str = ''.join('{0:08b}'.format(ord(x), 'b') for x in key)
    odd_key = ""
    even_key = ""
    for i, c in enumerate(bin_str):
        if (i % 2 == 0):
            even_key += c
        else:
            odd_key += c
    return (odd_key, even_key)

def convert_block_to_matrix(block):
    block_matrix = []
    block_row = []
    el = ""
    count_row = 0
    for i, c in enumerate(block):
        if (i % 4 != 0) or (i == 0):
            el += c
        else:
            block_row.append(el)
            el = c
            count_row += 1
            if (count_row) == 4:
                block_matrix.append(block_row)
                block_row = []
                count_row = 0

    if (block_row):
        block_row.append(el)
        block_matrix.append(block_row)
    return block_matrix

def convert_matrix_to_block(matrix):
    result = ""
    for i in range(4):
        for j in range(4):
            result += matrix[i][j]
    return result

def xor_matrix_multipiclation(right_block, key_block):
    """
        Input : 64 bit blocks
        Output : return xor multipiclation
    """
    result = [['A' for x in range(4)] for x in range(4)]
    def xor_str(in1, in2):
        if (in1 == in2):
            return "0"
        else:
            return "1"
    for i in range(4):
        for j in range(4):
            el1 = right_block[i][j]
            el2 = key_block[i][j]
            res = ""
            for k, c in enumerate(el1):
                res += xor_str(el1[k], el2[k])
            result[i][j] = res
    return result

def substitute(block):
    """
        Do substitution process for 4x4 box block with S-BOX
    """
    result = [['A' for x in range(4)] for x in range(4)]
    for i in range(4):
        for j in range(4):
            el = block[i][j]
            row_str = el[0] + el[2]
            row = int(row_str, 2)
            col_str = el[1] + el[3]
            col = int(col_str, 2)
            sub_el = "{0:04b}".format(S_BOX[row][col])
            result[i][j] = sub_el
    return result

def get_row_col_idx(val):
    for i in range(4):
        for j in range(4):
            if (S_BOX[i][j] == int(val, 2)):
                return (i, j)

def unsubstitute(block):
    """
        Do substitution process for 4x4 box block with S-BOX
    """
    result = [['A' for x in range(4)] for x in range(4)]
    for i in range(4):
        for j in range(4):
            el = block[i][j]
            row, col = get_row_col_idx(el)
            row_bin = "{0:02b}".format(row)
            col_bin = "{0:02b}".format(col)
            sub_el = row_bin[0] + col_bin[0] + row_bin[1] + col_bin[1]
            result[i][j] = sub_el
    return result

def slide(block):
    """
        Slide element in block
    """
    result = [['A' for x in range(4)] for x in range(4)]
    for i in range(4):
        for j in range(4):
            if (i % 2 == 0):
                if (j+1 >= 4):
                    k = 0
                else:
                    k = j+1
            else:
                if (j-1 < 0):
                    k = 3
                else:
                    k = j-1
            result[i][j] = block[i][k]
    return result

def unslide(block):
    """
        Unslide element in block
    """
    result = [['A' for x in range(4)] for x in range(4)]
    for i in range(4):
        for j in range(4):
            if (i % 2 == 0):
                if (j-1 < 0):
                    k = 3
                else:
                    k = j-1
            else:
                if (j+1 >= 4):
                    k = 0
                else:
                    k = j+1
            result[i][j] = block[i][k]
    return result

def block_to_bin_str(block):
    result = ""
    for i in range(4):
        for j in range(4):
            result += block[i][j]
    return result

def scramble_key(key):
    """
        Scramble key with P-Box
    """
    result = ['A' for x in range(64)]
    for i, c in enumerate(key):
        result[P_BOX_KEY[i]] = key[i]
    return ''.join(result)

def scramble_text(block):
    result = [['A' for x in range(4)] for x in range(4)]

    temp_list = []
    for i in range(4):
        for j in range(4):
            temp_list.append(block[i][j])

    scrambled_list = ['A' for x in range(16)]
    for i in range(16):
        scrambled_list[P_BOX_MSG[i]] = temp_list[i]

    scrambled_matrix = [['A' for x in range(4)] for x in range(4)]
    for i in range(16):
        scrambled_matrix[i // 4][i % 4] = scrambled_list[i]
    return scrambled_matrix

def unscramble_text(scrambled_block):
    result = [['A' for x in range(4)] for x in range(4)]
    temp_list = []
    for i in range(4):
        for j in range(4):
            temp_list.append(scrambled_block[i][j])

    scrambled_list = ['A' for x in range(16)]
    for i in range(16):
        scrambled_list[i] = temp_list[P_BOX_MSG[i]]

    scrambled_matrix = [['A' for x in range(4)] for x in range(4)]
    for i in range(16):
        scrambled_matrix[i // 4][i % 4] = scrambled_list[i]
    return scrambled_matrix

def key_expansion(i, key):
    """
        Expand key using key expansion function
    """
    odd_key, even_key = separate_key(key)
    if (i == 0):
        key = scramble_key(odd_key)
    elif (i == 9):
        key = odd_key[::-1]
        key = scramble_key(key)
    else:
        key = even_key[63] + even_key[:63]
        key = scramble_key(key)
    return key

def xor_op(str1, str2):

    if (len(str1) != len(str2)):
        return -1
    else:
        result = ""
        for i, c in enumerate(str1):
            if (str1[i] == str2[i]):
                result += "0"
            else:
                result += "1"
        return result

def  f_function(block, key):
    res1 = xor_matrix_multipiclation(block, key)
    res2 = substitute(res1)
    res3 = slide(res2)
    res4 = scramble_text(res3)
    result = convert_matrix_to_block(res4)
    return result

def enchiper_block(block, key_in):
    # Encryption process
    left_block, right_block = separate_text(block)
    for i in range(10):
        temp = left_block
        left_block = right_block
        key = key_expansion(i, key_in)
        right_block_mat = convert_block_to_matrix(right_block)
        key = convert_block_to_matrix(key)
        right_block = xor_op(temp, f_function(right_block_mat, key))
    return (left_block + right_block)

def dechiper_block(block, key_in):
    left_block, right_block = separate_text(block)
    i = 9
    while (i >= 0):
        temp = right_block
        right_block = left_block
        key = key_expansion(i, key_in)
        left_block_mat = convert_block_to_matrix(right_block)
        key = convert_block_to_matrix(key)
        left_block = xor_op(temp, f_function(left_block_mat, key))
        i -= 1
    return (left_block + right_block)

def encrypt(text, key):
    blocks = separate_to_blocks(text)
    ciphertext = ""
    for block in blocks:
        ciphertext += enchiper_block(block, key)
    result = ""
    i = 0
    print (len(ciphertext))
    while (i < len(ciphertext)):
        result += chr(int(ciphertext[i:(i+8)], 2))
        i += 8
    return result

def decrypt(text, key):
    blocks = separate_to_blocks(text)
    ciphertext = ""
    for block in blocks:
        ciphertext += dechiper_block(block, key)
    result = ""
    i = 0
    while (i < len(ciphertext)):
        result += chr(int(ciphertext[i:(i+8)], 2))
        i += 8
    return result

def main():
    text = input("Input your plaintext (minimum 16 character) :")
    key = input("Input your key (must 16 character) :")
    ciphertext = encrypt(text, key)
    print (ciphertext)
    print (len(ciphertext))
    d = decrypt(ciphertext, key)
    print (d)
    print (len(d))

if __name__ == "__main__":
    main()
