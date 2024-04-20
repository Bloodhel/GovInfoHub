import streamlit as st
import requests

# Define Streamlit layout
st.title("GovInfoHub")

# Navigation bar
st.markdown("""
    <style>
        .container {
            width: 80%;
            max-width: 1200px;
            margin: auto;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .nav-logo img {
            height: 40px;
        }

        .nav-links {
            list-style-type: none;
            margin: 0;
            padding: 0;
            font-size: 18px;
        }

        .nav-links li {
            display: inline-block;
            margin-right: 20px;
        }

        .nav-links li a {
            color: #fff;
            text-decoration: none;
            transition: color 0.3s ease;
        }

        .nav-links li a:hover {
            color: #fff;
        }
    </style>
""", unsafe_allow_html=True)

st.write('<nav class="container"><div class="nav-logo"><img src="src\Logo.png" alt="GovInfoHub Logo"></div><ul class="nav-links"><li><a href="#contact">Contact Us</a></li><li><a href="AboutUs.html">About Us</a></li></ul></nav>', unsafe_allow_html=True)

# Chat interface
st.markdown("""
    <style>
        .chat-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }

        .chat-box {
            width: 50%;
            max-width: 200px;
            padding: 15px;
            border: 1px solid #ccc;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            background-color: #e1f0f1;
            margin-bottom: 20px;
        }

        .message {
            background-color: #fff;
            padding: 4px 5px;
            margin-bottom: 10px;
            border-radius: 5px;
            color: #333;
            font-size: 14px;
        }

        #user-input {
            width: calc(50% - 100px);
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 4px;
            margin-right: 10px;
        }

        #send-btn {
            width: 60px;
            padding: 8px 10px;
            background-color: #138808;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
    </style>
""", unsafe_allow_html=True)

st.write('<div class="chat-container"><div class="chat-box" id="chat-box"><div class="message">Welcome to GovInfoHub! How can we assist you today?</div></div><input type="text" id="user-input" placeholder="Type your message here..."><button id="send-btn">Send</button></div>', unsafe_allow_html=True)

# Function to send message to backend
@st.cache
def send_message(user_input):
    response = requests.post('https://govinfohub-8.onrender.com', json={'message': user_input})
    if response.status_code == 200:
        return response.json()['message']
    else:
        return "Error occurred while processing your request."

# Function to handle user input
def handle_input():
    user_input = st.text_input("Your message here:")
    if st.button("Send") or st.session_state.enter_pressed:
        if user_input.strip() != "":
            st.write(f"User: {user_input}")
            bot_response = send_message(user_input)
            st.write(f"Bot: {bot_response}")

# Listen for Enter key press
if st.session_state.enter_pressed is None:
    st.session_state.enter_pressed = False

if st.session_state.enter_pressed:
    handle_input()

if st.session_state.enter_pressed != st.button("Send"):
    st.session_state.enter_pressed = st.button("Send")

handle_input()
