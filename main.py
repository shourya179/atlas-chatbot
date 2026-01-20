from core.bot import chatbot

def run():
    bot = chatbot("Atlas")
    bot.memory.load()

    print("Atlas is online. Type 'exit' to quit.\n")

    while True:
        user_input = input("you").strip()

        if user_input.lower in ("exit","quit"):
            bot.memory.save()
            print("Atsal : Session saved. Goodbye.")
            break
        responce = bot.handle(user_input)
        print(f"Atsal :{responce}")

        bot.memory.save()
if __name__ == "__main__":
    run()