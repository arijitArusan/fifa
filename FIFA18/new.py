import smtplib
from flask_mail import Mail,Message
from sample2 import app
app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='arijitd1791@gmail.com',
    MAIL_PASSWORD='zwjnvsaitxwdkdwp',
)
mail=Mail(app)