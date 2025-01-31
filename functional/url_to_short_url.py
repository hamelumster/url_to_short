import string
import random


def url_to_short_url(input_url: str) -> str:
    new_url = ''
    slash_count = 0

    for el in input_url:
        new_url += el
        if el == '/':
            slash_count += 1
        if slash_count == 3:
            break

    code = ''.join(random.choices(string.ascii_letters, k=8))
    short_url = new_url + code

    return short_url

