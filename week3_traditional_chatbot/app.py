"""Gradio interface for the standalone Week 3 traditional chatbot."""

from __future__ import annotations

import os

import gradio as gr
from chatbot import reply


def respond(message: str, history: list[dict] | None) -> tuple[list[dict], str]:
    """Add one user and assistant exchange to the chat history."""

    clean = (message or "").strip()
    answer = reply(message)
    updated = list(history or [])
    if clean:
        updated.append({"role": "user", "content": clean})
    updated.append({"role": "assistant", "content": answer})
    return updated, ""


def create_demo() -> gr.Blocks:
    with gr.Blocks(title="Week 3 Traditional Chatbot") as demo:
        gr.Markdown(
            "# Week 3 Traditional Chatbot\n"
            "This prototype uses fixed rules and keyword matching. It does not use an LLM."
        )
        chatbot = gr.Chatbot(
            label="Conversation",
            height=430,
            placeholder="Ask what the bot can do, or ask about setup, testing, or the assignment.",
        )
        message = gr.Textbox(
            label="Message",
            placeholder="What can you do?",
            lines=2,
            max_lines=4,
        )
        with gr.Row():
            send = gr.Button("Send", variant="primary")
            clear = gr.Button("Clear")

        gr.Examples(
            examples=[
                ["What can you do?"],
                ["What is required for the assignment?"],
                ["How do I test the chatbot?"],
                ["I am stuck with a setup error."],
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
