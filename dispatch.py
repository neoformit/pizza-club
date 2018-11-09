# Import django models:
import os
import sys
import django
sys.path.append(r'C:\Users\Public\Documents\Google Drive\Python\Django\pizzaclub')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pizzaclub.settings")
django.setup()
from django.apps import apps
Order = apps.get_model('form','Order')
#==============================================================================
import schedule
import datetime
import smtplib
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#==============================================================================


def send_email(to,body):
    fromaddr = 'uscpizzatime@gmail.com'
    toaddr = to
    username = 'uscpizzatime'
    password = 'givemepizza'
    msg = MIMEMultipart('alternative')
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = 'Sent at %s' % str(datetime.datetime.now().time())[:8]
    msg.attach(MIMEText(body, 'html', 'UTF-8'))
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()

#===============================================================================

def html_table(orders):
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    table {
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
    }
    
    td, th {
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
    }
    
    tr:nth-child(even) {
        background-color: #dddddd;
    }
    </style>
    <body>
    
    <h2>Here are this week's pizza orders!</h2>
    <br>
    
    <table style="width:100%">
      <tr>
        <th>Name</th>
        <th>Order</th> 
        <th>Cost</th>
        <th>Comments</th>
      </tr>
    """
    
    for o in orders:
        entries = (o.name, o.item, str(o.cost), o.comments)
        html += "<tr>"
        for e in entries:
            html += "<td>" + e + "</td>\n"
        html += "</tr>"
    
    html += "</table> </body> </html>"
    
    return html        
        
#==============================================================================
    
def dispatch():
    
    def tab(text):
        return " " * (25 - len(text))
    
    today = datetime.date.today()
    cutoff = str(today.replace(day = today.day-5))

    orders = Order.objects.filter(date__gt=cutoff)
    
    pizzaman = "cameron.hyde@research.usc.edu.au"
    
    body = html_table(orders)
    
    f=0
    while True:
        try:
            send_email(pizzaman,body)
            print("Email sent")
            break
        except:
            print("Smtp connection failed. Trying again...")
            f+=1
            if f == 2:
                print("Smpt connection failed.")
                break
            else: continue

schedule.every().friday.at("01:10").do(dispatch)

while True:
    schedule.run_pending()
    sleep(10)
