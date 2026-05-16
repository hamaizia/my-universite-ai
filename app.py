import streamlit as st
from datetime import datetime, timedelta
import json
import os
import glob

# === 1. لغة الهاتف أوتوماتيك ===
try:
    lang = st.context.headers.get("Accept-Language", "ar")[:2].lower()
except:
    lang = "ar"

# === 2. الترجمة ===
text = {
    "ar": {
        "title": "🌍 جامعتي الذكية العالمية",
        "subtitle": "إجابات من جامعات العالم | كل دولة في ملف منفصل",
        "header": "1. اختار البلد والتخصص",
        "country": "البلد",
        "major": "التخصص",
        "button": "جاوبني",
        "result": "إجابة عن تخصص",
        "in": "في",
        "answer_from": "📚 الإجابة الملخصة من المصادر الرسمية:",
        "warning": "⚠️ اختار بلد وتخصص",
        "search": "ابحث...",
        "footer": "المعلومات من مواقع الجامعات الرسمية | صنع hamaizia ❤️",
        "rule": "🚫 كل الإجابات ملخصة من مواقع الجامعات الرسمية فقط.",
        "ad_banner": "📢 مساحة إعلانية - ادعم التطبيق",
        "ad_required": "⚠️ شاهد إعلان للمتابعة",
        "ad_button": "شاهد الإعلان الآن",
        "limit_reached": "❌ وصلت للحد: 20 سؤال",
        "wait": "⏰ انتظر 3 ساعات أو",
        "watch_ad": "شاهد إعلان لفتح 20 سؤال إضافي",
        "questions_left": "الأسئلة المتبقية",
        "no_data": "لا توجد بيانات لهذا التخصص",
        "source": "المصدر",
        "no_summary": "⚠️ لا يوجد ملخص لهذه الجامعة بعد",
        "file_error": "❌ ما لقيتش مجلد databases أو الملفات فارغة! أنشئ مجلد databases وحط فيه ملفات json",
        "show_source": "📎 اذكر المصدر",
        "new_search": "🔄 بحث جديد"
    },
    "en": {
        "title": "🌍 My Smart University Global",
        "subtitle": "Answers from universities worldwide | Each country in separate file",
        "header": "1. Choose Country and Major",
        "country": "Country",
        "major": "Major",
        "button": "Answer",
        "result": "Answer about",
        "in": "in",
        "answer_from": "📚 Summarized answer from official sources:",
        "warning": "⚠️ Choose country and major",
        "search": "Search...",
        "footer": "Info from official university websites | Made by hamaizia ❤️",
        "rule": "🚫 All answers are summarized from official university websites only.",
        "ad_banner": "📢 Ad Space - Support the App",
        "ad_required": "⚠️ Watch an ad to continue",
        "ad_button": "Watch Ad Now",
        "limit_reached": "❌ Limit reached: 20 questions",
        "wait": "⏰ Wait 3 hours or",
        "watch_ad": "Watch ad to unlock 20 more questions",
        "questions_left": "Questions left",
        "no_data": "No data for this major",
        "source": "Source",
        "no_summary": "⚠️ No summary available for this university yet",
        "file_error": "❌ databases folder not found or empty! Create databases folder with json files",
        "show_source": "📎 Show Source",
        "new_search": "🔄 New Search"
    },
    "fr": {
        "title": "🌍 Mon Université Intelligente Mondiale",
        "subtitle": "Réponses des universités du monde | Chaque pays dans un fichier",
        "header": "1. Choisissez Pays et Spécialité",
        "country": "Pays",
        "major": "Spécialité",
        "button": "Répondre",
        "result": "Réponse sur",
        "in": "en/au",
        "answer_from": "📚 Réponse résumée des sources officielles:",
        "warning": "⚠️ Choisissez pays et spécialité",
        "search": "Rechercher...",
        "footer": "Infos des sites officiels des universités | Créé par hamaizia ❤️",
        "rule": "🚫 Toutes les réponses sont résumées depuis les sites officiels des universités uniquement.",
        "ad_banner": "📢 Espace Pub - Soutenez l'App",
        "ad_required": "⚠️ Regardez une pub pour continuer",
        "ad_button": "Regarder Pub",
        "limit_reached": "❌ Limite atteinte: 20 questions",
        "wait": "⏰ Attendez 3h ou",
        "watch_ad": "Regardez une pub pour débloquer 20 questions",
        "questions_left": "Questions restantes",
        "no_data": "Pas de données pour cette spécialité",
        "source": "Source",
        "no_summary": "⚠️ Pas de résumé disponible pour cette université",
        "file_error": "❌ Dossier databases introuvable ou vide! Créez dossier databases avec fichiers json",
        "show_source": "📎 Afficher Source",
        "new_search": "🔄 Nouvelle Recherche"
    }
}

if lang not in text:
    lang = "ar"
t = text[lang]

# === 3. نظام الإعلانات والحد + حالة البحث ===
if 'question_count' not in st.session_state:
    st.session_state.question_count = 0
if 'blocked_until' not in st.session_state:
    st.session_state.blocked_until = None
if 'search_done' not in st.session_state:
    st.session_state.search_done = False

# === 4. تحميل قاعدة البيانات من مجلد databases - كل دولة ملف ===
@st.cache_data
def load_database():
    database = {}
    db_files = glob.glob('databases/*.json')

    if not db_files:
        st.error(t["file_error"])
        st.stop()

    for file_path in db_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                database.update(data)
        except Exception as e:
            st.warning(f"⚠️ خطأ في قراءة الملف {file_path}: {e}")

    if not database:
        st.error(t["file_error"])
        st.stop()

    return database

database = load_database()

# === 5. نستخرجو الدول والتخصصات الموجودة ===
all_keys = list(database.keys())
all_countries = sorted(list(set([key.split('_')[0] for key in all_keys])))
all_majors_by_country = {}

for key in all_keys:
    country, major = key.split('_', 1)
    if country not in all_majors_by_country:
        all_majors_by_country[country] = []
    all_majors_by_country[country].append(major)

# === 6. الواجهة ===
st.set_page_config(page_title=t["title"], page_icon="🌍", layout="wide")
st.markdown(f"<div style='background:#FF4B4B;padding:10px;border-radius:5px;text-align:center;color:white;font-weight:bold;'>{t['ad_banner']} - 728x90</div>", unsafe_allow_html=True)
st.title(t["title"])
st.info(t["rule"])
st.write(t["subtitle"])

# التحقق من الحظر
if st.session_state.blocked_until:
    remaining = st.session_state.blocked_until - datetime.now()
    if remaining.total_seconds() > 0:
        h, m = int(remaining.total_seconds() // 3600), int((remaining.total_seconds() % 3600) // 60)
        st.error(f'{t["limit_reached"]}')
        st.warning(f'{t["wait"]}: {h} س و {m} د')
        if st.button(t["watch_ad"]):
            st.session_state.blocked_until = None
            st.session_state.question_count = 0
            st.rerun()
        st.stop()
    else:
        st.session_state.blocked_until = None
        st.session_state.question_count = 0

st.sidebar.metric(t["questions_left"], 20 - st.session_state.question_count)
st.header(t["header"])

# اختيار البلد والتخصص
col1, col2 = st.columns(2)
with col1:
    country = st.selectbox(t["country"], all_countries, key="country_select")
with col2:
    majors_for_country = sorted(all_majors_by_country.get(country, []))
    if majors_for_country:
        major = st.selectbox(t["major"], majors_for_country, help=t["search"], key="major_select")
    else:
        st.warning(t["no_data"])
        major = None

# خيار إظهار المصدر
show_source = st.checkbox(t["show_source"], value=False)

# أزرار البحث والرجوع
col_btn1, col_btn2 = st.columns([3, 1])

with col_btn1:
    search_btn = st.button(t["button"], type="primary", use_container_width=True, disabled=not major)

with col_btn2:
    if st.session_state.search_done:
        if st.button(t["new_search"], use_container_width=True):
            st.session_state.search_done = False
            st.rerun()

# تنفيذ البحث
if search_btn and major:
    st.session_state.search_done = True

    # إعلان كل 5 أسئلة
    if st.session_state.question_count > 0 and st.session_state.question_count % 5 == 0:
        st.warning(t["ad_required"])
        if st.button(t["ad_button"]):
            st.rerun()
        st.stop()

    st.session_state.question_count += 1
    if st.session_state.question_count >= 20:
        st.session_state.blocked_until = datetime.now() + timedelta(hours=3)
        st.rerun()

# عرض النتائج
if st.session_state.search_done and major:
    key = f"{country}_{major}"
    st.subheader(f'{t["result"]} {major} {t["in"]} {country}:')

    if key in database and database[key]:
        st.markdown(f"### {t['answer_from']}")

        for i, uni in enumerate(database[key], 1):
            with st.container():
                st.markdown(f"**{i}. {uni['name']}**")
                if 'summary' in uni:
                    st.write(uni['summary'])
                else:
                    st.warning(t["no_summary"])

                if show_source:
                    st.caption(f"{t['source']}: [{uni['url']}]({uni['url']})")

                st.markdown("---")
    else:
        st.warning(t["no_data"])
        st.session_state.search_done = False

st.markdown("---")
st.write(t["footer"])
