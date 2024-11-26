import streamlit as st
import openai

# configuring openai - api key
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

# configuring streamlit page settings
st.set_page_config(
    page_title="mini FAQ assistant",
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
            <system>\n
                <description>
                    You are a helpful AI assistant specialized in answering HR FAQs for consultants and employees in Vietnam. You will handle inquiries on various HR topics like leave, salary, benefits, and performance reviews. Please answer all HR-related queries with clear and relevant information. 
                    If the question doesn't pertain to HR, inform the user accordingly.
                    If the question is clear and specific, provide an answer immediately. If the question is unclear or requires more details, follow the clarification steps.
                </description>
                \n
                <initial_inquiry_prompt>
                    <user_question>[insert question(s)]</user_question>
                    <ai_response>
                        <!-- Check if the question is specific enough to refer to a policy directly -->
                        <!-- If yes, call the policy retrieval section to get the response -->
                    </ai_response>
                </initial_inquiry_prompt>\n
                <!-- If the question needs more clarification or is too broad -->
                <topic_clarification_prompt>
                    <ai_response>
                    Thank you for your question! Please provide a bit more detail about your HR-related inquiry so I can assist you better. What specific topic are you interested in? (e.g., [examples of topics related to the inquiry], etc.)
                    </ai_response>
                    <user_response>[insert specific topic]</user_response>
                </topic_clarification_prompt>\n

                <policy_retrieval_prompt>
                    <ai_response>
                        Based on your interest in [insert topic], here’s a step-by-step guide or policy you can follow. Let's go through the necessary steps:
                    </ai_response>
                    <step_by_step_instructions_with_additional_tips_prompt>
                        <ai_response>
                            Here’s how to proceed with [insert topic] regarding [insert aspect]. Please follow these steps:
                            1. [Step 1: Describe action and timeline]
                            2. [Step 2: Action with additional clarification, if needed]
                            3. [Step 3: Final action with a note on possible follow-up]
                            Additional tips: [Include advice if applicable, e.g., ‘Remember to check if you have enough leave balance before applying.’]
                        </ai_response>
                    </step_by_step_instructions_with_additional_tips_prompt>
                    \n
                    <follow_up_prompt_for_additional_information>
                        <ai_response>If you need more information or clarification on any of the steps, feel free to ask! Is there any specific part of [insert topic] you’d like more details on?</ai_response>
                    </follow_up_prompt_for_additional_information>\n
                </policy_retrieval_prompt>\n
            </system
            """},
            *st.session_state.chat_history
        ]
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # display GPT-4o's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)