import streamlit as st
from openai import ChatCompletion  # Or HuggingFace transformers, depending on your model

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
        return """You are TalentScout's AI Hiring Assistant. Your role is to:
1. Gather candidate information professionally and efficiently.
2. Generate relevant technical questions based on their tech stack.
3. Maintain a friendly, professional tone.
4. End conversations when requested."""

    def get_next_prompt(self):
        if self.conversation_state == "GREETING":
            return "Welcome to TalentScout! I'm here to learn about your background and technical skills. What's your full name?"
        
        prompts = {
            "NAME": "What's your email address?",
            "EMAIL": "What's your phone number?",
            "PHONE": "How many years of experience do you have in the tech industry?",
            "EXPERIENCE": "What position are you applying for?",
            "POSITION": "Where are you currently located?",
            "LOCATION": "Please list the technologies you are proficient in (e.g., Python, Django, React).",
            "TECH_STACK": "I will now generate questions for the technologies you listed. Please wait...",
            "QUESTIONS": "Thank you! A recruiter will review your information and get in touch with you soon."
        }
        return prompts.get(self.conversation_state, "")

    def validate_input(self, field, value):
        if field == "email":
            return "@" in value and "." in value
        elif field == "phone":
            return len(value) >= 10
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
            questions.append(f"Can you explain the core concepts of {tech}?")
        return questions


# Streamlit UI
def main():
    st.title("TalentScout Hiring Assistant")

    if 'assistant' not in st.session_state:
        st.session_state.assistant = HiringAssistant()
        st.session_state.messages = []

    # Display messages from the conversation
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    assistant = st.session_state.assistant

    # If it's the greeting state, no need to validate, just ask for the name
    if assistant.conversation_state == "GREETING":
        response = assistant.get_next_prompt()
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # After the user inputs a response
    if prompt := st.chat_input("Your response"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Validate and update state after receiving a valid response
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

        # Transition to next state and get next prompt
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
