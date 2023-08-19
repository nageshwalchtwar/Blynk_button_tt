import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import firebase_admin
from firebase_admin import credentials, storage, firestore

# Email configuration
sender_email = 'rtllab55@gmail.com'
sender_password = 'evyvskiyltlczpaj'
receiver_emails = ['nageshwalchtwar257@gmail.com', 'akshit.gureja@research.iiit.ac.in', 'rishabh.agrawal@students.iiit.ac.in']
mail_server = 'smtp.gmail.com'  
mail_port = 587

def get_res():
    url = "https://blr1.blynk.cloud/external/api/get?token=vTZNEt9WyE--pOBu6LmH_QMAkoEcC4hd&v3"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    on_btn = response.text
    return on_btn

def send_email(subject, body, receivers):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(receivers)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(mail_server, mail_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receivers, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email")

prev_status = '0'  # Initializing previous status as '0'

# Initialize Firebase with your project credentials
cred = credentials.Certificate("credentials.json")  # Update the path
firebase_admin.initialize_app(cred, {"storageBucket": "blynk-usage.appspot.com"})
# Read and upload the README file
bucket = storage.bucket()
README_path = "README.md"  # Update with actual path

def upload_to_firebase(content):
    blob = bucket.blob("README.md")
    blob.upload_from_string(content)

while True:
    status = get_res()

    if status != prev_status:  # If there's a change in status, log the timestamp to README
        with open("README.md", "a") as file:
            if status == '1':
                file.write(f"- Button Usage pressed at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            else:
                file.write(f"- Experiment is not in use at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        prev_status = status  # Update previous status with the current status

    current_time = time.strftime('%H:%M')
    if current_time == '00:00:01':
        # Send email at 00:00 (midnight) every day
        with open("README.md", "r") as file:
            log_content = file.read()
            send_email("Button Usage Log of VR - RTL", log_content, receiver_emails)
    with open(README_path, "r") as file:
        content = file.read()
        upload_to_firebase(content)
            

    time.sleep(1)
