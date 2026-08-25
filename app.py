import streamlit as st
from google import genai

st.set_page_config(page_title="Telugu Story & Prompt Book", page_icon="📖")

st.title("📖 తెలుగు స్టోరీ & ఇలస్ట్రేషన్ ప్రాంప్ట్ బుక్")
st.write("మీ ఆలోచనను తెలుగులో ఇవ్వండి, పర్ఫెక్ట్ కథ మరియు బొమ్మల కోసం AI ప్రాంప్ట్స్ వస్తాయి!")

# Streamlit Secrets నుండి API Key ని ఆటోమేటిక్‌గా తీసుకోవడం (మళ్లీ మళ్లీ అడగదు)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = None

# ఒకవేళ Secrets లో కీ లేకపోతే మాత్రమే బాక్స్ చూపుతుంది (సెఫ్టీ కోసం)
if not api_key:
    api_key = st.text_input("మీ Gemini API Key ఇవ్వండి:", type="password")

story_input = st.text_area("మీ కథ లేదా సీన్ గురించి తెలుగులో టైప్ చేయండి: (ఉదాహరణకు: ఒక అబ్బాయి సైకిల్ మీద బడికి వెళ్తున్నాడు)")

if st.button("కథ & ప్రాంప్ట్ తయారు చేయి"):
    if not api_key:
        st.warning("దయచేసి API Key అందించండి.")
    elif not story_input:
        st.warning("దయచేసి సీన్ వివరాలు ఇవ్వండి.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            story_prompt = f"""
            మీరు నిపుణుడైన పిల్లల కథల రచయిత మరియు ఇలస్ట్రేటర్. 
            ఈ క్రింది భావన ఆధారంగా: '{story_input}'
            ప్రతి సీన్‌కి ఈ క్రింది విధంగా స్పష్టంగా ఫార్మాట్ చేయండి:
            
            ### సీన్ [నెంబర్]
            - **కథ వివరణ:** [ఈ సీన్ లో ఏం జరుగుతుందో తెలుగులో రాయండి]
            - **ఇలస్ట్రేషన్ ప్రాంప్ట్ (English):** [ఈ సీన్‌కి తగిన ఇమేజ్ ప్రాంప్ట్ ఇంగ్లీష్‌లో]
            """
            
            with st.spinner("కథ మరియు ప్రాంప్ట్స్ తయారవుతున్నాయి..."):
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[story_prompt],
                )
            
            if response and response.text:
                st.success("మీ స్టోరీ బుక్ మరియు ఇలస్ట్రేషన్ ప్రాంప్ట్స్ తయారయ్యాయి!")
                st.markdown(response.text)
                st.info("💡 సూచన: పైన ఇచ్చిన ఇంగ్లీష్ ప్రాంప్ట్‌లను ఉపయోగించి మీరు బొమ్మలు సృష్టించుకోవచ్చు.")
            else:
                st.warning("ఎదైనా సమాచారం రాలేదు, దయచేసి మళ్ళీ ప్రయత్నించండి.")
                
        except Exception as e:
            st.error(f"లోపం జరిగింది: {e}")
