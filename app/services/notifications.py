from __future__ import annotations


class AirbnbAIBrain:
    EMERGENCY_KEYWORDS = [
        "fire",
        "smoke",
        "gas",
        "leak",
        "flood",
        "water leak",
        "no electricity",
        "power outage",
        "security",
        "unsafe",
        "locked out",
    ]
    MAINTENANCE_KEYWORDS = [
        "ac",
        "heating",
        "wifi",
        "internet",
        "hvac",
        "lock",
        "door",
        "window",
        "plumbing",
        "shower",
        "toilet",
        "appliance",
        "kitchen",
        "washer",
        "dryer",
        "hot water",
    ]
    SERVICE_KEYWORDS = [
        "check in",
        "check-in",
        "check out",
        "checkout",
        "parking",
        "key",
        "instructions",
        "arrival",
        "late checkout",
        "guest access",
    ]

    def classify_intent(self, message: str) -> dict[str, str]:
        text = message.lower()

        if any(keyword in text for keyword in self.EMERGENCY_KEYWORDS):
            return {"intent": "emergency", "urgency": "high"}
        if any(keyword in text for keyword in self.MAINTENANCE_KEYWORDS):
            return {"intent": "maintenance", "urgency": "medium"}
        if any(keyword in text for keyword in self.SERVICE_KEYWORDS):
            return {"intent": "guest_service", "urgency": "low"}

        return {"intent": "general", "urgency": "low"}

    def generate_response(self, intent: str, guest_name: str | None = None, listing_name: str | None = None) -> str:
        guest_prefix = f"Hi {guest_name}, " if guest_name else ""

        if intent == "emergency":
            return (
                f"{guest_prefix}We are sorry you are experiencing this. Our team is escalating the issue immediately and "
                "we will coordinate the fastest response for the property. Please stay safe and share any photos or urgent details."
            )
        if intent == "maintenance":
            return (
                f"{guest_prefix}Thank you for reporting this. We are creating a maintenance ticket and will contact the right contractor "
                f"for {listing_name or 'your property'} as soon as possible."
            )
        if intent == "guest_service":
            return (
                f"{guest_prefix}Thanks for your message. We are checking the property details and will get you the right answer as quickly as possible."
            )
        return (
            f"{guest_prefix}Thanks for reaching out. We have received your message and our team will review it shortly."
        )

    def triage_message(self, message: str, guest_name: str | None = None, listing_name: str | None = None) -> dict[str, str | bool]:
        classification = self.classify_intent(message)
        intent = classification["intent"]
        urgency = classification["urgency"]
        requires_work_order = intent in {"emergency", "maintenance"}

        return {
            "intent": intent,
            "urgency": urgency,
            "response": self.generate_response(intent, guest_name, listing_name),
            "requires_work_order": requires_work_order,
        }
