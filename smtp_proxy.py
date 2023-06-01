import asyncio
from aiosmtpd.controller import Controller
import re
import smtplib
class MySMTPProxyHandler:
    def __init__(self):
        self.spam_domains = self.load_spam_domains()

    def load_spam_domains(self):
        with open("block.txt", "r") as file:
            return [line.strip() for line in file]

    async def handle_DATA(self, server, session, envelope):
        mail_from = envelope.mail_from
        sender_domain = re.split('@', mail_from)[-1]
        
        if sender_domain in self.spam_domains or re.search(r"\.in$", sender_domain):
            print(f"Blocked email from {mail_from}")
        else:
            print(f"Forwarding email from {mail_from}")
            await self.forward_email(envelope)

    async def forward_email(self, envelope):
        # Extract necessary information from the envelope
        mail_from = envelope.mail_from
        rcpt_tos = envelope.rcpt_tos
        data = envelope.content.decode('utf-8')
        
        # Define the SMTP server details for forwarding
        smtp_host = 'smtp.gmail.com'
        smtp_port = 25
        
        # Connect to the SMTP server
        try:
            smtp_client = smtplib.SMTP(smtp_host, smtp_port)
            
            # Send the email
            smtp_client.sendmail(mail_from, rcpt_tos, data)
            
            # Close the connection
            smtp_client.quit()
            
            print("Email forwarded successfully.")
        except Exception as e:
            print(f"Failed to forward email: {str(e)}")

controller = Controller(MySMTPProxyHandler(), hostname='localhost', port=1025)
controller.start()
print("Proxy server started on localhost:1025")

try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    pass
finally:
    controller.stop()
