import smtplib 

smtpServer = 'smtp.gmail.com'
fromadr = 'devprueba282@gmail.com'
toadr = 'marie.adim@gmail.com'
text = "prueba"
server = smtplib.SMTP(smtpServer, 587)
#server.ehlo()
server.starttls()
server.login(fromadr, 'fnwt fftq pqpq alkh')
server.sendmail(fromadr, toadr, text)
server.quit()
