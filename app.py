import streamlit as st
from google import genai
import re

st.set_page_config(page_title="Telugu Story & Prompt Book", page_icon="📖")
st.title("📖 తెలుగు స్టోరీ & ఇలస్ట్రేషన్ ప్రాంప్ట్ బుక్")
st.write("మీ ఆలోచనను తెలుగులో ఇవ్వండి, పర్‌ఫెక్ట్ కథ మరియు బొమ్మల కోసం AI ప్రాంప్ట్స్ వస్తాయి!")

api_key = st.text_input("మీ Gemini API Key ఇవ్వండి:", type="password")
prompt = st.text_area("మీ కథ లేదా సీన్ గురించి తెలుగులో టైప్ చేయండి: (ఉదాహరణకు: ఒక అబ్బాయి సైకిల్ మీద బడికి వెళ్తున్నాడు)")

if st.button("కథ & ప్రాంప్ట్స్ తయారు చేయి"):
    if api_key and prompt:
        try:
            client = genai.Client(api_key=api_key)
            
            story_prompt = f"""
            నిపుణుడైన పిల్లల కథల రచయిత మరియు ఇలస్ట్రేటర్ లాగా వ్యవహరించండి.
            ఈ క్రింది భావన ఆధారంగా: '{prompt}', దీనిని **3 లేదా 4 చిన్న భాగాలుగా (Scenes)** విభజించి ఒక అందమైన కథలా **పూర్తిగా తెలుగులో** రాయండి.
            ప్రతి సీన్‌కి ఈ క్రింది విధంగా స్పష్టంగా ఫార్మాట్ చేయండి:
            
            ### సీన్ [నంబర్]
            - **కథ వివరణ:** [ఈ సీన్ లో ఏం జరుగుతుందో తెలుగులో రాయండి]
            - **ఇలస్ట్రేషన్ ప్రాంప్ట్ (English):** [ఈ సీన్‌ని DALL-E లేదా Midjourney లో వేస్తే పర్‌ఫెక్ట్ బొమ్మ వచ్చేలా చాలా స్పష్టమైన ఇంగ్లీష్ ఇలస్ట్రేషన్ ప్రాంప్ట్ రాయండి, ఉదాహరణకు: children's book illustration, vibrant watercolor style, cute characters...]
            """
            
            with st.spinner("కథ మరియు ప్రాంప్ట్స్ తయారవుతున్నాయి..."):
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=[story_prompt],
                )
            
            if response.text:
                st.success("మీ స్టోరీ బుక్ మరియు ఇలస్ట్రేషన్ ప్రాంప్ట్స్ సిద్ధంగా ఉన్నాయి!")
                st.markdown(response.text)
                st.info("💡 సూచన: పైన ఇచ్చిన ఇంగ్లీష్ 'ఇలస్ట్రేషన్ ప్రాంప్ట్' ను కాపీ చేసి ChatGPT (DALL-E) లేదా Bing Image Creator లో పేస్ట్ చేస్తే అద్భుతమైన ఒరిజినల్ బొమ్మలు వస్తాయి!")
            else:
                st.warning("ఏదైనా సమాచారం రాలేదు, దయచేసి మళ్ళీ ప్రయత్నించండి.")
        except Exception as e:
            st.error(f"లోపం జరిగింది: {e}")
    else:
        st.warning("దయచేసి API Key మరియు సీన్ వివరాలు ఇవ్వండి.")
