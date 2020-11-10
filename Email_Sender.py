#Script for sending an email with the smtplib library and gmail account

#!/usr/bin/env python3

import email.message
import mimetypes
import os.path
import smtplib
import ssl

def generate_email(sender, recipient, subject, body, attachment_path = None):
	message = email.message.EmailMessage()
	message["From"] = sender
	message["To"] = recipient
	message["Subject"] = subject
	message.set_content(body)

	if attachment_path:
		attachment_filename = os.path.basename(attachment_path)
		mime_type, _ = mimetypes.guess_type(attachment_path)
		mime_type, mime_subtype = mime_type.split('/', 1)

		with open(attachment_path, 'rb') as ap:
			message.add_attachment(ap.read(),
									maintype = mime_type,
									subtype = mime_subtype,
									filename = attachment_filename)
	return message

def send_email(message):
	port = 465
	password = "password"
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
		server.login("email@gmail.com", password)
		server.send_message(message)
		server.quit()
