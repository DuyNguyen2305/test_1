import streamlit as st
from PIL import Image
from streamlit_chat import message
from utils import get_initial_message, get_chatgpt_response, update_chat
import os
import openai
import pandas as pd

# Định nghĩa CSS cho tiêu đề
st.markdown(
    """
    <style>
    .title-text {
        color: red;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Thiết lập API key của ChatGPT
openai.api_key = "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"

logo_path = "logo.png"
logo_image = Image.open(logo_path)
col1, col2 = st.columns([2,1])

with col2:
    st.image(logo_image, width=180)

with col1:
    st.markdown('<h1 class="title-text">NKD Bot : Trợ lý ảo thời khóa biểu - Trường Đại học Bách Khoa.</h1>', unsafe_allow_html=True)

model = "gpt-3.5-turbo"
# model = "text-davinci-003"#"text-davinci-003"

@st.cache(allow_output_mutation=True)
def initialize_session_state():
    return {}

if 'session_state' not in st.session_state:
    st.session_state['session_state'] = initialize_session_state()

def login():
    # Hiển thị giao diện đăng nhập
    username = st.sidebar.text_input("Username", key='username')
    password = st.sidebar.text_input("Password", type="password", key='password')
    login_button = st.sidebar.button("Login")

    if login_button:
        # Kiểm tra thông tin đăng nhập
        if username == "admin" and password == "123":
            st.success("Đăng nhập thành công!")
            # Hiển thị chatbot nếu đăng nhập thành công
            # show_chatbot()
            # router("chatbot")
            st.session_state['is_logged_in'] = True
        else:
            st.error("Tên người dùng hoặc mật khẩu không đúng")

def chatbot():
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []

    # placeholder = st.empty()
    query = st.sidebar.text_input("Query: ", key="input")
    submit_button = st.sidebar.button("Gửi")
    # Xử lý khi nút gửi được nhấn

    if 'messages' not in st.session_state:
        st.session_state['messages'] = get_initial_message()

    if query:
        with st.spinner("generating..."):
            messages = st.session_state['messages']
            messages = update_chat(messages, "user", query)
            # st.write("Before  making the API call")
            # st.write(messages)
            response = get_chatgpt_response(messages, model)
            messages = update_chat(messages, "assistant", response)
            st.session_state.past.append(query)
            st.session_state.generated.append(response)

    if st.session_state['generated']:
        # st.title(st.session_state)
        with st.sidebar:

            for i in range(len(st.session_state['generated']) - 1, -1, -1):
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))

            # with st.expander("Show Messages"):
            #     st.write(messages)
def router(page):
    if 'is_logged_in' not in st.session_state:
        st.session_state['is_logged_in'] = False
    # st.title(st.session_state)

    if not st.session_state['is_logged_in']:
        login()
    else:
        chatbot()

def display_timetable():
    timetable_df = pd.read_csv('Book4.csv')
    # timetable_df.style.highlight_max()
    # Tạo một bảng HTML từ DataFrame
    html_table = timetable_df.to_html(index=False, escape=False)

    # Hiển thị bảng trong Streamlit và tô màu các ô
    # st.write(html_table, unsafe_allow_html=True)

    # Tô màu các ô có giá trị 1 trong bảng HTML
    html_table = html_table.replace('<td>1</td>', '<td style="background-color: green;">1</td>')
    # Hiển thị bảng đã tô màu bằng Markdown trong Streamlit
    st.markdown(html_table, unsafe_allow_html=True)

def main():
    # Sử dụng radio button để chọn trang hiển thị
    page = st.sidebar.radio("TRANG", ["LOGIN", "CHAT"])
    router(page)
    st.subheader("Thời khóa biểu trong tuần")
    display_timetable()

if __name__ == "__main__":
    main()