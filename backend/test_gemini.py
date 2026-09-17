from ai.gemini_service import ask_gemini


def main():
    question = "What is financial distress in simple terms?"

    try:
        response = ask_gemini(question)

        print("\n========================================")
        print("BTIP GEMINI TEST")
        print("========================================")
        print("\nQuestion:")
        print(question)

        print("\nGemini Response:")
        print(response)

        print("\n========================================")
        print("Gemini connection successful!")
        print("========================================\n")

    except Exception as exc:
        print("\n========================================")
        print("GEMINI TEST FAILED")
        print("========================================")
        print(f"\nError: {exc}")
        print()


if __name__ == "__main__":
    main()