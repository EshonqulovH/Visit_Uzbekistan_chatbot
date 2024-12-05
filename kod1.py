import streamlit as st
import openai
import streamlit as st
import folium
from streamlit_folium import st_folium

# Sahifa sozlamalari
st.set_page_config(
    page_title="O‘zbekistonga Xush kelibsiz",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Session state'da til, sahifa holati va API kalitni boshqarish
if "language" not in st.session_state:
    st.session_state["language"] = None
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"
if "api_key" not in st.session_state:
    st.session_state["api_key"] = None

# OpenAI API kalitni o'rnatish
if st.session_state["api_key"]:
    openai.api_key = st.session_state["api_key"]

# Orqa fon tasvirlari
background_urls = {
    "home": "https://sudex.uz/wp-content/uploads/2021/11/72cef04923577cc395792d82b5acbe0b.jpg",
    "historical_sites": "https://static.zarnews.uz/crop/5/9/720__80_59687f917a0d46685a52ec8fe7c04138.jpg?img=self&v=1626171787",
    "historical_figures": "https://daryo.uz/static/2023/03/6423eaff9e4e5.jpg",
    "travel_start": "https://media.tehrantimes.com/d/t/2024/06/11/4/5023325.jpg?ts=1718112763961",
}
current_background = background_urls.get(st.session_state["current_page"], "")

# CSS orqali orqa fonni sozlash
st.markdown(
    f"""
    <style>
    /* Tana uchun umumiy fon */
    body {{
        background-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('{current_background}');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
    }}
    /* Asosiy ilova o'rnatmalarini o'zgartirish */
    .stApp {{
        background: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        max-width: 900px;
        margin: 2rem auto;
        animation: fadeIn 2s ease-in-out;
    }}
    /* Tugmalar uchun animatsiya */
    button {{
        background-color: #007BFF;
        border: none;
        color: white;
        padding: 10px 20px;
        text-align: center;
        font-size: 16px;
        border-radius: 5px;
        transition: transform 0.3s ease, background-color 0.3s ease;
    }}
    button:hover {{
        background-color: #0056b3;
        transform: scale(1.05);
    }}
    /* Matn uchun animatsiyalar */
    @keyframes fadeIn {{
        from {{
            opacity: 0;
        }}
        to {{
            opacity: 1;
        }}
    }}
    h1, h2, h3 {{
        font-family: 'Helvetica', sans-serif;
        animation: fadeIn 2s ease-in-out;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)
# Til tanlash funksiyasi
def set_language(lang):
    st.session_state["language"] = lang

# Sahifani o'zgartirish funksiyasi
def change_page(page):
    st.session_state["current_page"] = page

# Til tanlash sahifasi
if st.session_state["language"] is None:
    st.title("Tilni tanlang | Выберите язык | Select Language")
    st.button("O‘zbekcha", on_click=lambda: set_language("uz"))
    st.button("Русский", on_click=lambda: set_language("ru"))
    st.button("English", on_click=lambda: set_language("en"))

# API kalitni kiritish sahifasi
elif st.session_state["api_key"] is None:
    api_texts = {
        "uz": {
            "title": "API Kalitni kiriting",
            "label": "OpenAI API Kalitni kiriting:",
            "button": "Tasdiqlash",
            "success": "API kalit muvaffaqiyatli kiritildi. Davom eting!",
            "error": "API kalitni kiritish shart!",
            "welcome": "O'zbekistonga xush kelibsiz!",
        },
        "ru": {
            "title": "Введите API ключ",
            "label": "Введите API ключ OpenAI:",
            "button": "Подтвердить",
            "success": "API ключ успешно введен. Продолжайте!",
            "error": "Необходимо ввести API ключ!",
            "welcome": "Добро пожаловать в Узбекистан!",
        },
        "en": {
            "title": "Enter API Key",
            "label": "Enter OpenAI API Key:",
            "button": "Submit",
            "success": "API key successfully entered. Proceed!",
            "error": "API key is required!",
            "welcome": "Welcome to Uzbekistan!",
        },
    }

    lang = st.session_state["language"]
    t = api_texts[lang]

    st.markdown(f"<h1 style='text-align: center; color: green;'>{t['welcome']}</h1>", unsafe_allow_html=True)  # Xush kelibsiz matni katta va yashil
    st.title(t["title"])
    
    api_key_input = st.text_input(t["label"], type="password")
    if st.button(t["button"]):
        if api_key_input:
            st.session_state["api_key"] = api_key_input
            openai.api_key = api_key_input
            st.success(t["success"])
        else:
            st.error(t["error"])

# Asosiy dastur
else:
    translations = {
        "uz": {
            "home": "🏠 Bosh sahifa",
            "main_text":  """
                **O‘zbekiston Respublikasi** — Markaziy Osiyoda joylashgan mustaqil davlat. 
                1991-yil 1-sentabr kuni O‘zbekiston Sovet Ittifoqidan mustaqilligini e'lon qilgan.
                
                **Tarixiy davrlar**:
                - Qadimgi davrlarda So‘g‘diyona, Baqtriya va Xorazm kabi davlatlar bo‘lgan.
                - Miloddan avvalgi IV asrda Aleksandr Makedonskiy yurishlari.
                - VII-VIII asrlarda Arab xalifaligi hukmronligi.
                - IX-XII asrlarda ilm-fan va madaniyat markazi.
                - XIV asrda Amir Temur davlatining tashkil etilishi.
                - 1991-yilda mustaqillikka erishgan.

                **Geografik joylashuvi**:
                - sharqda Tojikiston va Qirg‘iziston bilan,
                - g‘arbda Turkmaniston bilan,
                - shimolda Qozog‘iston bilan,
                - janubda Afg‘oniston bilan chegaradosh.

                **Poytaxti**: Toshkent shahri.
            """,
            "historical_sites": "🏛️ Tarixiy obidalar",
            "welcome_text_historical_sites": "Siz bu sahifada Tarixiy obidalar bo'yicha ma'lumot olishingiz mumkin",
            "historical_figures": "👤 Tarixiy shaxslar",
            "welcome_text_historical_figures": "Siz bu sahifada Tarixiy shaxslar bo'yicha ma'lumot olishingiz mumkin",
            "travel_start": "🚶‍♂️ Sayohatni boshlash",
            "welcome_text_travel_start": "Siz bu sahifada O'zbekiston bo'ylab sayohat qilishingiz mumkin",
            "chatbot_home": "🏠 Bosh sahifa uchun Chatbot",
            "chatbot_historical_sites": "🏛️ Tarixiy obidalar uchun Chatbot",
            "chatbot_historical_figures": "👤 Tarixiy shaxslar uchun Chatbot",
            "chatbot_travel_start": "🚶‍♂️ Sayohatni boshlash uchun Chatbot"
        },
        "ru": {
            "home": "🏠 Главная",
            "main_text": """
                **Республика Узбекистан** — независимое государство, расположенное в Центральной Азии. 
                1 сентября 1991 года Узбекистан провозгласил свою независимость от Советского Союза.
                
                **Исторические эпохи**:
                - В древности здесь находились Согдиана, Бактрия и Хорезм.
                - В IV веке до н.э. походы Александра Македонского.
                - В VII-VIII веках правление Арабского халифата.
                - В IX-XII веках центр науки и культуры.
                - В XIV веке основание государства Амиром Темуром.
                - В 1991 году обретение независимости.

                **Географическое расположение**:
                - На востоке граничит с Таджикистаном и Кыргызстаном,
                - на западе с Туркменистаном,
                - на севере с Казахстаном,
                - на юге с Афганистаном.

                **Столица**: город Ташкент.
            """,
            "historical_sites": "🏛️ Исторические памятники",
            "welcome_text_historical_sites": "На этой странице вы можете получить информацию о исторических памятниках.",
            "historical_figures": "👤 Исторические личности",
            "welcome_text_historical_figures": "На этой странице вы можете получить информацию о исторических личностях.",
            "travel_start": "🚶‍♂️ Начать путешествие",
            "welcome_text_travel_start": "На этой странице вы можете путешествовать по Узбекистану.",
            "chatbot_home": "🏠 Чатбот для Главной страницы",
            "chatbot_historical_sites": "🏛️ Чатбот для Исторических памятников",
            "chatbot_historical_figures": "👤 Чатбот для Исторических личностей",
            "chatbot_travel_start": "🚶‍♂️ Чатбот для Начала путешествия",
        },
        "en": {
            "home": "🏠 Home",
            "main_text":  """
                **Republic of Uzbekistan** — an independent state located in Central Asia. 
                On September 1, 1991, Uzbekistan declared its independence from the Soviet Union.
                
                **Historical Eras**:
                - Ancient states like Sogdiana, Bactria, and Khorezm.
                - Campaigns of Alexander the Great in the 4th century BCE.
                - Arab Caliphate rule in the 7th-8th centuries.
                - Center of science and culture in the 9th-12th centuries.
                - Foundation of the Timurid state in the 14th century.
                - Independence achieved in 1991.

                **Geographical location**:
                - Borders Tajikistan and Kyrgyzstan to the east,
                - Turkmenistan to the west,
                - Kazakhstan to the north,
                - Afghanistan to the south.

                **Capital**: Tashkent.
            """,
            "historical_sites": "🏛️ Historical Sites",
            "welcome_text_historical_sites": "On this page, you can find information about historical monuments.",
            "historical_figures": "👤 Historical Figures",
            "welcome_text_historical_figures": "On this page, you can find information about historical figures.",
            "travel_start": "🚶‍♂️ Start Your Journey",
            "welcome_text_travel_start": "On this page, you can travel across Uzbekistan.",
            "chatbot_home": "🏠 Chatbot for Home",
            "chatbot_historical_sites": "🏛️ Chatbot for Historical Sites",
            "chatbot_historical_figures": "👤 Chatbot for Historical Figures",
            "chatbot_travel_start": "🚶‍♂️ Chatbot for Travel Start",
        },
    }

    lang = st.session_state["language"]
    t = translations[lang]

    # Yon panel
    st.sidebar.markdown("### 🧭 Menu")
    st.sidebar.button(t["home"], on_click=lambda: change_page("home"))
    st.sidebar.button(t["historical_sites"], on_click=lambda: change_page("historical_sites"))
    st.sidebar.button(t["historical_figures"], on_click=lambda: change_page("historical_figures"))
    st.sidebar.button(t["travel_start"], on_click=lambda: change_page("travel_start"))

    # Sahifa mazmuni
    if st.session_state["current_page"] == "home":
        st.title(t["home"])
        st.write(t["main_text"])

        # Home sahifasi uchun chatbot
        if "messages_home" not in st.session_state:
            st.session_state["messages_home"] = []

        if "history" not in st.session_state:
            st.session_state["history"] = []  # Javoblarni saqlash uchun

        st.markdown(f"### {t['chatbot_home']}")
        user_input = st.text_input("Savol bering (Home):", key="input_home")
        if st.button("Enter", key="send_home"):
            if user_input:
                st.session_state["messages_home"].append({"role": "user", "content": user_input})

                try:

                    system_prompt = """
                                    You are an expert on Uzbekistan and provide clear and concise answers. 
                                    If asked about other countries, respond with, "I only have knowledge about Uzbekistan." 
                                    You can also answer questions on social, economic, and political matters. 
                                    However, you do not provide information about historical monuments or historical figures. 
                                    If someone asks about historical figures or monuments, respond with, 
                                    "You can find information on this through our next page."
                                    """

                    response = openai.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            *st.session_state["messages_home"]
                        ]
                    )
                    # Botning javobini olish
                    bot_response = response.choices[0].message.content
                    st.session_state["messages_home"].append({"role": "bot", "content": bot_response})
                    
                    # Javobni tarixga saqlash
                    st.session_state["history"].append({
                        "question": user_input,
                        "answer": bot_response
                    })
                except Exception as e:
                    # Xatolik yuzaga kelsa
                    bot_response = "Error: Unable to fetch a response. Please try again later."
                    st.session_state["messages_home"].append({"role": "bot", "content": bot_response})

        # Xabarlarni ko‘rsatish
        st.subheader("Chat:")
        for message in st.session_state["messages_home"]:
            role = "👤" if message["role"] == "user" else "🤖"
            st.write(f"{role} {message['content']}")

        # Refresh tugmasi
        if st.button("Refresh chat"):
            st.session_state["messages_home"] = []  # Chatni tozalash

        # Tarixni ko‘rsatish
        st.subheader("(Tarix,История,History):")
        for record in st.session_state["history"]:
            st.write(f"**Savol**: {record['question']}")
            st.write(f"**Javob**: {record['answer']}")


    elif st.session_state["current_page"] == "historical_sites":
        st.title(t["historical_sites"])
        st.write(t["welcome_text_historical_sites"])

        # Historical Sites sahifasi uchun chatbot
        if "messages_historical_sites" not in st.session_state:
            st.session_state["messages_historical_sites"] = []

        st.markdown(f"### {t['chatbot_historical_sites']}")
        
        if "history_city" not in st.session_state:
            st.session_state["history_city"] = []  # Javoblarni saqlash uchun

        # Foydalanuvchi kiritmasi
        user_input = st.text_input("Savol bering (Historical Sites):", key="input_historical_sites")
        if st.button("Enter", key="send_historical_sites"):
            if user_input:
                # Foydalanuvchi xabarini qo‘shish
                st.session_state["messages_historical_sites"].append({"role": "user", "content": user_input})
                try:
                    # Sistem prompt
                    system_prompt1 = """
                    You are a specialist in historical monuments located exclusively in Uzbekistan. 
                    You provide concise and precise answers only about historical monuments in Uzbekistan. 
                    If asked about monuments outside of Uzbekistan, you respond with: 
                    'I only have expertise in historical monuments located in Uzbekistan.' 
                    If asked about other topics, you respond with: 
                    'I am a specialist only in historical monuments.'
                    """
                    
                    # ChatGPT API orqali javob olish
                    response = openai.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": system_prompt1},
                            *st.session_state["messages_historical_sites"]
                        ]
                    )
                    # Botning javobini olish
                    bot_response = response.choices[0].message.content
                    st.session_state["messages_historical_sites"].append({"role": "bot", "content": bot_response})
                    
                    # Javobni tarixga saqlash
                    st.session_state["history_city"].append({
                        "question": user_input,
                        "answer": bot_response
                    })
                except Exception as e:
                    # Xatolik yuzaga kelsa
                    bot_response = "Error: Unable to fetch a response. Please try again later."
                    st.session_state["messages_historical_sites"].append({"role": "bot", "content": bot_response})

        # Xabarlarni ko‘rsatish
        st.subheader("Chat:")
        for message in st.session_state["messages_historical_sites"]:
            role = "👤" if message["role"] == "user" else "🤖"
            st.write(f"{role} {message['content']}")

        # Refresh tugmasi
        if st.button("Refresh chat"):
            st.session_state["messages_historical_sites"] = []  # Chatni tozalash

        # Tarixni ko‘rsatish
        st.subheader("(Tarix,История,History):")
        for record in st.session_state["history_city"]:
            st.write(f"**Savol**: {record['question']}")
            st.write(f"**Javob**: {record['answer']}")


    elif st.session_state["current_page"] == "historical_figures":
        st.title(t["historical_figures"])
        st.write(t["welcome_text_historical_figures"])

        # Historical Figures sahifasi uchun chatbot
        if "messages_historical_figures" not in st.session_state:
            st.session_state["messages_historical_figures"] = []

        if "history_figure" not in st.session_state:
            st.session_state["history_figure"] = []  # Javoblarni saqlash uchun

        st.markdown(f"### {t['chatbot_historical_figures']}")

        user_input = st.text_input("Savol bering (Historical Figures):", key="input_historical_figures")
        if st.button("Enter", key="send_historical_figures"):
            if user_input:
                st.session_state["messages_historical_figures"].append({"role": "user", "content": user_input})
                try:
                    system_prompt2 = """
                                    You are a specialist in historical figures and great scholars exclusively from Uzbekistan. 
                                    You provide concise and precise answers only about historical figures from Uzbekistan. 
                                    If asked about individuals outside of Uzbekistan, you respond with: 
                                    'I only have information about historical figures from Uzbekistan.' 
                                    If asked about other topics, you respond with: 
                                    'I can only provide information about historical figures.'
                                    """

                    # ChatGPT API orqali javob olish
                    response = openai.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": system_prompt2},
                            *st.session_state["messages_historical_figures"]
                        ]
                    )
                    # Botning javobini olish
                    bot_response = response.choices[0].message.content
                    st.session_state["messages_historical_figures"].append({"role": "bot", "content": bot_response})
                    
                    # Javobni tarixga saqlash
                    st.session_state["history_figure"].append({
                        "question": user_input,
                        "answer": bot_response
                    })
                except Exception as e:
                    # Xatolik yuzaga kelsa
                    bot_response = "Error: Unable to fetch a response. Please try again later."
                    st.session_state["messages_historical_figures"].append({"role": "bot", "content": bot_response})

        # Xabarlarni ko‘rsatish
        st.subheader("Chat:")
        for message in st.session_state["messages_historical_figures"]:
            role = "👤" if message["role"] == "user" else "🤖"
            st.write(f"{role} {message['content']}")

        # Refresh tugmasi
        if st.button("Refresh chat"):
            st.session_state["messages_historical_figures"] = []  # Chatni tozalash

        # Tarixni ko‘rsatish
        st.subheader("(Tarix,История,History):")
        for record in st.session_state["history_figure"]:
            st.write(f"**Savol**: {record['question']}")
            st.write(f"**Javob**: {record['answer']}")


    elif st.session_state["current_page"] == "travel_start":
        st.title(t["travel_start"])
        st.write(t["welcome_text_travel_start"])

        # Xizmatlarni tanlash (Taxi, Poyezd, Samolyot)
        st.markdown("### Xizmatlar")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🚕 Taxi", key="taxi"):
                st.session_state["selected_service"] = "taxi"
                st.success("Taxi xizmati tanlandi! Batafsil ma'lumot uchun quyida savol bering.")

        with col2:
            if st.button("🚆 Poyezd", key="train"):
                st.session_state["selected_service"] = "train"
                st.success("Poyezd xizmati tanlandi! Batafsil ma'lumot uchun quyida savol bering.")

        with col3:
            if st.button("✈️ Samolyot", key="airplane"):
                st.session_state["selected_service"] = "airplane"
                st.success("Samolyot xizmati tanlandi! Batafsil ma'lumot uchun quyida savol bering.")

        # Xarita funksiyasi
        st.markdown("### 📍 Bormoqchi bo'lgan joyingizni belgilang:")
        # Standart Toshkent markazi koordinatalari
        m = folium.Map(location=[41.2995, 69.2401], zoom_start=10)

        # Xarita interfeysini ko'rsatish (kichraytirilgan o'lchamlar bilan)
        output = st_folium(m, width=500, height=300)

        # Foydalanuvchi tanlagan joyni olish
        if output["last_clicked"] is not None:
            location = output["last_clicked"]
            st.session_state["selected_location"] = location
            st.success(f"Tanlangan joy: Kenglik: {location['lat']}, Uzunlik: {location['lng']}")

        # Chatbot funksiyasi
        if "messages_travel_start" not in st.session_state:
            st.session_state["messages_travel_start"] = []

        st.markdown(f"### {t['chatbot_travel_start']}")
        user_input = st.text_input("Savol bering (Travel Start):", key="input_travel_start")
        if st.button("Enter", key="send_travel_start"):
            if user_input:
                st.session_state["messages_travel_start"].append({"role": "user", "content": user_input})
                try:
                    # Xizmatga mos javoblar uchun maxsus model yaratish
                    service = st.session_state.get("selected_service", "general")
                    system_content = "You are an assistant providing travel guidance in Uzbekistan."
                    if service == "taxi":
                        system_content += " Focus on taxi-related queries and services."
                    elif service == "train":
                        system_content += " Focus on train-related queries and schedules."
                    elif service == "airplane":
                        system_content += " Focus on flight-related queries and tickets."

                    # Tanlangan joyni javobga qo'shish
                    if "selected_location" in st.session_state:
                        location_info = f" User's selected location is Latitude: {st.session_state['selected_location']['lat']}, Longitude: {st.session_state['selected_location']['lng']}."
                        system_content += location_info

                    response = openai.ChatCompletion.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_content},
                            *st.session_state["messages_travel_start"]
                        ]
                    )
                    bot_response = response.choices[0].message.content
                    st.session_state["messages_travel_start"].append({"role": "bot", "content": bot_response})
                except Exception as e:
                    bot_response = "Error: Unable to fetch a response. Please try again later."
                    st.session_state["messages_travel_start"].append({"role": "bot", "content": bot_response})

        # Xabarlarni ko'rsatish
        for message in st.session_state["messages_travel_start"]:
            role = "👤" if message["role"] == "user" else "🤖"
            st.write(f"{role} {message['content']}")