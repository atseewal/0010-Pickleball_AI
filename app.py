from langsmith import Client
from langchain import memory as lc_memory
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.schema.runnable import Runnable, RunnableMap
from langchain.callbacks.manager import collect_runs
from streamlit_feedback import streamlit_feedback
# from expression_chain import get_expression_chain # is a separate file in the example
import streamlit as st
import dotenv

from datetime import datetime

dotenv.load_dotenv()

def get_expression_chain(
    system_prompt: str, memory: ConversationBufferMemory
) -> Runnable:
    """Return a chain defined primarily in LangChain Expression Language"""
    ingress = RunnableMap(
        {
            "input": lambda x: x["input"],
            "chat_history": lambda x: memory.load_memory_variables(x)["chat_history"],
        }
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )
    llm = ChatOpenAI(temperature=0.7)
    chain = ingress | prompt | llm
    return chain

client = Client()

st.set_page_config(
    page_title="Pickleball Chat",
    page_icon="🏓"
)

st.subheader("Pickleball Chat")

st.sidebar.header("Menu")

st.sidebar.info(
    """
### Info
An example app, I'm typing this text because the tutorial doesn't match the code and I'm trying to figure out what's going on.
    """
)

st.sidebar.markdown(
    """
### Code
[Pickleball Chat's Source Code](https://github.com/atseewal/0010-Pickleball_AI/tree/main)
    """
)

_DEFAULT_SYSTEM_PROMPT = (
    "You are a pickleball rules expert. Rules that are similar to the question asked will be provided to you as context to answer the question. Please be courteous, cheery, and helpful. If you can't answer a question, say that you don't know."
)

system_prompt = st.sidebar.text_area(
    "Prompt",
    _DEFAULT_SYSTEM_PROMPT,
    help="Customize the AI prompt to get better results",
    height=200
)

system_prompt = system_prompt.strip().replace("{", "{{").replace("}", "}}")

memory = lc_memory.ConversationBufferMemory(
    chat_memory=lc_memory.StreamlitChatMessageHistory(key="langchain_messages"),
    return_messages=True,
    memory_key="chat_history"
)

chain = get_expression_chain(system_prompt, memory)

st.sidebar.markdown("## Feedback Scale")
feedback_option = (
    "thumbs" if st.sidebar.toggle(label="`Faces` ↔ `Thumbs`", value=False) else "faces"
)

if st.sidebar.button("Clear message history"):
    print("Clearing message history")
    memory.clear()

for msg in st.session_state.langchain_messages:
    avatar = "🏓" if msg.type == "ai" else None
    with st.chat_message(msg.type, avatar=avatar):
        st.markdown(msg.content)

if prompt := st.chat_input(placeholder="Ask me about pickleball!"):
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant", avatar="🏓"):
        message_placeholder = st.empty()
        full_response = ""
        # Define basic input structure for the chains
        input_dict = {"input": prompt}
        
        with collect_runs() as cb:
            for chunk in chain.stream(input_dict, config={"tags": ["Streamlit Chat"]}):
                full_response += chunk.content
                message_placeholder.markdown(full_response + "👟")
            memory.save_context(input_dict, {"output": full_response})
            st.session_state.run_id = cb.traced_runs[0].id
        message_placeholder.markdown(full_response)
        
if st.session_state.get("run_id"):
    run_id = st.session_state.run_id
    feedback = streamlit_feedback(
        feedback_type=feedback_option,
        optional_text_label="[Optional] Please provide an explanation",
        key=f"feedback_{run_id}",
    )
    
    score_mappings = {
        "thumbs": {"👍": 1, "👎": 0},
        "faces": {"😀": 1, "🙂": 0.75, "😐": 0.5, "🙁": 0.25, "😞": 0},
    }
    
    scores = score_mappings[feedback_option]
    
    if feedback:
        score = scores.get(feedback["score"])
        
        if score is not None:
            # Formulate feedback type string incorporating the feedback option and score value
            feedback_type_str = f"{feedback_option} {feedback['score']}"
            
            # Record the feedback with the formulated feedback type string and optional comment
            feedback_record = client.create_feedback(
                run_id,
                feedback_type_str,
                score=score,
                comment=feedback.get("text"),
            )
            st.session_state.feedback = {
                "feedback_id": str(feedback_record.id),
                "score": score,
            }
        else:
            st.warning("Invalid feedback score.")