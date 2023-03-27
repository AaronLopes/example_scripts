import openai

openai.api_key = "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" # Replace YOUR_API_KEY with your actual API key

def generate_response(prompt):
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "user", "content": prompt},
        ],
        temperature = 0.7
    )
    return response.choices[0].message['content']

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit chat":
        break
    response = generate_response(user_input)
    print("ChatGPT: " + str(response))