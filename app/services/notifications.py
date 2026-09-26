from __future__ import annotations


class NotificationService:
    def __init__(self, twilio_client=None, sendgrid_client=None):
        self.twilio_client = twilio_client
        self.sendgrid_client = sendgrid_client

    def send_guest_sms(self, phone_number: str | None, message: str) -> dict:
        if not phone_number:
            return {"status": "skipped", "reason": "no_phone_number"}
        if self.twilio_client is None:
            return {"status": "simulated", "recipient": phone_number, "message": message}
        return {"status": "sent", "recipient": phone_number, "message": message}

    def send_host_alert(self, message: str) -> dict:
        if self.sendgrid_client is None:
            return {"status": "simulated", "message": message}
        return {"status": "sent", "message": message}
