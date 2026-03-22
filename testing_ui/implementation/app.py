import gradio as gr
from dotenv import load_dotenv
import os 

from answer import answer_question

load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")
print(api_key)

def format_context(context):
    result = "<h2 style='color: #ff7800;'>Relevant Context</h2>\n\n"
    for doc in context:
        result += f"<span style='color: #ff7800;'>Source: {doc.metadata['source']}</span>\n\n"
        result += doc.page_content + "\n\n"
    return result


def chat(history):
    last_message = history[-1]["content"]
    prior = history[:-1]
    answer, context = answer_question(last_message, prior)
    history.append({"role": "assistant", "content": answer})
    return history, format_context(context)

# --------- Navigation ----------
def go_to_chat():
    return gr.update(visible=False), gr.update(visible=True)

def go_home():
    return gr.update(visible=True), gr.update(visible=False)

def put_message_in_chatbot(message, history):
    return "", history + [{"role": "user", "content": message}]
# def main():
#     def put_message_in_chatbot(message, history):
#         return "", history + [{"role": "user", "content": message}]

#     # theme = gr.themes.Soft(font=["Inter", "system-ui", "sans-serif"])

#     with gr.Blocks(title="Trinity Helper Assistant") as ui:
#         gr.Markdown("# 🏢 Trinity Helper Assistant\nAsk me anything about Trinity!")

#         with gr.Row():
#             with gr.Column(scale=1):
#                 chatbot = gr.Chatbot(
#                     label="💬 Conversation", height=600, type="messages", show_copy_button=True
#                 )
#                 message = gr.Textbox(
#                     label="Your Question",
#                     placeholder="Ask anything about Trinity...",
#                     show_label=False,
#                 )

#             with gr.Column(scale=1):
#                 context_markdown = gr.Markdown(
#                     label="📚 Retrieved Context",
#                     value="*Retrieved context will appear here*",
#                     container=True,
#                     height=600,
#                 )

#         message.submit(
#             put_message_in_chatbot, inputs=[message, chatbot], outputs=[message, chatbot]
#         ).then(chat, inputs=chatbot, outputs=[chatbot, context_markdown])

#     ui.launch(inbrowser=True,share=True)

# if __name__ == "__main__":
#     main()

# --------- UI ----------
with gr.Blocks(title="Team Portal") as demo:

    # ---------- HOME PAGE ----------
    with gr.Column(visible=True) as home_page:
        gr.Markdown(
            """
            <div style="text-align:center; margin-top:60px;">
                <h1>🚀 Trinity Portal</h1>
                <p>Select your team</p>
            </div>
            """
        )

        with gr.Row(equal_height=True):
            gr.HTML("""
            <div style="display:flex; justify-content:center; gap:40px; margin-top:40px;">
            """)
            dev_btn = gr.Button("👨‍💻 Developer", size="lg")
            prod_btn = gr.Button("📦 Product Team", size="lg")
            gr.HTML("</div>")

    # ---------- CHATBOT PAGE ----------
    with gr.Column(visible=False) as chat_page:
        gr.Markdown("# 🏢 Trinity Helper Assistant\nAsk me anything about Trinity!")

        with gr.Row():
            with gr.Column(scale=1):
                chatbot = gr.Chatbot(
                    label="💬 Conversation",
                    height=600,
                    type="messages",
                    show_copy_button=True,
                )
                message = gr.Textbox(
                    label="Your Question",
                    placeholder="Ask anything about Trinity...",
                    show_label=False,
                )

            with gr.Column(scale=1):
                context_markdown = gr.Markdown(
                    value="*📚 Retrieved context will appear here*",
                    container=True,
                    height=600,
                )

        back_btn = gr.Button("⬅ Back to Home")

        # Chat flow
        message.submit(
            put_message_in_chatbot,
            inputs=[message, chatbot],
            outputs=[message, chatbot],
        ).then(
            chat,
            inputs=chatbot,
            outputs=[chatbot, context_markdown],
        )

    # ---------- Actions ----------
    dev_btn.click(fn=go_to_chat, outputs=[home_page, chat_page])
    prod_btn.click(fn=go_to_chat, outputs=[home_page, chat_page])
    back_btn.click(fn=go_home, outputs=[home_page, chat_page])

demo.launch(inbrowser=True, share=True)
