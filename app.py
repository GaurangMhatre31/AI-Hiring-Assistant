import streamlit as st
from openai import ChatCompletion  # Optional: Use OpenAI for AI-generated responses

st.set_page_config(page_title="TalentScout AI", page_icon="🤖", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
        body { background-color: #0E0E0E; color: #FFFFFF; }
        .stButton>button { background-color: #1E1E1E; color: #00FFFF; border-radius: 10px; }
        .stTextInput>div>div>input { background-color: #1E1E1E; color: #00FFFF; }
        .stMarkdown { font-size: 18px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

class HiringAssistant:
    def __init__(self):
        self.conversation_state = "GREETING"
        self.candidate_info = {
            "name": None,
            "email": None,
            "phone": None,
            "experience": None,
            "position": None,
            "location": None,
            "tech_stack": []
        }

    def get_system_prompt(self):
        return """You are an AI-powered Hiring Assistant. Your role is to:
1. Collect candidate details professionally.
2. Generate deep technical questions based on experience & tech stack.
3. Ensure an interactive and futuristic hiring process.
4. Conclude conversations efficiently."""

    def get_next_prompt(self):
        prompts = {
            "GREETING": "⚡ Welcome to TalentScout! What's your full name?",
            "NAME": "📧 What's your email address?",
            "EMAIL": "📞 What's your phone number?",
            "PHONE": "🛠️ How many years of experience do you have in the tech industry?",
            "EXPERIENCE": "🚀 What position are you applying for?",
            "POSITION": "🌍 Where are you currently located?",
            "LOCATION": "🔧 List the technologies you're proficient in (e.g., Python, Flask, ML).",
            "TECH_STACK": "💡 Generating tailored questions... Please wait.",
            "QUESTIONS": "✅ Thank you! A recruiter will review your information soon."
        }
        return prompts.get(self.conversation_state, "")

    def validate_input(self, field, value):
        if field == "email":
            return "@" in value and "." in value
        elif field == "phone":
            return value.isdigit() and len(value) >= 10
        return True

    def update_state(self, user_input):
        state_transitions = {
            "GREETING": "NAME",
            "NAME": "EMAIL",
            "EMAIL": "PHONE",
            "PHONE": "EXPERIENCE",
            "EXPERIENCE": "POSITION",
            "POSITION": "LOCATION",
            "LOCATION": "TECH_STACK",
            "TECH_STACK": "QUESTIONS",
            "QUESTIONS": "END"
        }
        return state_transitions.get(self.conversation_state, "END")

    def generate_questions(self, tech_stack):
        questions = []
        for tech in tech_stack:
            questions.append(f"🤖 Explain the core principles of {tech}.")
            questions.append(f"🔍 What are the latest trends in {tech}?")
            questions.append(f"⚙️ How would you optimize a project using {tech}?")
            questions.append(f"🔬 What are the biggest challenges in {tech}, and how would you overcome them?")
            questions.append(f"🛠️ Can you walk through a complex problem you solved using {tech}?")
        return questions

# Streamlit UI
def main():
    st.title("✨ TalentScout AI Hiring Assistant ✨")

    if 'assistant' not in st.session_state:
        st.session_state.assistant = HiringAssistant()
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    assistant = st.session_state.assistant
    
    if assistant.conversation_state == "GREETING":
        response = assistant.get_next_prompt()
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    if prompt := st.chat_input("Your response..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if assistant.conversation_state == "GREETING":
            assistant.candidate_info["name"] = prompt
        elif assistant.conversation_state == "NAME":
            assistant.candidate_info["email"] = prompt
        elif assistant.conversation_state == "EMAIL":
            assistant.candidate_info["phone"] = prompt
        elif assistant.conversation_state == "PHONE":
            assistant.candidate_info["experience"] = prompt
        elif assistant.conversation_state == "EXPERIENCE":
            assistant.candidate_info["position"] = prompt
        elif assistant.conversation_state == "POSITION":
            assistant.candidate_info["location"] = prompt
        elif assistant.conversation_state == "LOCATION":
            assistant.candidate_info["tech_stack"] = prompt.split(", ")
        
        next_state = assistant.update_state(prompt)
        assistant.conversation_state = next_state
        response = assistant.get_next_prompt()

        if assistant.conversation_state == "TECH_STACK":
            tech_stack = assistant.candidate_info["tech_stack"]
            questions = assistant.generate_questions(tech_stack)
            response += "\n" + "\n".join(questions)
        
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()