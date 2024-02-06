import random

def codeRandomizer(lenght):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    code = ''

    for i in range(lenght):
        code += random.choice(characters)

    return code