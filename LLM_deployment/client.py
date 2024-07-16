import requests
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("./app/Qwen2-1.5B-Instruct-bnb-4bit")


def send_request(host, port, text):
    url = f"http://{host}:{port}/"
    data = text
    response = requests.post(url, data=data, stream=True)
    return response


def generate_word(conv: list, input_text: str):
    conv.append(dict(role="user", content=input_text))

    chat = tokenizer.apply_chat_template(
        conv, tokenize=False, add_generation_prompt=True
    )

    generated_text = ""
    response = send_request(host="172.16.222.235", port="80", text=chat)
    for chunk in response.iter_content(None):
        new_text = chunk.decode("utf-8")
        yield new_text
        generated_text += new_text

    conv.append(dict(role="assistant", content=generated_text))


conv = []

while True:
    input_text = input("INPUT: ")
    for word in generate_word(conv, input_text):
        print(word, end="", flush=True)
        # pass
    print()
