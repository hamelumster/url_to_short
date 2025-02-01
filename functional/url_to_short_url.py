import string
import random


def url_to_short_url() -> str:
    main_url = "https://url-to-short-url.onrender.com/"
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    short_url = main_url + code

    return short_url

