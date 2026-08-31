"""Gradio interface for the three chatbot assignment stages."""

from __future__ import annotations

import html
import os
from typing import Any

import gradio as gr

from src.adaptive_llm_portfolio.chat_engine import (
    ADAPTIVE_MODE,
    OPENAI_MODE,
    TRADITIONAL_MODE,
    ChatEngine,
)

CSS = (
    ".hero {padding: 1.1rem 1.25rem; border-radius: 18px; "
    "background: linear-gradient(135deg, #eef2ff, #ecfeff); "
    "border: 1px solid #c7d2fe;}\n"
    ".hero h1 {margin: 0 0 .3rem 0; color: #312e81;}\n"
    ".status-card {padding: .8rem 1rem; border-radius: 14px; "
    "border: 1px solid #cbd5e1; background: #f8fafc;}\n"
    ".status-card strong {color: #312e81;}\n"
    ".mode-note {font-size: .9rem; color: #475569;}"
)
THEME = gr.themes.Soft(primary_hue="indigo", neutral_hue="slate")


def render_status(mode: str, context: Any, live_openai: bool) -> str:
    service = "Live OpenAI" if live_openai else "Offline demonstration"
    color = {"Positive": "#166534", "Needs support": "#9a3412"}.get(context.sentiment, "#334155")
    return (
        '<div class="status-card">'
        f"<strong>Mode:</strong> {html.escape(mode)} &nbsp; | &nbsp; "
        f"<strong>Service:</strong> {service}<br>"
        f"<span style='color:{color}'><strong>Adaptation signal:</strong> "
        f"{html.escape(context.language)}, {html.escape(context.sentiment)}, "
        f"{html.escape(context.urgency)} urgency, "
        f"{html.escape(context.response_density)} response.</span>"
        "</div>"
    )


def create_demo(engine: ChatEngine | None = None) -> gr.Blocks:
    engine = engine or ChatEngine()

    def respond(message: str, history: list[dict[str, Any]] | None, mode: str):
        clean_message = (message or "").strip()
        if not clean_message:
            return history or [], "", "Please enter a message."
        reply, context = engine.reply(clean_message, history, mode)
        updated = list(history or [])
        updated.extend(
            [
                {"role": "user", "content": clean_message},
                {"role": "assistant", "content": reply},
            ]
        )
        return updated, "", render_status(mode, context, engine.openai_service.available)

    with gr.Blocks(title="Adaptive LLM Learning Lab") as demo:
        gr.HTML(
            "<div class='hero'><h1>Adaptive LLM Learning Lab</h1>"
            "<p>Compare a rule-based chatbot with an OpenAI model and an adaptive "
            "human-computer interaction mode.</p></div>"
        )
        with gr.Row():
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    height=430,
                    label="Conversation",
                    placeholder="Ask about setup, GitHub, the assignment, or an LLM concept.",
                )
                message = gr.Textbox(
                    label="Message",
                    placeholder="Example: I am stuck and need a brief setup plan today.",
                    lines=2,
                )
                with gr.Row():
                    send = gr.Button("Send", variant="primary")
                    clear = gr.Button("Clear")
            with gr.Column(scale=2):
                mode = gr.Radio(
                    [TRADITIONAL_MODE, OPENAI_MODE, ADAPTIVE_MODE],
                    value=TRADITIONAL_MODE,
                    label="Chatbot stage",
                )
                gr.Markdown(
                    "**How to compare the stages**\n\n"
                    "1. Traditional rules: deterministic intent matching.\n"
                    "2. OpenAI LLM: contextual model response.\n"
                    "3. Adaptive OpenAI: language, sentiment, urgency, and density "
                    "guide the response."
                )
                status = gr.HTML(
                    "<div class='status-card'><strong>Ready.</strong> "
                    "Choose a mode and send a message.</div>"
                )
                gr.Examples(
                    examples=[
                        ["How do I set up the Python environment?"],
                        ["I am frustrated and need a short plan before today's deadline."],
                        ["Hola, necesito ayuda con la tarea."],
                    ],
                    inputs=[message],
                    label="Try an example",
                )

        send.click(respond, [message, chatbot, mode], [chatbot, message, status])
        message.submit(respond, [message, chatbot, mode], [chatbot, message, status])
        clear.click(
            lambda: (
                [],
                "",
                "<div class='status-card'><strong>Cleared.</strong></div>",
            ),
            None,
            [chatbot, message, status],
        )
    return demo


demo = create_demo()


if __name__ == "__main__":
    port = int(os.getenv("APP_PORT", "7860"))
    demo.launch(
        server_name="127.0.0.1",
        server_port=port,
        show_error=True,
        theme=THEME,
        css=CSS,
    )
