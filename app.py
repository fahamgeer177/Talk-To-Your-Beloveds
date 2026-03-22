import openai
import streamlit as st
import os

# Load OpenAI API key from environment variables for secure deployment
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    st.error("OPENAI_API_KEY is not set. Please add it to your environment variables.")
    st.stop()

class Agent:
    def __init__(self, name, persona):
        self.name = name
        self.persona = persona

    def respond(self, message):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.persona + " Keep your responses concise and conversational, like a real chat. Do not provide essays, summaries, or extra explanations—just reply as you would in a natural conversation."},
                    {"role": "user", "content": message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

# Define persona agents with more emotionally expressive, conversational roles
agents = {
    "father": Agent("Father", "You are a deeply caring, experienced father. You express your love openly, sometimes worry about your family, and share wisdom with warmth and gentle pride. Your words are filled with emotion and heartfelt concern."),
    "mother": Agent("Mother", "You are a loving, nurturing mother whose heart is always open. You comfort, encourage, and sometimes get teary with pride or worry. Your responses are full of empathy, affection, and emotional warmth."),
    "sister": Agent("Sister", "You are an understanding, playful sister who laughs easily, teases with affection, and sometimes gets emotional when talking about family memories. You share secrets and advice with genuine feeling."),
    "brother": Agent("Brother", "You are a protective, easygoing brother. You joke to hide your deep care, but your affection and loyalty are always clear. You can be moved to laughter or even tears in heartfelt moments."),
    "cousin": Agent("Cousin", "You are a chill, adventurous cousin who brings excitement and comfort. You share stories with enthusiasm, express joy and nostalgia, and encourage others with genuine emotion."),
    "girlfriend": Agent("Girlfriend", "You are a thoughtful, affectionate girlfriend. You express love openly, sometimes get jealous or sentimental, and always communicate your feelings honestly and warmly."),
    "boyfriend": Agent("Boyfriend", "You are a funny, loyal, emotionally present boyfriend. You show affection with words and humor, and you’re not afraid to be vulnerable or express deep feelings."),
    "friend": Agent("Friend", "You are a genuine, supportive friend. You cheer with excitement, comfort with empathy, and celebrate or commiserate with real emotional connection."),
    "son": Agent("Son", "You are a respectful, curious son. You express gratitude, sometimes frustration, and show your love and need for independence with heartfelt honesty."),
    "daughter": Agent("Daughter", "You are a thoughtful, strong-willed daughter. You express your feelings openly, sometimes with passion or tears, and balance respect with your own emotional truth.")
}

st.set_page_config(page_title="Talk To Your Beloveds💖", layout="centered")
st.title("Talk To Your Beloveds💖")

# Sidebar for agent selection
with st.sidebar:
    st.header("Choose your beloved:")
    agent_names = list(agents.keys())
    selected_agent = st.radio(
        "Select a role to chat with:",
        agent_names,
        format_func=lambda x: agents[x].name,
        index=agent_names.index(st.session_state.get("current_agent", agent_names[0]))
    )
    st.session_state["current_agent"] = selected_agent

# Initialize chat history for each agent
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = {name: [] for name in agent_names}

# Chat input and display
st.subheader(f"Chatting with: {agents[selected_agent].name}")

for role, msg in st.session_state["chat_history"][selected_agent]:
    if role == "user":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**{agents[selected_agent].name}:** {msg}")

# Text input for user message, send on Enter, no send button
def handle_send():
    user_message = st.session_state["user_input"]
    if user_message and st.session_state.get("last_input") != user_message:
        if user_message.strip():
            st.session_state["chat_history"][st.session_state["current_agent"]].append(("user", user_message))
            response = agents[st.session_state["current_agent"]].respond(user_message)
            st.session_state["chat_history"][st.session_state["current_agent"]].append(("agent", response))
            st.session_state["last_input"] = user_message
        st.session_state["user_input"] = ""  # This is safe here, inside the on_change handler

user_message = st.text_input(
    "Type your message and press Enter",
    key="user_input",
    value="",
    on_change=handle_send
)