import json, re, random, datetime
from typing import Dict, Any, List

class Chatbot:
    def __init__(self, rules_path: str = "rules.json"):
        with open(rules_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.company = data.get("company", {})
        self.intents = data.get("intents", [])
        self.fallbacks = data.get("fallbacks", ["Sorry, I didn't understand."])

        # Pre-compile intent patterns
        self._compiled = []
        for intent in self.intents:
            compiled_patterns = [re.compile(p, re.I) for p in intent.get("patterns", [])]
            self._compiled.append({"intent": intent, "patterns": compiled_patterns})

    def _extract_order_id(self, text: str):
        # Match 6 to 10 digits with optional "order" / "ord" prefix
        m = re.search(r"(?:\\bord(?:er)?\\s*#?\\s*)?(\\d{6,10})\\b", text, re.I)
        if m:
            return m.group(1)
        return None

    def _handle_order_status(self, text: str) -> str:
        order_id = self._extract_order_id(text)
        if not order_id:
            return "Please share your 6–10 digit Order ID (e.g., ORD 123456) to check the status."
        # Deterministic fake status based on order id
        states = ["Processing", "Packed", "Dispatched", "Out for Delivery", "Delivered"]
        idx = sum(ord(c) for c in order_id) % len(states)
        status = states[idx]
        # ETA heuristic
        days = (sum(int(c) for c in order_id if c.isdigit()) % 5) + 1
        eta = (datetime.date.today() + datetime.timedelta(days=days)).strftime("%b %d, %Y")
        return f"Order #{order_id}: {status}. Estimated date: {eta}. Need anything else?"

    def _format(self, text: str) -> str:
        # Replace placeholders with company info, if any
        try:
            return text.format(**self.company)
        except Exception:
            return text

    def respond(self, text: str, state: Dict[str, Any] | None = None) -> Dict[str, Any]:
        if state is None:
            state = {}
        normalized = text.strip()
        if not normalized:
            return {"reply": random.choice(self.fallbacks), "state": state}

        # Score intents by number of pattern matches
        best = None
        best_score = 0
        for entry in self._compiled:
            score = 0
            for pat in entry["patterns"]:
                if pat.search(normalized):
                    score += 1
            if score > best_score:
                best_score = score
                best = entry["intent"]

        if best:
            name = best.get("name")
            if name == "order_status":
                reply = self._handle_order_status(normalized)
                return {"reply": reply, "state": state}
            responses = best.get("responses", [])
            if responses:
                reply = self._format(random.choice(responses))
                return {"reply": reply, "state": state}

        # Fallback
        return {"reply": random.choice(self.fallbacks), "state": state}


if __name__ == "__main__":
    bot = Chatbot()
    print("RuleBot ready. Type 'exit' to quit.")
    while True:
        try:
            msg = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break
        if msg.lower() in {"exit", "quit"}:
            print("Bye!")
            break
        print("Bot:", bot.respond(msg)["reply"])
