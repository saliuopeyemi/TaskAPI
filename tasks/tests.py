# import smtplib

# s = smtplib.SMTP("smtp.gmail.com",587,timeout=200)
# s.starttls()

# s.login("saliuoazeez@gmail.com","Hhlbbcnofns2$")
# message="Testing out this message"

# s.sendmail("saliuoazeez@gmail.com","saliuoazeez@gmail.com",message)

# s.quit()

import yagmail

def send_email():
    yag = yagmail.SMTP(user="saliuoazeez@gmail.com", password="Hhlbbcnofns1$")
    subject = "Test Email with yagmail"
    body = "Hello, this is a test email using yagmail!"
    yag.send(to="saliuoazeez@gmail.com", subject=subject, contents=body)
    print("Email sent successfully!")

send_email()