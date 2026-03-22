import streamlit as st
from implementation.answer import answer_question
from feedback import insert_feedback,get_feedback_data

# ---------- Page Config ----------
st.set_page_config(
    page_title="Trinity AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# # ---------- Custom CSS ----------
# st.markdown("""
# <style>
# .chat-scroll-area {
#     height: 62vh;
#     overflow-y: auto;
#     padding: 10px 4px 60px 4px;
# }

# .fixed-input {
#     position: fixed;
#     bottom: 80px;
#     left: 0;
#     right: 0;
#     max-width: 1100px;
#     margin: auto;
#     background: var(--background-color);
#     padding-top: 10px;
# }

# .fixed-footer {
#     position: fixed;
#     bottom: 10px;
#     left: 0;
#     right: 0;
#     max-width: 1100px;
#     margin: auto;
#     background: var(--background-color);
# }
# </style>
# """, unsafe_allow_html=True)


# ---------- Chat Logic ----------
def process_chat(role):
    history = st.session_state.chat_history
    last_message = history[-1]["content"]
    prior = history[:-1]

    answer, _ = answer_question(last_message, prior, role=role)

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": answer
    })


def init_chat_state(role):
    chat_key = f"chat_history_{role}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = []
    return chat_key


def render_chat(role):
    
    chat_key = init_chat_state(role)
    history = st.session_state[chat_key]

    tab_chat, tab_analytics = st.tabs(["💬 Assistant", "📊 Analytics"])

    # ================= TAB 1 — CHAT =================
    with tab_chat:

        # ----- Messages (Scrollable) -----
        st.markdown(
            f"""
            <div style="text-align:center;">
                <div style="font-size:28px; font-weight:bold;">🏢 Trinity AI Assistant</div>
                <div style="font-size:18px;">Team: {role.capitalize()}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown('<div class="chat-scroll-area">', unsafe_allow_html=True)


        for i, msg in enumerate(history):

            feedback_key = f"feedback_done_{i}"
            if feedback_key not in st.session_state:
                st.session_state[feedback_key] = False
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

                if msg["role"] == "assistant":
                    question = history[i-1]["content"]
                    col1, col2, col3 = st.columns([1,1,6])
                    with col1:
                        if not st.session_state[feedback_key]:
                            if st.button("👍", key=f"like_{i}"):
                                insert_feedback(question, "like", role)
                                st.session_state[feedback_key] = True
                                st.toast("👍 Feedback saved!")
                                st.rerun()
                    with col2:
                        if not st.session_state[feedback_key]:
                            if st.button("👎", key=f"dislike_{i}"):
                                # st.session_state.feedback.append("dislike")
                                insert_feedback(question, "dislike", role)
                                st.session_state[feedback_key] = True
                                st.toast("Feedback saved!")
                                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


        # ----- Fixed Input (Bottom) -----
        st.markdown('<div class="fixed-input">', unsafe_allow_html=True)

        #----- Input -----
        user_input = st.chat_input("Ask anything about Trinity...")
        st.markdown('</div>', unsafe_allow_html=True)


        # if user_input:
        #     history.append({"role": "user", "content": user_input})

        #     last_message = history[-1]["content"]
        #     prior = history[:-1]

        #     answer, _ = answer_question(last_message, prior, role=role)
        #     history.append({"role": "assistant", "content": answer})

        #     st.rerun()
        if user_input:
            
            history.append({"role": "user", "content": user_input})

            # ✅ Immediately render the new user message
            with st.chat_message("user"):
                st.markdown(user_input)

            # ✅ Show spinner while LLM is working
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    last_message = user_input
                    prior = history[:-1]
                    answer, _ = answer_question(last_message, prior, role=role)
                    st.markdown(answer)

            history.append({"role": "assistant", "content": answer})
            st.rerun()

        st.divider()
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.switch_page("login_page.py")

    with tab_analytics:

        st.subheader("User Feedback Analytics")

        totals_df, trend_df, model_df = get_feedback_data(st.session_state.role)

        if totals_df.empty:
            st.info("No feedback yet.")
            st.stop()

        # ================= METRICS =================
        likes = int(totals_df.loc[totals_df["name"]=="like","count"].sum())
        dislikes = int(totals_df.loc[totals_df["name"]=="dislike","count"].sum())
        total = likes + dislikes

        col1, col2, col3 = st.columns(3)
        col1.metric("👍 Likes", likes)
        col2.metric("👎 Dislikes", dislikes)
        col3.metric("📊 Total Feedback", total)

        st.divider()

        # ================= BAR CHART =================
        st.subheader("Total Feedback Distribution")
        bar_data = {
            "Feedback": {
                "Likes": likes,
                "Dislikes": dislikes
            }
        }
        st.bar_chart(bar_data)

        st.divider()

        # ================= LINE CHART =================
        st.subheader("Feedback Trend (Date-wise)")

        trend_df = trend_df.set_index("feedback_date")
        st.line_chart(trend_df)

        st.subheader("Model-wise Feedback Comparison")


        # ================= MODEL WISE COMPARISION CHART =================
        model_df = model_df.set_index("model")

        # Optional: better labels
        model_df = model_df.rename(columns={
            "likes": "👍 Likes",
            "dislikes": "👎 Dislikes"
        })

        st.bar_chart(model_df)