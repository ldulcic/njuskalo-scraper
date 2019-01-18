import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def parse_urls_file(path):
    return [url.strip() for url in open(path) if url]


def parse_mail_config():
    config = {}
    for line in open('mail.config'):
        if line:
            parts = line.strip().split('=')
            config[parts[0].strip()] = parts[1].strip()
    return config


class MailSender:

    def __init__(self):
        config = parse_mail_config()
        self.MAIL_HOST = config['MAIL_HOST']
        self.MAIL_PORT = config['MAIL_PORT']
        self.MAIL_USER = config['MAIL_USER']
        self.MAIL_PASS = config['MAIL_PASS']
        self.MAIL_RECIPIENT = config['MAIL_RECIPIENT']

    def send_email(self, items):
        assert len(items) > 0
        msg = MIMEMultipart()
        msg['From'] = self.MAIL_USER
        msg['To'] = self.MAIL_RECIPIENT
        msg['Subject'] = 'Novi stan!' if len(items) == 1 else 'Novi stanovi!'

        ads_strings = map(lambda ad: "<a href=\"%s\">%s</a><br>%s<br>%s€<br>" % (ad['link'], ad['title'], ad['description'], ad['price']), items)
        body = """
        %s
        
        <br><br>
        Iiiiiiiiiiiiiiddiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii !!!!!!!!!!!
        """ % ('<br>'.join(ads_strings))
        msg.attach(MIMEText(body, 'html'))

        mail_server = smtplib.SMTP(self.MAIL_HOST, self.MAIL_PORT)
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.ehlo()
        mail_server.login(self.MAIL_USER, self.MAIL_PASS)
        mail_server.sendmail(self.MAIL_USER, self.MAIL_RECIPIENT, msg.as_string())
        mail_server.close()

