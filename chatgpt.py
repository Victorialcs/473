from openai import OpenAI
import os

def get_chatgpt_response(prompt_text):
    #os.environ["OPENAI_API_KEY"] = "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"
    api_key = "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"
    client = OpenAI(api_key=api_key)

    # Sending a prompt to ChatGPT
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Adjust the model name based on availability
        messages=[{"role": "system", "content": "You are a smart thing. Please work."}, {"role": "user", "content": prompt_text}]
    )
    if response.choices:
        return(response.choices[0].message.content.strip())
    else:
        print("ERROR ERROR ERROR NO MESSAGE FOUND")
        # Extracting the text from the response

# Example usage
prompt = "Hello, how are you?"
output = get_chatgpt_response(prompt)
print(output)
