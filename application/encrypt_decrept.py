import os

def Set_codebook():
    enc_dict = {'A': '01', 'B': '02', 'C': '03', 'D': '04', 'E': '05', 'F': '06', 'G': '07', 'H': '08', 'I': '09',
                 'J': '10', 'K': '11',
                 'L': '12', 'M': '13', 'N': '14', 'O': '15', 'P': '16', 'Q': '17', 'R': '18', 'S': '19', 'T': '20',
                 'U': '21', 'V': '22',
                 'W': '23', 'X': '24', 'Y': '25', 'Z': '26',
                 '0': '90', '1': '91', '2': '92', '3': '93', '4': '94', '5': '95', '6': '96', '7': '97', '8': '98',
                 '9': '99'
                 }
    dec_dict = {}
    for key in enc_dict.keys():
        dec_dict[enc_dict[key]] = key

    return enc_dict, dec_dict

def encrypt(msg, enc_dict, option = 'shift'):

    enc_book = []
    for s in msg:
        enc_book.append(enc_dict[s])
    msg_encrypt = ''.join(enc_book)
    return msg_encrypt

def decrypt(msg, dec_dict,option = 'shift'):
    dec_book = []
    msg_ls = []

    while (len(msg)):
        word = msg[:2]
        msg_ls.append(word)
        msg = msg[2:]

    for s in msg_ls:
        dec_book.append(dec_dict[s])

    msg_decrypt = ''.join(dec_book)
    return msg_decrypt



if __name__ == '__main__':
    msg = 'ABC'
    enc_dict , dec_dict = Set_codebook()
    msg_enc = encrypt(msg,enc_dict)
    print('encrypt', msg  , '-->', msg_enc)
    msg_dec = decrypt(msg_enc, dec_dict)
    print('decrypt', msg_enc, msg_dec)