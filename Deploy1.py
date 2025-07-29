import streamlit as st
import openai

# Page setup
st.set_page_config(page_title="Social Media Buzz Generator", layout="centered")
st.title("📣 Social Media Post Generator")
st.markdown("Create viral posts for LinkedIn, Instagram, and Twitter with an AI-generated image!")

# Input API Key
openai_api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")
if not openai_api_key:
    st.warning("Please enter your OpenAI API key to proceed.")
    st.stop()

# Set the API key for the OpenAI client
client = openai.OpenAI(api_key=openai_api_key)

# Inputs
instruction = st.text_area("📝 What do you want to announce?", placeholder="E.g. Launching our new AI health tracker...")
language = st.selectbox("🌐 Choose language", ["English", "Hindi", "Spanish", "French", "German", "Chinese"])

# Generate button
if st.button("✨ Generate Posts and Image") and instruction:

    with st.spinner("Generating content..."):

        def generate_post(platform):
            word_limit = "200-300 words" if platform == "LinkedIn" else "under 150 words"
            prompt = (
                f"Write an exciting, buzz-worthy social media post in {language} about this announcement:\n\n"
                f"{instruction}\n\n"
                f"Format it for {platform}, within {word_limit}."
            )
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.8
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                return f"❌ Error generating {platform} post: {str(e)}"

        def generate_image(prompt_text):
            try:
                img_response = client.images.generate(
                    model="dall-e-3",
                    prompt=f"Illustration style image representing: {prompt_text}",
                    n=1,
                    size="1024x1024"
                )
                return img_response.data[0].url
            except Exception as e:
                return None

        # Generate for all platforms
        platforms = ["LinkedIn", "Instagram", "Twitter"]
        posts = {p: generate_post(p) for p in platforms}
        image_url = generate_image(instruction)

        # Display results
        st.subheader("📄 Generated Posts")
        for p in platforms:
            st.markdown(f"### {p}")
            st.write(posts[p])

        st.subheader("🖼️ AI-generated Image")
        if image_url:
            st.image(image_url, use_column_width=True)
        else:
            st.error("Image generation failed. Try again later or check your OpenAI key.")

        # Store in session state
        if "history" not in st.session_state:
            st.session_state["history"] = []
        st.session_state["history"].append({
            "instruction": instruction,
            "posts": posts,
            "image_url": image_url
        })

# Sidebar history
if "history" in st.session_state and st.session_state["history"]:
    st.sidebar.title("🕒 Previous Generations")
    for idx, item in enumerate(st.session_state["history"][::-1]):
        st.sidebar.markdown(f"**{len(st.session_state['history']) - idx}.** {item['instruction'][:50]}...")
