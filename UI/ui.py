import sys, os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import ingest_uploaded_file, ask_question

st.set_page_config(page_title="PolyDoc Chat", layout="wide")

st.markdown("""
<style>
html,body,[data-testid="stApp"]{
height:100vh;
overflow:hidden;
background:linear-gradient(135deg,#020617,#0f172a,#1e293b);
}

.block-container{
height:100vh;
padding:0;
}

.header{
padding:18px 30px;
font-size:34px;
font-weight:800;
color:#7dd3fc;
border-bottom:1px solid rgba(255,255,255,.08);
}

.layout{
display:flex;
height:calc(100vh - 80px);
}

.sidebar{
width:340px;
padding:20px;
background:rgba(255,255,255,.03);
border-right:1px solid rgba(255,255,255,.08);
}

.chat-wrapper{
flex:1;
display:flex;
flex-direction:column;
}

.chat-box{
flex:1;
padding:20px;
overflow-y:auto;
}

.input-box{
padding:18px;
border-top:1px solid rgba(255,255,255,.08);
background:rgba(255,255,255,.03);
}

.msg-user{
background:#3b82f6;
color:white;
padding:14px 18px;
border-radius:18px;
margin:10px 0 10px auto;
max-width:70%;
}

.msg-bot{
background:#334155;
color:#e5e7eb;
padding:14px 18px;
border-radius:18px;
margin:10px 0;
max-width:70%;
}

button{
background:#38bdf8!important;
color:#020617!important;
border-radius:12px!important;
font-weight:600!important;
}
</style>
""",unsafe_allow_html=True)

st.markdown('<div class="header">PolyDoc Chat</div>',unsafe_allow_html=True)

left,right=st.columns([0.25,0.75])

with left:
    st.markdown('<div class="sidebar">',unsafe_allow_html=True)

    files=st.file_uploader(
        "Upload files",
        accept_multiple_files=True
    )

    if st.button("Process documents",use_container_width=True):
        if files:
            for f in files:
                ingest_uploaded_file(f.getvalue(),f.name)
            st.success("Documents processed")

    if st.button("Clear chat",use_container_width=True):
        st.session_state.messages=[]

    st.markdown('</div>',unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages=[]

with right:
    st.markdown('<div class="chat-wrapper">',unsafe_allow_html=True)

    st.markdown('<div class="chat-box">',unsafe_allow_html=True)
    for m in st.session_state.messages:
        if m["role"]=="user":
            st.markdown(f'<div class="msg-user">{m["content"]}</div>',unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="msg-bot">{m["content"]}</div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('<div class="input-box">',unsafe_allow_html=True)
    user_input=st.chat_input("Ask about your documents")
    st.markdown('</div>',unsafe_allow_html=True)

    if user_input:
        st.session_state.messages.append({"role":"user","content":user_input})

        with st.spinner("Thinking..."):
            answer=ask_question(user_input)

        st.session_state.messages.append({"role":"assistant","content":answer})

    st.markdown('</div>',unsafe_allow_html=True)
