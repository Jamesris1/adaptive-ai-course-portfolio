"""Gradio interface for the Week 3 Azure AI Language chatbot."""

from __future__ import annotations

import os

import gradio as gr

try:
    from .azure_chatbot import reply
    from .azure_service import AzureSentimentService
except ImportError:  # Support direct execution with `python app.py`.
    from azure_chatbot import reply
    from azure_service import AzureSentimentService

SERVICE = AzureSentimentService()


def respond(message: str, history: list[dict] | None) -> tuple[list[dict], str]:
    clean = (message or "").strip()
    answer = reply(message, SERVICE)
    updated = list(history or [])
    if clean:
        updated.append({"role": "user", "content": clean})
    updated.append({"role": "assistant", "content": answer})
    return updated, ""


def create_demo() -> gr.Blocks:
    status = "Configured" if SERVICE.available else "Not configured"
    with gr.Blocks(title="Week 3 Azure AI Language Chatbot") as demo:
        gr.Markdown(
            "# Week 3 Azure AI Language Chatbot\n"
            "A traditional course-support chatbot extended with Azure sentiment analysis.\n\n"
            f"**Azure connection:** {status}"
        )
        chatbot = gr.Chatbot(
            label="Conversation",
            height=430,
            placeholder="Enter a short question or statement.",
        )
        message = gr.Textbox(
            label="Message",
            placeholder="I am excited that the chatbot is working.",
            lines=2,
            max_lines=4,
        )
        with gr.Row():
            send = gr.Button("Send", variant="primary")
            clear = gr.Button("Clear")
        gr.Examples(
            examples=[
                ["What can you do?"],
                ["I am excited that the chatbot is working."],
                ["This setup is frustrating and difficult."],
                ["The assignment is due this week."],
            ],
            inputs=message,
        )

        send.click(respond, [message, chatbot], [chatbot, message])
        message.submit(respond, [message, chatbot], [chatbot, message])
        clear.click(lambda: ([], ""), None, [chatbot, message])
    return demo


demo = create_demo()


if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=int(os.getenv("APP_PORT", "7860")),
        show_error=True,
    )
