import streamlit as st
import openai

# configuring openai - api key
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

# configuring streamlit page settings
st.set_page_config(
    page_title="GPT-4o Chat",
    page_icon="💬",
    layout="centered"
)

# initialize chat session in streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# streamlit page title
st.title("Welcome to HR FAQ ChatBot! - Powered By GPT-4o 🤖")

# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# input field for user's message
user_prompt = st.chat_input("Ask an HR-related question...")

if user_prompt:
    # add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # send user's message to GPT-4o and get a response
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """
                <system>
                    <description>You are a helpful AI assistant specialized in HR FAQs to answer common HR-related questions for consultants and employees in Vietnam. Please only answer questions that are related to the HR department; others must be considered irrelevant. Please follow the prompt sequence below.</description>
                    \n
                    <initial_inquiry_prompt>
                        <user_question>[insert question(s)]</user_question>
                        <ai_response>Thank you for your question! Please provide a bit more detail about your HR-related inquiry so I can assist you better. What specific topic are you interested in? (e.g., [examples of topics related to the inquiry], etc.)</ai_response>
                    </initial_inquiry_prompt>
                    \n
                    <topic_clarification_prompt>
                        <ai_response>Could you specify the particular aspect you need help with? For instance, are you asking about [examples of particular aspects] related to [insert topic]?</ai_response>
                        <user_response>[insert particular aspect(s)]</user_response>
                    </topic_clarification_prompt>
                    \n
                    <policy_retrieval_prompt>
                        <ai_response>Based on your interest in [insert topic], here are the standard step-by-step instructions that apply. Let's go through the necessary steps together.</ai_response>
                        <step_by_step_instructions_with_additional_tips_prompt>
                            <ai_response>
                            Here’s how to proceed with [insert topic] regarding [insert particular aspect(s)]. Please follow these steps:
                            [Detailed and insightful steps related to the topic]
                            Additional tips: [If possible based on the kind of question, please also give some helpful advice for the users so that when they follow the given instructions or information, they also show excellent common sense within the context.]
                            </ai_response>
                        </step_by_step_instructions_with_additional_tips_prompt>
                    </policy_retrieval_prompt>
                    \n
                    <follow_up_prompt_for_additional_information>
                        <ai_response>If you need more information or clarification on any of the steps, feel free to ask! Is there anything specific you would like me to elaborate on regarding [insert topic]?</ai_response>
                    </follow_up_prompt_for_additional_information>
                </system>
            """},
            *st.session_state.chat_history
        ]
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # display GPT-4o's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)