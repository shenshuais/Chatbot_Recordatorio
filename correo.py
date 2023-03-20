import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configura los datos del servidor SMTP y del correo electrónico emisor
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'shenshauai@gmail.com' 
smtp_password = 'zqwernjidirvprke'
from_email = 'shenshauai@gmail.com'  

def enviar(para, asunto, cuerpo):
    # Configura los datos del correo electrónico receptor
    if para and asunto and cuerpo: 
        to_email = para  
        subject = asunto
        body = cuerpo

        # Crea el mensaje MIME
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Crea una conexión segura con el servidor SMTP y envía el mensaje
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(from_email, to_email, message.as_string())
    else: 
        print("Error: Información incompleta")







