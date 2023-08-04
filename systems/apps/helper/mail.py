import smtplib
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader, select_autoescape, PackageLoader

try:
    from config import config
except:
    try:
        import sys
        sys.path.append('../..')
        from config import config
    except:
        raise "Email Services Failed to Start"

class Mail:
    def __init__(self):
        pass
        
    def send_email(self, subject, sender_mail, recipient_mail, sender_password, template, **kwargs):
        """Sends an email using a template."""
        env = Environment(
            loader= FileSystemLoader(searchpath="apps/static/mail_content"),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template(template)
        
        body = template.render(**kwargs)
        msg = MIMEText(body, 'html')
        msg['Subject'] = subject
        msg['From'] = sender_mail
        msg['To'] = recipient_mail # ', '.join(recipient_mails)
        
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(sender_mail, sender_password)
        smtp_server.sendmail(sender_mail, recipient_mail, msg.as_string())
        smtp_server.quit()
        
    def newsletter_mail(self, title="", content="", recepient_mails=[], source_url="", image_thumbnail=""):
        subject = "Surat Untukmu: "+ title # —
        content = content[:300]+"..."
        
        for rm in recepient_mails:
            self.send_email(
                template='newsletter_body.html',
                subject=subject,
                sender_mail=config.NEWSLETTER_EMAIL_ADDR,
                sender_password=config.NEWSLETTER_EMAIL_PWD,
                recipient_mail=rm,
                
                title=title,
                image_thumbnail=image_thumbnail,
                content_body=content,
                source_url=source_url
            )
    
    def reset_password_mail(self, name="", recepient_mail="", redirect_url=""):
        subject = "Bhinneka App — Permintaan Lupa Password" # —
        
        self.send_email(
            template='reset_password_body.html',
            subject=subject,
            sender_mail=config.NOREPLY_EMAIL_ADDR,
            sender_password=config.NOREPLY_EMAIL_PWD,
            recipient_mail=recepient_mail,
            
            redirect_url=redirect_url,
            requested_user=name
        )
    
    def account_confirmation_mail(self, name="", recepient_mail="", redirect_url=""):
        subject = "Bhinneka App — Konfirmasi Email" # —
        
        self.send_email(
            template='email_confirm_body.html',
            subject=subject,
            sender_mail=config.NOREPLY_EMAIL_ADDR,
            sender_password=config.NOREPLY_EMAIL_PWD,
            recipient_mail=recepient_mail,
            
            redirect_url=redirect_url,
            requested_user=name
        )

if __name__ == "__main__":
    mail = Mail()
    mail.newsletter_mail(
            title="Pelestarian Bahasa Daerah Harus Konsisten Dilakukan demi Budaya Bangsa",
            content="Jakarta - Wakil Ketua MPR RI Lestari Moerdijat mengatakan keragaman bahasa daerah sebagai bagian dari budaya harus terus ditingkatkan melalui berbagai upaya pelestarian. Hal ini dilakukan demi mewujudkan ketahanan budaya bangsa. \"Upaya pelestarian bahasa daerah sebagai bagian dari identitas bangsa Indonesia harus menjadi kepedulian kita bersama,\" kata Wakil Ketua MPR RI, Lestari Moerdijat dalam keterangannya, Kamis (27/4/2023).",
            recepient_mails=["hujankopimalam@gmail.com"],
            source_url="https://news.detik.com/berita/d-6692686/pelestarian-bahasa-daerah-harus-konsisten-dilakukan-demi-budaya-bangsa",
            image_thumbnail="https://akcdn.detik.net.id/community/media/visual/2022/11/02/wakil-ketua-mpr-ri-lestari-moerdijat.jpeg?w=700&q=90"
        )