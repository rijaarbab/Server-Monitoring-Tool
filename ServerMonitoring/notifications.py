import smtplib
import requests
import yaml
from email.mime.text import MIMEText

email_enabled = False
email_smtp_server = ""
email_smtp_port = 587
email_sender = ""
email_password = ""
email_recipients = []

slack_enabled = False
slack_webhook = ""
slack_channel = ""
slack_username = ""

def load_notification_config():
    global email_enabled, email_smtp_server, email_smtp_port
    global email_sender, email_password, email_recipients
    global slack_enabled, slack_webhook, slack_channel, slack_username    
    try:
    
        with open("configs/config.yaml", 'r') as f:
            config = yaml.safe_load(f)
            
            # Load Email config
            email_config = config['notifications']['email']
            email_enabled = email_config['enabled']
            email_smtp_server = email_config['smtp_server']
            email_smtp_port = email_config['smtp_port']
            email_sender = email_config['sender_email']
            email_password = email_config['sender_password']
            email_recipients = email_config['recipient_emails']
            
            # Load Slack config
            slack_config = config['notifications']['slack']
            slack_enabled = slack_config['enabled']
            slack_webhook = slack_config['webhook_url']
            slack_channel = slack_config['channel']
            slack_username = slack_config['username']
    except:
        pass

def send_email(alert, metrics):
    if not email_enabled:
        return
    
    try:
        subject = f"[{alert['level']}] {alert['type']} Alert"
        
        message = f"Alert: {alert['message']}\nTime: {alert['time']}\n\nServer: {metrics['hostname']}\nOS: {metrics['os']}\n"
        
        msg = MIMEText(message)
        
        msg['To'] = ', '.join(email_recipients)
        msg['From'] = email_sender
       
        msg['Subject'] = subject
        
        server = smtplib.SMTP(email_smtp_server, email_smtp_port)
        server.starttls()
        server.login(email_sender, email_password)
        server.send_message(msg)
        server.quit()
        
        print(f"Email sent to {', '.join(email_recipients)}")
    except:
        print("Email sent failed ")

def send_slack(alert, metrics) :
    if not slack_enabled:
        return
    
    try:
        message = f"*[{alert['level']}] {alert['type']} Alert*\n{alert['message']}\nTime: {alert['time']}\nServer: {metrics['hostname']}"
        
        data = {
            'channel': slack_channel,
            'username': slack_username,
            'text': message
        }
        
        response = requests.post(slack_webhook, json=data)
        
        if response.status_code == 200:
            print("Slack  message sent")
        else:
            print("Slack message failed")
    except:
        print("Slack message failed")

def send_notifications(alert, metrics) :
    load_notification_config()  
    send_email(alert, metrics)
    send_slack(alert, metrics )
