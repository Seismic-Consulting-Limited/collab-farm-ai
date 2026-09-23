from app.chatbot.chatbot import chat


def start_chat():

    print("================================")
    print("   CollabFarm AI Assistant")
    print("   Type 'exit' to quit")
    print("================================")


    session_id = "local_test_session"


    while True:

        user_input = input("\nYou: ")


        if user_input.lower() == "exit":
            print("Goodbye!")
            break


        response = chat(
            user_input,
            session_id
        )


        print("\nAssistant:")
        print(response["answer"])


if __name__ == "__main__":
    start_chat()