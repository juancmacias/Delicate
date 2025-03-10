import smtplib 
import os
from dotenv import load_dotenv

def Mail(email_sender:str):
    smtpServer = 'smtp.gmail.com'
    fromadr = 'devprueba282@gmail.com'
    toadr = email_sender
    text = "prueba"
    password = os.getenv('MAIL_PASS')

    if not password:
        raise Exception("No se encontró la contraseña en el archivo .env")

    try:
        # Establecer la conexión SMTP
        server = smtplib.SMTP(smtpServer, 587)
        server.starttls()
        server.login(fromadr, password)

        server.sendmail(fromadr, toadr, text)
        server.quit()
        print("Correo enviado exitosamente")

    except Exception as e:
        print(f"Error al enviar el correo: {e}")