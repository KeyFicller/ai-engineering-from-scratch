import os
import json
import urllib.request


def call_with_sdk():
    try:
        import openai
    except ImportError:
        print("Install the SDK: pip install openai")
        return

    client = openai.OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": "What is a neural network in one sentence?"}])
    print(f"SDK response: {response.choices[0].message.content}")
    print(f"Tokens used: {response.usage.prompt_tokens} in, {response.usage.completion_tokens} out")


def call_raw_http():
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("Set DEEPSEEK_API_KEY environment variable first")
        return

    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
    }
    body = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "What is a neural network in one sentence?"}],
    }).encode()

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
        print(f"Raw HTTP response: {result['choices'][0]['message']['content']}")
        print(f"Tokens used: {result['usage']['prompt_tokens']} in, {result['usage']['completion_tokens']} out")


if __name__ == "__main__":
    print("=== API Calls ===\n")
    print("1. Using the SDK:")
    call_with_sdk()
    print("\n2. Using raw HTTP:")
    call_raw_http()
