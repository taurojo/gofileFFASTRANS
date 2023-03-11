#!/usr/bin/python
# -*- coding: UTF-8 -*-
# This code retrieves output data from FFASTRANS.
# It collects the output data and uploads the file to GOFILE.
# It sends the link to the email address specified.


from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
import json
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from datetime import datetime
from datetime import timedelta


try:
  
    # Create a log and add the starting time to it
    now = datetime.now()
    formatTimeINICIO = now.strftime('%d/%m/%Y, %H:%M:%S')

  # Create a log and add the starting time to it
    log = "INICIO" + formatTimeINICIO

  # Get the command line arguments from FFASTRANS
    nameficheroData= sys.argv[1]	
    workdata= sys.argv[2]
    name= sys.argv[3]
    duracion= sys.argv[4]

  # Retrieve the server data for uploading
    data = requests.get('https://apiv2.gofile.io/getServer').json()
        #{'status': 'ok', 'data': {'server': 'srv-store3'}}

    print(data)

  # Check if the server status is ok. If not, try again.
    if data['status']== "ok":
        servidorfre = (data['data']['server'])
       
        servidorup = "https://" + servidorfre + ".gofile.io/uploadFile"
  
    # Launch the curl from Python
    # curl -F email=myname@example.com -F file=@file.txt https://srv-file6.gofile.io/uploadFile
    # Response example
    # {"status":"ok","data":{"code":"123Abc","adminCode":"3ZcBq12nTgb4cbSwJVYY","fileName":"file.txt"}}
    
        
    # Add the server data to the log
        log += "</br> ok: "+ json.dumps(data)
    else:
        log = "</br> ERROR:"+json.dumps(data)

# Create a MultipartEncoder to upload the file
    mp_encoder = MultipartEncoder(
        fields={
            'file': (nameficheroData, open(nameficheroData, 'rb'))
        }
    )


# Send a POST request to upload the file
    r = requests.post(servidorup,data=mp_encoder, 
        headers={'Content-Type': mp_encoder.content_type}
    ).json()

# Get the link for the uploaded file and add the response data to the log
    link = "https://gofile.io/?c="+ r['data']['code'] 

    log += "</br> respuesta Gofile: "+ json.dumps(r)
        


# Set the email addresses for sending the email

    # me == my email address
    # you == recipient's email address
    me = "xxxxx@xxxxx.xx"
    # you = "xxxxx@xxxx.xxx"
    

# Add the file information and link to the email body
        you = ['xxxx@xxx.xxx' ,'xxxx@xxxx.xx']

# Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Envio:{workdata} | {name}"
    msg['From'] = me
    msg['To'] = you

#Log create text
    now = datetime.now()
    formatTimeINICIO = now.strftime('%d/%m/%Y, %H:%M:%S')
    log += "<br>nameficheroData: "+nameficheroData +"<br>"+"workdata"+workdata +"<br>"+"name"+name +"<br>"+"duracion"+duracion+"<br>"+"<br> FIN" + formatTimeINICIO


# Create the body of the message (a plain-text and an HTML version).
    text = f"Link: {link}, from file: {name} from conversor {workdata}"
    html = f"""\
    <html>
      <head>CONVERSOR</head>
      <body>
        <p>
           File: {name}<br>
           Dur: {duracion}<br>
           Workflow: {workdata}<br>
           Link: <a href="{link}">{name}</a>
        <br>
        <br>
        <br>
        </p>
        <p>LOG <br>
        <small> {log}</small></p>
      </body>
    </html>
    """

# Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP('smtp.epi.es')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, you, msg.as_string())
    s.quit()
    sys.exit()	


except Exception as e: 
     
#If error send mail to admin

    print (e)
    # me == my email address
    # you == recipient's email address
    me = "xxxx@xxxx.xx"
    ##Aqui definimos a quien va el error.
    you = "xxxx@xxxx.xx"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"ERROR!!! Conversion:{workdata} | {name}"
    msg['From'] = me
    msg['To'] = "xxxx@xxxx.xx"

    #Parte para el log
    log ="LOG DE ERRORES:"
    now = datetime.now()
    log += "<br>nameficheroData:"+nameficheroData +"<br>"+"workdata"+workdata +"<br>"+"name"+name +"<br>"+"duration"+duracion+"<br>"+"<br>"


    # Create the body of the message (a plain-text and an HTML version).
    text = f"This is the link {link}, from file{name} in workdata: {workdata}"
    html = f"""\
    <html>
      <head>CONVERSOR</head>
      <body>
        <p> 
        {e}
           File: {name}<br>
           Dur: {duracion}<br>
           Workflow: {workdata}<br>
           Link: <a href="{link}">{name}</a>
        <br><br><br>
        </p>
        <p>LOG <br>
        <small> {log}</small></p>
      </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP('smtp.epi.es')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, you, msg.as_string())
    s.quit()
    
    sys.exit()	
