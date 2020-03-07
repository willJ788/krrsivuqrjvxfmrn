import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import serial
import picamera
from time import sleep
from twilio.rest import Client
import zipfile

def send_sms():
    account_sid = 'AC439b14cc5ee988deb151536b6774703f'
    auth_token = '8b80eafbf5e9639efff47084ee22a63c'

    client = Client(account_sid, auth_token)

    client.messages.create(
        to='+447484152911',
        from_="+12017204907",
        body="!ALERT!\nSomeone has entered your room"
    )

def send_error():
    account_sid = 'AC439b14cc5ee988deb151536b6774703f'
    auth_token = '8b80eafbf5e9639efff47084ee22a63c'

    client = Client(account_sid, auth_token)

    client.messages.create(
        to='+447484152911',
        from_="+12017204907",
        body="System ERROR 303!\nSystem 'sudo shutdown -h now'\nManual Maintenance Required..."
    )

def take_img():
    camera = picamera.PiCamera()
    camera.capture('/home/pi/Desktop/img1.jpg')
    timer(1)
    camera.capture('/home/pi/Desktop/img2.jpg')
    timer(1)
    camera.capture('/home/pi/Desktop/img3.jpg')
    timer(1)
    camera.capture('/home/pi/Desktop/img4.jpg')
    timer(1)
    camera.capture('/home/pi/Desktop/img5.jpg')

def send_img():
    with zipfile.ZipFile(r"/home/pi/Desktop/alert_photos.zip", 'w') as my_zip:
        my_zip.write(r"/home/pi/Desktop/img1.jpg")
        my_zip.write(r"/home/pi/Desktop/img2.jpg")
        my_zip.write(r"/home/pi/Desktop/img3.jpg")
        my_zip.write(r"/home/pi/Desktop/img4.jpg")
        my_zip.write(r"/home/pi/Desktop/img5.jpg")

    email_user = 'williamrcjohnston@gmail.com'
    email_password = 'krrsivuqrjvxfmrn'
    email_send = 'williamrcjohnston@gmail.com'

    subject = '!ALERT! someone has entered room!'

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    body = 'Someone has entered your room! Here are photos from scene...'
    msg.attach(MIMEText(body, 'plain'))

    filename = r"/home/pi/Desktop/alert_photos.zip"

    attachment = open(filename, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= "+filename)

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)
    server.sendmail(email_user, email_send, text)
    server.quit()
def door_open_protocal():
    global asdata
    while True:
        value = asdata.readline()
        print(int(value))
        if int(value) == 202:
            pass
        elif int(value) == 101:
            serial_read()
        else:
            pass
             
def serial_read():
    global asdata
    not_error = True
    while not_error:
        if asdata.inWaiting() > 0:
            mydata = asdata.readline()
            print(int(mydata))
            if int(mydata) == 101:
                pass
            elif int(mydata) == 202:
                send_sms()
                print('sms sent')
                take_img()
                print('img taken')
                send_img()
                print('img sent')
                sleep(5)
                if int(mydata) == 202:
                    door_open_protocal()
            elif int(mydata) == 303:
                send_error()
                not_error = False
                break
        else:
            pass

sleep(30)
asdata = serial.Serial('com8', 9600)
serial_read()
