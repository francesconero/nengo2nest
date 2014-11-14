'''
Created on Aug 24, 2014

@author: Francesco Nero
'''


def char_range(s):
    return list(map(chr, range(ord(s[0]), ord(s[-1]) + 1)))


def latin_alphabet():
    return char_range('A-I') + char_range('L-V') + ['Z']


def name_from_number(n):
    alphabet = latin_alphabet()
    return encode_number(n, alphabet)


def encode_number(n, alphabet):
    out = ''
    k = len(alphabet)
    while n > 0:
        out = alphabet[(n - 1) % k] + out
        if n % k == 0:
            n -= 1
        n //= k
    return out


def chop_int(N, M):
    while N > M:
        N -= M
        yield M
    if N > 0:
        yield N