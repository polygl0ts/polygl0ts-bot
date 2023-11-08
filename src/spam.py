import config
import smtplib

from email.message import EmailMessage


def send_mail(recipient, user_captcha):
    # Create the email to send
    msg = EmailMessage()
    msg["From"] = config.email.username
    msg["To"] = recipient
    msg["Subject"] = "Verification code for polygl0ts Discord server"
    msg.set_content(f'Hello {recipient}, your verification code is "{user_captcha}"!')

    with smtplib.SMTP_SSL(
        host=config.email.smtp_host, port=config.email.smtp_port
    ) as smtp_conn:
        try:
            # Mail go brrrrr
            smtp_conn.login(user=config.email.username, password=config.email.password)
            smtp_conn.sendmail(
                from_addr=config.email.username, to_addrs=recipient, msg=msg.as_bytes()
            )
        except smtplib.SMTPException as e:
            return False
    return True
