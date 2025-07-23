import streamlit as st
import openai
from openai import OpenAI
import os
from io import StringIO
import base64

# ✅ Set API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set page configuration
st.set_page_config(
    page_title="AI-D: Your First Aid Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    .stApp {
        background: linear-gradient(135deg, #1c2b4d 0%, #3d6cb9 100%);
        font-family: 'Inter', sans-serif;
    }
    #MainMenu, footer, header {visibility: hidden;}
    .main .block-container {padding-top: 1rem; max-width: 1200px;}
    .main-header {
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px;
        padding: 2rem; text-align: center; margin-bottom: 2rem;
    }
    .main-header h1 {
        color: #ffffff; font-size: 3.5rem; font-weight: 700;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    .main-header p {
        color: rgba(255, 255, 255, 0.85); font-size: 1.25rem;
    }
    .content-card {
        background: rgba(255, 255, 255, 0.08); backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 20px;
        padding: 2rem; margin: 1rem 0; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease;
    }
    .content-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
    }
    .emergency-box {
        background: rgba(217, 48, 56, 0.15); backdrop-filter: blur(10px);
        border: 1px solid rgba(217, 48, 56, 0.5); border-radius: 15px;
        padding: 1.5rem; margin: 1rem 0; color: #f8d7da;
        animation: emergencyPulse 2s infinite;
    }
    @keyframes emergencyPulse {
        0% { box-shadow: 0 0 0 0 rgba(217, 48, 56, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(217, 48, 56, 0); }
        100% { box-shadow: 0 0 0 0 rgba(217, 48, 56, 0); }
    }
    .emergency-box h3 {
        color: #d93038;
        text-shadow: 0 0 10px rgba(217, 48, 56, 0.3);
    }
    .warning-box {
        background: rgba(255, 193, 7, 0.1); backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 193, 7, 0.3); border-radius: 15px;
        padding: 1.5rem; margin: 1rem 0; color: #ffc107;
    }
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #4facfe !important;
        box-shadow: 0 0 15px rgba(79, 172, 254, 0.3) !important;
    }
    .stButton > button {
        background-color: #4facfe !important;
        background-image: linear-gradient(315deg, #4facfe 0%, #00f2fe 74%) !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.2) !important;
    }
    .stFileUploader > div {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 2px dashed rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
    }
    .stFileUploader > div:hover {
        border-color: #4facfe !important;
        background: rgba(0, 0, 0, 0.3) !important;
    }
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
    }
    .stMarkdown, .stText, .stRadio {
        color: #f0f0f0 !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: rgba(0, 0, 0, 0.1); }
    ::-webkit-scrollbar-thumb { background: #4facfe; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #00f2fe; }
</style>""", unsafe_allow_html=True)


# ✅ Use environment-based client initializer
def initialize_openai_client():
    try:
        if not openai.api_key:
            st.error("Authentication Error: OpenAI API key not found.")
            return None
        return OpenAI()
    except Exception as e:
        st.error(f"Error initializing OpenAI client: {str(e)}")
        return None


def get_first_aid_advice(client, injury_description, content_type="text", image_data=None):
    try:
        if content_type == "image" and image_data:
            prompt = """You are a qualified first aid assistant..."""
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                ]}],
                max_tokens=1000, temperature=0.3
            )
        else:
            prompt = f"""You are a qualified first aid assistant... Injury Description: {injury_description}..."""
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful and clear first aid assistant..."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000, temperature=0.3
            )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred while getting advice: {str(e)}")
        return None


def read_uploaded_file(uploaded_file):
    try:
        if uploaded_file.type.startswith('image/'):
            image_data = base64.b64encode(uploaded_file.getvalue()).decode()
            st.info("Image uploaded successfully! The AI will analyze the image.")
            return image_data, "image"
        else:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            content = stringio.read()
            return content, "text"
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None, None


def main():
    st.markdown('''
    <div class="main-header">
        <h1>AI-D 🩺</h1>
        <p>Your Intelligent Assistant for First Aid & Social Well-being</p>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("""<div class="emergency-box">
        <h3>🚨 In a Life-Threatening Emergency, Call for Help First!</h3>
        <p>This tool provides guidance, not a replacement for professional medical services...</p>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("## ✍ Describe the Situation")
        input_method = st.radio("Select Input Method:", ("Text Description", "Upload a File (Image or Text)"), horizontal=True)
        injury_description, content_type, image_data = "", "text", None

        if input_method == "Text Description":
            injury_description = st.text_area("Describe the injury in detail:", height=150, placeholder="Example: My friend fell and has a deep cut...")
        else:
            uploaded_file = st.file_uploader("Upload image or text file:", type=['txt', 'png', 'jpg', 'jpeg', 'webp'])
            if uploaded_file:
                file_content, file_type = read_uploaded_file(uploaded_file)
                if file_content:
                    if file_type == "image":
                        content_type = "image"
                        image_data = file_content
                        injury_description = "Image uploaded for analysis."
                        st.image(uploaded_file, caption="Image for Analysis", width=300)
                    else:
                        content_type = "text"
                        injury_description = file_content
                        st.text_area("File Content:", value=injury_description, height=150, disabled=True)

        if st.button("🚀 Get First Aid Advice", type="primary"):
            if not injury_description.strip() and content_type != "image":
                st.error("Input Required: Please describe the injury or upload a file.")
            else:
                with st.spinner("🧠 AI is analyzing the situation..."):
                    client = initialize_openai_client()
                    if client:
                        advice = get_first_aid_advice(client, injury_description, content_type, image_data)
                        if advice:
                            st.success("Analysis Complete! Here is your guidance.")
                            st.markdown("---")
                            st.markdown("### 🩹 First Aid Guidance")
                            st.markdown(advice)
                            st.markdown("""<div class="warning-box">
                                <h4>⚠ Important Disclaimer</h4>
                                <p>This AI-generated advice is for informational purposes only...</p>
                            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### ☎ Emergency Numbers")
        st.markdown("""
        - 🇮🇳 India: 102 / 108  
        - 🇺🇸 USA/Canada: 911  
        - 🇪🇺 Europe: 112  
        - 🇬🇧 UK: 999  
        - 🇦🇺 Australia: 000
        """)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### ✅ Quick First Aid Reminders")
        with st.expander("🩸 Bleeding"):
            st.markdown("""1. Use gloves if available...""")
        with st.expander("🔥 Burns (Minor)"):
            st.markdown("""1. Run cool (not cold) water...""")
        with st.expander("🦴 Sprains (R.I.C.E.)"):
            st.markdown("""- REST, ICE, COMPRESSION, ELEVATION""")
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
