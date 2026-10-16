
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"

AVAILABLE_MODELS = {
    "Gemma": "gemma3:1b",
    "Llama": "llama3.2",
}


def analyze_job_offer(job_text, model_name):
    if model_name not in AVAILABLE_MODELS:
        raise ValueError("Choose Gemma or Llama.")

    payload = {
        "model": AVAILABLE_MODELS[model_name],
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an AI job offer safety assistant. "
                    "Identify possible warning signs such as upfront fees, "
                    "unrealistic salaries, pressure tactics, and requests "
                    "for passwords or banking details. Explain your reasons "
                    "in simple English. Suggest safe verification steps. "
                    "Never claim a job is definitely fake based only on text."
                ),
            },
            {
                "role": "user",
                "content": job_text,
            },
        ],
        "stream": False,
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=180,
    )
    response.raise_for_status()

    return response.json()["message"]["content"]
