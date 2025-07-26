# app.py
import streamlit as st
import openai
from PIL import Image
import base64
import io

st.set_page_config(page_title="GPT Vision App", layout="centered")

st.title("🧠 GPT Vision App")
st.caption("Upload an image and get a GPT-4 Vision description.")

openai.api_key = st.secrets["OPENAI_API_KEY"]

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Convert image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    if st.button("Analyze Image"):
        with st.spinner("Analyzing..."):
            response = openai.chat.completions.create(
                model="gpt-4o",  # or "gpt-4-vision-preview"
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Describe this image in detail."},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{img_base64}"},
                            },
                        ],
                    }
                ],
                max_tokens=500,
            )

            st.markdown("### 📝 GPT-4's Description")
            st.write(response.choices[0].message.content)