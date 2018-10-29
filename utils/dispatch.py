import schedule
import datetime
import smtplib
from time import sleep
from form.models import Order
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to,msg):
    fromaddr = 'uscpizzatime@gmail.com'
    toaddr = to
    text = msg
    username = 'uscpizzatime'
    password = 'givemepizza'
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = 'Pizza time!'
    msg.attach(MIMEText(text))
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()

#===============================================================================

def dispatch():
    today = datetime.date.today()
    cutoff = str(today.replace(day = today.day-5))

    orders = Order.objects.filter(date__gt=cutoff)

    body = "Name\t\tOrder\t\tCost"
    
    pizzaman = "cameron.hyde@research.usc.edu.au"
    
    if len(orders):
        for order in orders:
            body += "\n"
            body += ("%s\t\t%s\t\t%s" % (order.name,order.item,order.cost))

        message = """

        Happy Friday, you are this week's selected pizza fetcher!

        Here are this week's orders:

        %s

        """ % body

        send_email(pizzaman,message)

schedule.every().monday.at("11:57").do(dispatch)
while True:
    schedule.run_pending()
    sleep(30)