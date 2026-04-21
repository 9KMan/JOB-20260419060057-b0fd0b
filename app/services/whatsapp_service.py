import os
from twilio.rest import Client

class WhatsAppService:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_number = os.getenv("TWILIO_WHATSAPP_FROM")
        self.twilio_client = None
        if self.account_sid and self.auth_token:
            self.twilio_client = Client(self.account_sid, self.auth_token)

    def send_reward_message(self, to_phone, customer_name=""):
        name_greeting = f" {customer_name}" if customer_name else ""
        message_body = (
            f"🎉 Congratulations{name_greeting}! "
            f"You've earned a FREE car wash! "
            f"Present this message on your next visit to claim your reward. "
            f"Thank you for your loyalty!"
        )
        return self._send_whatsapp(to_phone, message_body)

    def send_redeem_confirmation(self, to_phone, customer_name=""):
        name_greeting = f" {customer_name}" if customer_name else ""
        message_body = (
            f"✅ Your reward has been redeemed{name_greeting}! "
            f"We look forward to seeing you soon for your FREE car wash. "
            f"Thank you for choosing us!"
        )
        return self._send_whatsapp(to_phone, message_body)

    def send_visit_confirmation(self, to_phone, visit_count, customer_name=""):
        name_greeting = f" {customer_name}" if customer_name else ""
        visits_until_reward = 10 - (visit_count % 10)
        message_body = (
            f"📝 Your visit has been recorded{name_greeting}! "
            f"Visit #{visit_count} complete. "
            f"Only {visits_until_reward} more visits until your next FREE wash! 🎁"
        )
        return self._send_whatsapp(to_phone, message_body)

    def _send_whatsapp(self, to_phone, body):
        try:
            if not self.twilio_client or not self.from_number:
                print(f"[WhatsApp Mock] To: {to_phone} | Message: {body}")
                return {"status": "mock", "to": to_phone, "body": body}

            message = self.twilio_client.messages.create(
                body=body,
                from_=self.from_number,
                to=f"whatsapp:{to_phone}"
            )
            return {"status": "sent", "sid": message.sid}
        except Exception as e:
            print(f"[WhatsApp Error] {str(e)}")
            return {"status": "error", "error": str(e)}