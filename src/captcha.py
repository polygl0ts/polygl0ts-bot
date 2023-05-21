import random
import string

import config

# Global storage for user captcha values
captchas = dict()
# Charset used for generating the random verification codes
charset = string.ascii_letters + string.digits


def generate_captcha(user_id):
    user_captcha = "".join(
        random.choice(charset) for _ in range(config.user_verification.captcha_length)
    )
    captchas[user_id] = user_captcha
    return user_captcha


def validate_captcha(user_id, user_captcha):
    cleaned_captcha = str(user_captcha).strip()

    saved_captcha = captchas.get(user_id, "")

    if saved_captcha == cleaned_captcha:
        # Remove the captcha upon successful verification
        del captchas[user_id]
        return True
    else:
        # Don't remove the captcha from the dict yet - give the user another chance :)
        return False
