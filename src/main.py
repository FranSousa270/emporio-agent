from src.agent.agent import Agent
from src.repositories.csv_repository import load_all_csv


def main():

    agent = Agent()

    try:
        print("\nAssistente virtual do Empório da Música")
        print("Digite 'sair' para encerrar.\n")

        while True:
            message = input("Você: ").strip()

            if message.lower() == "sair":
                break

            if not message:
                continue

            response = agent.respond(message)
            print(f"\nAssistente: {response}\n")

    finally:
        agent.close()


if __name__ == "__main__":
    main()
