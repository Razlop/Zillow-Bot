import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def answer_question():
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="I have this house, can you tell me about it, 978 Monterey Ln, Rochester Hills, MI 48307	549900	5	4	2877	SINGLE_FAMILY	191.1366006",
        temperature=0.7,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=1
    )

    # Extract the answer from the response
    answer = response.choices[0].text.strip()

    # Print the answer to the terminal
    print(answer)

# Call the answer_question function to print the answer
answer_question()
