import streamlit as st
from main import preprocess, detect_mood_vader, generate_palette, mood_messages

st.set_page_config(page_title="Mood Palette Generator", page_icon="🎨")

st.markdown(
    """
    <h1 style="text-align:center; font-size:42px;">🎨 Mood Palette Generator</h1>
    """,
    unsafe_allow_html=True,
)

def set_background_css(mood):

    css_dict = {

        "happy": """
            .stApp {
              background: linear-gradient(-45deg, #f6d365, #fda085, #fbc2eb, #a6c1ee);
              background-size: 400% 400%;
              animation: gradient 8s ease infinite;
            }
            @keyframes gradient {
              0% {background-position: 0% 50%;}
              50% {background-position: 100% 50%;}
              100% {background-position: 0% 50%;}
            }
        """,

        "sad": """
            .stApp {
                background: linear-gradient(180deg, #0f2027, #203a43, #2c5364);
                background-size: 200% 200%;
                animation: sadFlow 9s ease-in-out infinite;
            }
            @keyframes sadFlow {
                0% {background-position: 50% 0%;}
                50% {background-position: 50% 100%;}
                100% {background-position: 50% 0%;}
            }
        """,

        "sad_birthday": """
            .stApp {
                background: linear-gradient(180deg, #0f2027, #203a43, #2c5364);
                background-size: 200% 200%;
                animation: sad_bFlow 9s ease-in-out infinite;
            }
            @keyframes sad_bFlow {
                0% {background-position: 50% 0%;}
                50% {background-position: 50% 100%;}
                100% {background-position: 50% 0%;}
            }
        """,

        "sad_wedding": """
            .stApp {
                background: linear-gradient(180deg, #0f2027, #203a43, #2c5364);
                background-size: 200% 200%;
                animation: sad_wFlow 9s ease-in-out infinite;
            }
            @keyframes sad_wFlow {
                0% {background-position: 50% 0%;}
                50% {background-position: 50% 100%;}
                100% {background-position: 50% 0%;}
            }
        """,

        "disappointed": """
            .stApp {
                background: linear-gradient(180deg, #0f2027, #203a43, #2c5364);
                background-size: 200% 200%;
                animation: sad_pFlow 9s ease-in-out infinite;
            }
            @keyframes sad_pFlow {
                0% {background-position: 50% 0%;}
                50% {background-position: 50% 100%;}
                100% {background-position: 50% 0%;}
            }
        """,

        "calm": """
            .stApp {
                background: radial-gradient(circle, #d4fc79, #96e6a1, #84fab0, #8fd3f4);
                animation: calmBlur 8s ease infinite;
            }
            @keyframes calmBlur {
                0% {background-position: 50% 0%;}
                50% {background-position: 50% 100%;}
                100% {background-position: 50% 0%;}
            }
        """,

        "romantic": """
            .stApp {
                background: radial-gradient(circle at center, #ff9a9e, #fad0c4);
                background-size: 400% 400%;
                animation: pinkMove 6s ease infinite alternate;
            }
            @keyframes pinkMove {
                from {background-position: 0% 50%;}
                to   {background-position: 100% 50%;}
            }
        """,

         "wedding": """
            .stApp {
                background: radial-gradient(circle at center, #ff9a9e, #fad0c4);
                background-size: 400% 400%;
                animation: pink_WMove 6s ease infinite alternate;
            }
            @keyframes pink_WMove {
                from {background-position: 0% 50%;}
                to   {background-position: 100% 50%;}
            }
        """,

         "happy_wedding": """
            .stApp {
                background: radial-gradient(circle at center, #ff9a9e, #fad0c4);
                background-size: 400% 400%;
                animation: pink_hwMove 6s ease infinite alternate;
            }
            @keyframes pink_hwMove {
                from {background-position: 0% 50%;}
                to   {background-position: 100% 50%;}
            }
        """,

         "calm_wedding": """
            .stApp {
                background: radial-gradient(circle at center, #ff9a9e, #fad0c4);
                background-size: 400% 400%;
                animation: pink_cwMove 6s ease infinite alternate;
            }
            @keyframes pink_cwMove {
                from {background-position: 0% 50%;}
                to   {background-position: 100% 50%;}
            }
        """,

        "excited": """
            .stApp {
                background: linear-gradient(45deg, #ff00c8, #7a00ff, #00ffe0, #fff600, #ff006e);
                background-size: 400% 400%;
                animation: neonParty 6s linear infinite;
            }
            @keyframes neonParty {
                0% {background-position: 0% 50%;}
                50% {background-position: 100% 50%;}
                100% {background-position: 0% 50%;}
            }
        """,

        "focus": """
            .stApp {
                background: linear-gradient(45deg, #1CB5E0, #000046);
                background-size: 200% 200%;
                animation: focusPulse 8s ease infinite;
            }
            @keyframes focusPulse {
                0% {filter: brightness(100%);}
                50% {filter: brightness(120%);}
                100% {filter: brightness(100%);}
            }
        """,

        "dark": """
            .stApp {
                background: radial-gradient(circle at center,#C0C0C0,#708090) ;
                background-size: 400% 400%;
                animation: darkMove 6s ease infinite alternate;
            }
            @keyframes darkMove {
                from {background-position: 0% 50%;}
                to   {background-position: 100% 50%;}
            }
        """,

        "light": """
            .stApp {
                background: linear-gradient(120deg, #20B2AA, #EEE8AA , #F08080);
                background-size: 400% 400%;
                animation:lightMove 7s ease infinite alternate;
            }
             @keyframes lightMove {
                from {background-position: 0% 50%;}
                to   {background-position: 100% 50%;}

            }
        """,
         "aesthetic": """
            .stApp {
                background: linear-gradient(45deg, #E48F50, #753130, #2D293B, #60859E, #729BAE);
                background-size: 400% 400%;
                animation: neon_Party 8s linear infinite;
            }
            @keyframes neon_Party {
                0% {background-position: 0% 50%;}
                50% {background-position: 100% 50%;}
                100% {background-position: 0% 50%;}
            }
        """,

        # fallback for all other moods:
        "default": """
            .stApp {
                background: linear-gradient(120deg, #e0c3fc, #8ec5fc);
                animation: soft 10s ease infinite;
            }
            @keyframes soft {
                0% {background-position: 0% 50%;}
                50% {background-position: 100% 50%;}
                100% {background-position: 0% 50%;}
            }
        """
    }

    css = css_dict.get(mood, css_dict["default"])

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)



user_input = st.text_input(
    "Enter your mood or a short story:",
    placeholder="Type something like 'I feel calm and dreamy today'..."
)

if st.button("Generate Palette"):
    
    text = preprocess(user_input)
    mood = detect_mood_vader(text)

   
    set_background_css(mood)

    
    colors = generate_palette(mood)
    emoji, msg = mood_messages.get(mood, ("🎨", "A lovely color mood just for you."))

    st.markdown(
        f"""
        <h2 style="text-align:center; margin-top:20px;">{emoji} {msg}</h2>
        <p style="text-align:center; font-size:18px;"><b>Detected Mood:</b> {mood}</p>
        """,
        unsafe_allow_html=True,
    )

    
    cols = st.columns(5)

    swatch_css = """
    <style>
      .swatch-box {
      width:110px;
      height:160px;
      border-radius:20px;
      transition:transform 0.3s ease,box-shadow 0.3s ease;
      box-shadow: 0px 8px 18px rgba(0,0,0,0.25);
      }
      .swatch-box:hover {
      transform: scale(1.08);
      box-shadow:0px 15px 25px rgba(0,0,0,0.45);
      }
    <style>
    """
    st.markdown(swatch_css , unsafe_allow_html=True)

    for i, c in enumerate(colors):
        with cols[i]:
            st.markdown(
                f"""
                <div class="swatch-box" style="background:{c}; margin-top:25px;"></div>
                """,
                unsafe_allow_html=True
            )
            st.markdown(f"<p style='text-align:center; font-weight:bold;'>{c}</p>", unsafe_allow_html=True)