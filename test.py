import re
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP

class CustomSMTPHandler:
    def __init__(self):
        self.blocked_domains = self.load_blocked_domains()

    def load_blocked_domains(self):
        with open("block.txt") as file:
            return [line.strip() for line in file]

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        for recipient in address:
            domain = recipient.split('@')[-1]
            if self.is_blocked_domain(domain):
                print(f"Blocked email from {envelope.mail_from} to {recipient}")
                return '550 Blocked'

    def handle_DATA(self, server, session, envelope):
        # Process the message if not blocked
        print(f"Received email from {envelope.mail_from} to {envelope.rcpt_tos}")

        # Additional processing logic
        for line in envelope.content.decode().split("\n"):
            if line.startswith("Subject:"):
                subject = line[9:].strip()
                print(f"Subject: {subject}")
                # Add your processing logic here

    def is_blocked_domain(self, domain):
        if domain.endswith(".in"):
            return True

        for blocked_domain in self.blocked_domains:
            if re.match(blocked_domain, domain):
                return True

        return False

# Run the server on localhost:1025
handler = CustomSMTPHandler()
controller = Controller(handler, port=1025)
print("SMTP server proxy is running...")
controller.start()
