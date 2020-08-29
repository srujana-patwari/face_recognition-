import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send(filename):
    from_add = 'kulkarnisrujana66@gmail.com'
    to_add = 'srujanapatwari@gmail.com'
    subject = 'Finance Stock Report'

    msg = MIMEMultipart()
    msg['From'] = from_add
    msg['To'] = to_add
    msg['Subject'] = subject

    body = '<bTodays Finance Report Attached.</b'
    msg.attach(MIMEText(body,'html'))

    my_file = open(filename,'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((my_file).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition','attachment; filename= ' + filename)
    msg.attach(part)

    message = msg.as_string()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('kulkarnisrujana66@gmail.com','sgciaicylljgwivc')

    server.sendmail(from_add, to_add,message)

    server.quit()