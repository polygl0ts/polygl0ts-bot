import random
import string

import config

# Global storage for user captcha values
captchas = dict()
# Charset used for generating the random verification codes
charset = string.ascii_letters + string.digits + string.punctuation


def generate_captcha(user_id):
    user_captcha = "".join(random.choice(charset) for _ in range(config.user_verification.captcha_length))
    captchas[user_id] = user_captcha
    return user_captcha


def validate_captcha(user_id, user_captcha):
    cleaned_captcha = str(user_captcha).strip()
    return captchas.pop(user_id, "") == cleaned_captcha
