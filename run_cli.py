from engine import Chatbot

def main():
    bot = Chatbot()
    print("NovaMobiles Support Bot (rule-based)")
    print("Type 'exit' to quit.\n")
    while True:
        try:
            msg = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break
        if msg.lower() in {"exit", "quit"}:
            print("Bye!")
            break
        resp = bot.respond(msg)
        print("Bot:", resp["reply"])

if __name__ == "__main__":
    main()
