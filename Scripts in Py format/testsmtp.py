import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import datetime

now = datetime.datetime.now()
Today_date = now.strftime("%Y-%m-%d") ##Today's Date

pd.set_option('display.max_colwidth', -1)
location = 'To Upload/'+str(Today_date)+'/'+str(Today_date)+'.xlsx'
df = pd.read_excel(location)
df = df[['Heading','URL']]
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "cocaditya1@gmail.com"  # Enter your address
receiver_email = "shweta.pandey@lnmiit.ac.in"  # Enter receiver address
password = "aditya24401"

message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
text = """\
Hi,
How are you?
Real Python has many great tutorials:
www.realpython.com"""
html = """\
<html>
  <body>
    <h3>Please find data attached and below.</h3>
                   {}
  </body>
</html>
""".format(df.to_html())
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

message.attach(part1)
message.attach(part2)

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    
