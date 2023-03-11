# gofileFFASTRANS
Send file from FFASTRANS to Gofile

This is a Python script that collects output data from FFASTRANS, uploads the file to GOFILE, and sends the link to the specified email. Here's a brief rundown of what the script does:

It imports several Python modules for sending HTTP requests, email handling, and timestamp management.
It defines a function that sends an email with the file link and log data.
It sets several variables based on command-line arguments passed to the script, such as the name of the file, the name of the workflow, and the duration of the conversion.
It sends an HTTP GET request to https://apiv2.gofile.io/getServer to obtain the server URL to upload the file.
If the server returns an "ok" status, the script sends an HTTP POST request to the server URL to upload the file and get the file code.
It then generates an email message with the file link and log data and sends the email to the specified recipient(s).
There are several parts of the code that are not shown in this code snippet, such as the SMTP server address and credentials, as well as the HTML formatting for the email message. The code also catches and handles exceptions using the try and except blocks.
