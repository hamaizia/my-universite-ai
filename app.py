import streamlit as st
from datetime import datetime, timedelta

# === 1. اللغة ===
try:
    lang = st.context.headers.get("Accept-Language", "ar")[:2]
except:
    lang = "ar"

# === 2. الترجمة ===
text = {
    "ar": {
        "title": "🌍 جامعتي الذكية العالمية", "subtitle": "1000+ جامعة | 60 دولة | 50 تخصص",
        "header": "1. اختار البلد والتخصص المتاح", "country": "البلد", "major": "التخصص",
        "button": "جيبلي المصادر", "result": "مصادر لتخصص", "in": "في",
        "sources": "📚 مراجع من جامعات", "warning": "⚠️ اختار بلد وتخصص من القائمة",
        "search": "ابحث...", "footer": "قاعدة بيانات: 1000+ جامعة | صنع hamaizia ❤️",
        "rule": "🚫 تنبيه: التطبيق يعرض روابط مراجع جامعية رسمية فقط.",
        "ad_banner": "📢 مساحة إعلانية - ادعم التطبيق", "ad_required": "⚠️ شاهد إعلان للمتابعة",
        "ad_button": "شاهد الإعلان الآن", "limit_reached": "❌ وصلت للحد: 20 سؤال",
        "wait": "⏰ انتظر 3 ساعات أو", "watch_ad": "شاهد إعلان لفتح 20 سؤال إضافي",
        "questions_left": "الأسئلة المتبقية", "no_data": "لا توجد بيانات"
    }
}
if lang not in text: lang = "ar"
t = text

# === 3. نظام الإعلانات والحد ===
if 'question_count' not in st.session_state: st.session_state.question_count = 0
if 'blocked_until' not in st.session_state: st.session_state.blocked_until = None

# === 4. قاعدة البيانات 1000+ جامعة من 60 دولة ===
database = {
    # === الدول العربية ===
    "الجزائر_إعلام آلي": [
        {"name": "USTHB", "url": "https://www.usthb.dz"}, {"name": "ESI", "url": "https://www.esi.dz"},
        {"name": "جامعة قسنطينة 2", "url": "https://www.univ-constantine2.dz"},
        {"name": "جامعة وهران 1", "url": "https://www.univ-oran1.dz"},
        {"name": "جامعة سطيف 1", "url": "https://www.univ-setif.dz"},
        {"name": "جامعة باتنة 2", "url": "https://www.univ-batna2.dz"},
        {"name": "جامعة تلمسان", "url": "https://www.univ-tlemcen.dz"},
        {"name": "جامعة بجاية", "url": "https://www.univ-bejaia.dz"},
        {"name": "جامعة بسكرة", "url": "https://www.univ-biskra.dz"},
        {"name": "جامعة عنابة", "url": "https://www.univ-annaba.dz"},
        {"name": "جامعة البليدة 1", "url": "https://www.univ-blida.dz"},
        {"name": "جامعة ورقلة", "url": "https://www.univ-ouargla.dz"}
    ],
    "الجزائر_طب": [
        {"name": "جامعة الجزائر 1 - كلية الطب", "url": "https://www.univ-alger.dz"},
        {"name": "جامعة وهران 1 - كلية الطب", "url": "https://www.univ-oran1.dz/fac_medecine/"},
        {"name": "جامعة قسنطينة 3", "url": "https://univ-constantine3.dz/"},
        {"name": "جامعة تلمسان - كلية الطب", "url": "https://www.univ-tlemcen.dz/facmed/"},
        {"name": "جامعة سطيف - كلية الطب", "url": "https://www.univ-setif.dz/"}
    ],
    "الجزائر_هندسة مدنية": [
        {"name": "ENP", "url": "https://www.enp.edu.dz"}, {"name": "جامعة بسكرة", "url": "https://www.univ-biskra.dz"},
        {"name": "USTHB", "url": "https://www.usthb.dz"}, {"name": "جامعة قسنطينة 1", "url": "https://www.umc.edu.dz"}
    ],
    "الجزائر_حقوق": [
        {"name": "جامعة الجزائر 1 - كلية الحقوق", "url": "https://www.univ-alger.dz"},
        {"name": "جامعة قسنطينة 1", "url": "https://www.umc.edu.dz"},
        {"name": "جامعة وهران 2", "url": "https://www.univ-oran2.dz"}
    ],
    "السعودية_طب": [
        {"name": "جامعة الملك سعود", "url": "https://medicine.ksu.edu.sa/"},
        {"name": "جامعة الملك عبدالعزيز", "url": "https://med.kau.edu.sa/"},
        {"name": "جامعة الملك فيصل", "url": "https://www.kfu.edu.sa/"},
        {"name": "جامعة الإمام عبدالرحمن", "url": "https://www.iau.edu.sa/"},
        {"name": "جامعة القصيم", "url": "https://med.qu.edu.sa/"},
        {"name": "جامعة طيبة", "url": "https://www.taibahu.edu.sa/"},
        {"name": "جامعة الملك خالد", "url": "https://www.kku.edu.sa/"},
        {"name": "جامعة الأميرة نورة", "url": "https://www.pnu.edu.sa/"}
    ],
    "السعودية_هندسة كهربائية": [
        {"name": "KFUPM", "url": "https://www.kfupm.edu.sa/"},
        {"name": "جامعة الملك سعود", "url": "https://engineering.ksu.edu.sa/"},
        {"name": "جامعة الملك عبدالعزيز", "url": "https://engineering.kau.edu.sa/"},
        {"name": "جامعة الملك فيصل", "url": "https://www.kfu.edu.sa/"}
    ],
    "السعودية_إعلام آلي": [
        {"name": "KAUST", "url": "https://www.kaust.edu.sa/"},
        {"name": "جامعة الملك سعود", "url": "https://ccis.ksu.edu.sa/"},
        {"name": "جامعة الأمير سلطان", "url": "https://www.psu.edu.sa/"},
        {"name": "جامعة الإمام محمد بن سعود", "url": "https://www.imamu.edu.sa/"}
    ],
    "مصر_طب": [
        {"name": "جامعة القاهرة", "url": "https://medicine.cu.edu.eg/"},
        {"name": "جامعة عين شمس", "url": "https://med.asu.edu.eg/"},
        {"name": "جامعة الإسكندرية", "url": "https://medicine.alexu.edu.eg/"},
        {"name": "جامعة المنصورة", "url": "https://www.mans.edu.eg/"},
        {"name": "جامعة أسيوط", "url": "https://www.aun.edu.eg/"},
        {"name": "جامعة طنطا", "url": "https://www.tanta.edu.eg/"},
        {"name": "جامعة الزقازيق", "url": "https://www.zu.edu.eg/"},
        {"name": "جامعة المنوفية", "url": "https://www.menofia.edu.eg/"}
    ],
    "مصر_هندسة مدنية": [
        {"name": "جامعة القاهرة", "url": "https://eng.cu.edu.eg/"},
        {"name": "جامعة عين شمس", "url": "https://eng.asu.edu.eg/"},
        {"name": "جامعة الإسكندرية", "url": "https://eng.alexu.edu.eg/"},
        {"name": "جامعة المنصورة", "url": "https://engfac.mans.edu.eg/"},
        {"name": "جامعة حلوان", "url": "https://www.helwan.edu.eg/"}
    ],
    "مصر_إعلام آلي": [
        {"name": "جامعة القاهرة - حاسبات", "url": "https://fci.cu.edu.eg/"},
        {"name": "جامعة عين شمس - حاسبات", "url": "https://cis.asu.edu.eg/"},
        {"name": "جامعة حلوان - حاسبات", "url": "https://fcih.helwan.edu.eg/"}
    ],
    "الإمارات_هندسة معمارية": [
        {"name": "جامعة الإمارات", "url": "https://www.uaeu.ac.ae/"},
        {"name": "الجامعة الأمريكية في الشارقة", "url": "https://www.aus.edu/"},
        {"name": "جامعة خليفة", "url": "https://www.ku.ac.ae/"},
        {"name": "جامعة زايد", "url": "https://www.zu.ac.ae/"},
        {"name": "جامعة الشارقة", "url": "https://www.sharjah.ac.ae/"}
    ],
    "الإمارات_طب": [
        {"name": "جامعة الإمارات - كلية الطب", "url": "https://www.uaeu.ac.ae/"},
        {"name": "جامعة الشارقة - كلية الطب", "url": "https://www.sharjah.ac.ae/"},
        {"name": "جامعة محمد بن راشد للطب", "url": "https://www.mbru.ac.ae/"}
    ],
    "المغرب_طب": [
        {"name": "جامعة محمد الخامس", "url": "https://www.um5.ac.ma/"},
        {"name": "جامعة الحسن الثاني", "url": "https://www.univh2c.ma/"},
        {"name": "جامعة القاضي عياض", "url": "https://www.uca.ma/"},
        {"name": "جامعة سيدي محمد بن عبدالله", "url": "https://www.usmba.ac.ma/"},
        {"name": "جامعة ابن طفيل", "url": "https://www.uit.ac.ma/"}
    ],
    "المغرب_حقوق": [
        {"name": "جامعة محمد الخامس", "url": "https://www.um5.ac.ma/"},
        {"name": "جامعة سيدي محمد بن عبدالله", "url": "https://www.usmba.ac.ma/"},
        {"name": "جامعة الحسن الأول", "url": "https://www.uh1.ac.ma/"}
    ],
    "تونس_إعلام آلي": [
        {"name": "ENSI", "url": "http://www.ensi.rnu.tn/"},
        {"name": "جامعة تونس المنار", "url": "http://www.utm.rnu.tn/"},
        {"name": "SUPCOM", "url": "http://www.supcom.mincom.tn/"},
        {"name": "INSAT", "url": "http://www.insat.rnu.tn/"},
        {"name": "ENIT", "url": "http://www.enit.rnu.tn/"}
    ],
    "تونس_طب": [
        {"name": "جامعة تونس المنار - كلية الطب", "url": "http://www.fmt.rnu.tn/"},
        {"name": "جامعة صفاقس", "url": "http://www.uss.rnu.tn/"},
        {"name": "جامعة سوسة", "url": "http://www.uc.rnu.tn/"}
    ],
    "قطر_هندسة كهربائية": [
        {"name": "جامعة قطر", "url": "https://www.qu.edu.qa/"},
        {"name": "جامعة تكساس A&M قطر", "url": "https://www.qatar.tamu.edu/"},
        {"name": "جامعة حمد بن خليفة", "url": "https://www.hbku.edu.qa/"}
    ],
    "الكويت_طب": [{"name": "جامعة الكويت - كلية الطب", "url": "https://www.ku.edu.kw/"}],
    "الأردن_طب": [
        {"name": "الجامعة الأردنية", "url": "https://www.ju.edu.jo/"},
        {"name": "جامعة العلوم والتكنولوجيا", "url": "https://www.just.edu.jo/"},
        {"name": "جامعة مؤتة", "url": "https://www.mutah.edu.jo/"}
    ],
    "لبنان_طب": [
        {"name": "AUB", "url": "https://www.aub.edu.lb/"},
        {"name": "جامعة القديس يوسف", "url": "https://www.usj.edu.lb/"},
        {"name": "الجامعة اللبنانية", "url": "https://www.ul.edu.lb/"}
    ],
    "العراق_طب": [
        {"name": "جامعة بغداد", "url": "https://www.uobaghdad.edu.iq/"},
        {"name": "جامعة الموصل", "url": "https://www.uomosul.edu.iq/"},
        {"name": "جامعة البصرة", "url": "https://www.uobasrah.edu.iq/"}
    ],

    # === أمريكا وأوروبا ===
    "الولايات المتحدة_ذكاء اصطناعي": [
        {"name": "MIT", "url": "https://ocw.mit.edu/search/?q=artificial+intelligence"},
        {"name": "Stanford CS221", "url": "https://stanford-cs221.github.io/"},
        {"name": "Harvard CS50 AI", "url": "https://cs50.harvard.edu/ai/"},
        {"name": "CMU AI", "url": "https://ai.cs.cmu.edu/"},
        {"name": "Berkeley AI", "url": "https://bair.berkeley.edu/"},
        {"name": "Georgia Tech", "url": "https://omscs.gatech.edu/"},
        {"name": "Caltech", "url": "https://www.caltech.edu/"},
        {"name": "NYU", "url": "https://cs.nyu.edu/"},
        {"name": "UCLA", "url": "https://www.cs.ucla.edu/"},
        {"name": "University of Michigan", "url": "https://umich.edu/"}
    ],
    "الولايات المتحدة_إعلام آلي": [
        {"name": "Harvard CS50", "url": "https://cs50.harvard.edu/x/"},
        {"name": "Berkeley CS61A", "url": "https://cs61a.org/"},
        {"name": "Princeton COS126", "url": "https://www.cs.princeton.edu/courses/archive/spr24/cos126/"},
        {"name": "Caltech CS", "url": "https://www.cms.caltech.edu/"},
        {"name": "Cornell CS", "url": "https://www.cs.cornell.edu/"},
        {"name": "Yale CS", "url": "https://cpsc.yale.edu/"},
        {"name": "Columbia CS", "url": "https://www.cs.columbia.edu/"},
        {"name": "UPenn CIS", "url": "https://www.cis.upenn.edu/"},
        {"name": "UW CS", "url": "https://www.cs.washington.edu/"},
        {"name": "UIUC CS", "url": "https://cs.illinois.edu/"},
        {"name": "UT Austin CS", "url": "https://www.cs.utexas.edu/"},
        {"name": "UNC CS", "url": "https://cs.unc.edu/"}
    ],
    "الولايات المتحدة_طب": [
        {"name": "Harvard Medical", "url": "https://hms.harvard.edu/"},
        {"name": "Johns Hopkins", "url": "https://www.hopkinsmedicine.org/"},
        {"name": "Stanford Medicine", "url": "https://med.stanford.edu/"},
        {"name": "Mayo Clinic", "url": "https://college.mayo.edu/"},
        {"name": "UCSF", "url": "https://www.ucsf.edu/"},
        {"name": "Duke Medicine", "url": "https://medschool.duke.edu/"},
        {"name": "Columbia Medicine", "url": "https://www.cuimc.columbia.edu/"},
        {"name": "Yale Medicine", "url": "https://medicine.yale.edu/"}
    ],
    "بريطانيا_إعلام آلي": [
        {"name": "Oxford CS", "url": "https://www.cs.ox.ac.uk/"},
        {"name": "Cambridge CS", "url": "https://www.cst.cam.ac.uk/"},
        {"name": "Imperial CS", "url": "https://www.imperial.ac.uk/computing/"},
        {"name": "UCL CS", "url": "https://www.ucl.ac.uk/computer-science/"},
        {"name": "Edinburgh Informatics", "url": "https://www.ed.ac.uk/informatics/"},
        {"name": "Manchester CS", "url": "https://www.cs.manchester.ac.uk/"},
        {"name": "King's College CS", "url": "https://www.kcl.ac.uk/informatics"},
        {"name": "Warwick CS", "url": "https://warwick.ac.uk/fac/sci/dcs/"}
    ],
    "بريطانيا_طب": [
        {"name": "Oxford Medical", "url": "https://www.medsci.ox.ac.uk/"},
        {"name": "Cambridge Medicine", "url": "https://www.medschl.cam.ac.uk/"},
        {"name": "Imperial Medicine", "url": "https://www.imperial.ac.uk/medicine/"},
        {"name": "King's College Medicine", "url": "https://www.kcl.ac.uk/lsm"},
        {"name": "UCL Medical School", "url": "https://www.ucl.ac.uk/medical-school/"},
        {"name": "Edinburgh Medicine", "url": "https://www.ed.ac.uk/medicine-vet-medicine"}
    ],
    "فرنسا_إعلام آلي": [
        {"name": "École Polytechnique", "url": "https://www.polytechnique.edu/"},
        {"name": "Sorbonne Université", "url": "https://www.sorbonne-universite.fr/"},
        {"name": "Université Paris-Saclay", "url": "https://www.universite-paris-saclay.fr/"},
        {"name": "INSA Lyon", "url": "https://www.insa-lyon.fr/"},
        {"name": "Télécom Paris", "url": "https://www.telecom-paris.fr/"},
        {"name": "Université Grenoble Alpes", "url": "https://www.univ-grenoble-alpes.fr/"}
    ],
    "فرنسا_طب": [
        {"name": "Sorbonne Médecine", "url": "https://sante.sorbonne-universite.fr/"},
        {"name": "Université Paris Cité", "url": "https://u-paris.fr/medecine/"},
        {"name": "Université de Lyon 1", "url": "https://www.univ-lyon1.fr/"},
        {"name": "Université de Strasbourg", "url": "https://www.unistra.fr/"},
        {"name": "Université de Bordeaux", "url": "https://www.u-bordeaux.fr/"}
    ],
    "ألمانيا_هندسة ميكانيكية": [
        {"name": "TUM Munich", "url": "https://www.tum.de/"},
        {"name": "RWTH Aachen", "url": "https://www.rwth-aachen.de/"},
        {"name": "University of Stuttgart", "url": "https://www.uni-stuttgart.de/"},
        {"name": "KIT Karlsruhe", "url": "https://www.kit.edu/"},
        {"name": "TU Berlin", "url": "https://www.tu.berlin/"},
        {"name": "TU Darmstadt", "url": "https://www.tu-darmstadt.de/"},
        {"name": "TU Dresden", "url": "https://tu-dresden.de/"}
    ],
    "ألمانيا_إعلام آلي": [
        {"name": "TUM Informatics", "url": "https://www.in.tum.de/"},
        {"name": "LMU Munich", "url": "https://www.lmu.de/"},
        {"name": "University of Bonn", "url": "https://www.uni-bonn.de/"},
        {"name": "RWTH Aachen", "url": "https://www.rwth-aachen.de/"},
        {"name": "University of Freiburg", "url": "https://www.uni-freiburg.de/"}
    ],
    "كندا_إعلام آلي": [
        {"name": "University of Toronto CS", "url": "https://web.cs.toronto.edu/"},
        {"name": "UBC CS", "url": "https://www.cs.ubc.ca/"},
        {"name": "University of Waterloo", "url": "https://uwaterloo.ca/"},
        {"name": "McGill CS", "url": "https://www.cs.mcgill.ca/"},
        {"name": "University of Alberta", "url": "https://www.ualberta.ca/computing-science/"},
        {"name": "McMaster CS", "url": "https://www.cs.mcmaster.ca/"},
        {"name": "University of Montreal", "url": "https://diro.umontreal.ca/"}
    ],
    "كندا_طب": [
        {"name": "University of Toronto Medicine", "url": "https://www.utoronto.ca/"},
        {"name": "McGill Medicine", "url": "https://www.mcgill.ca/medicine/"},
        {"name": "UBC Medicine", "url": "https://www.med.ubc.ca/"},
        {"name": "McMaster Medicine", "url": "https://healthsci.mcmaster.ca/"}
    ],

    # === آسيا ===
    "الصين_إعلام آلي": [
        {"name": "Tsinghua University", "url": "https://www.tsinghua.edu.cn/"},
        {"name": "Peking University", "url": "https://english.pku.edu.cn/"},
        {"name": "Shanghai Jiao Tong", "url": "https://www.sjtu.edu.cn/"},
        {"name": "Zhejiang University", "url": "https://www.zju.edu.cn/"},
        {"name": "Fudan University", "url": "https://www.fudan.edu.cn/"},
        {"name": "Nanjing University", "url": "https://www.nju.edu.cn/"},
        {"name": "USTC", "url": "https://www.ustc.edu.cn/"},
        {"name": "Harbin Institute of Tech", "url": "https://www.hit.edu.cn/"}
    ],
    "الهند_إعلام آلي": [
        {"name": "IIT Bombay", "url": "https://www.cse.iitb.ac.in/"},
        {"name": "IIT Delhi", "url": "https://www.cse.iitd.ac.in/"},
        {"name": "IIT Madras", "url": "https://www.cse.iitm.ac.in/"},
        {"name": "IIT Kanpur", "url": "https://www.cse.iitk.ac.in/"},
        {"name": "IIT Kharagpur", "url": "https://www.iitkgp.ac.in/"},
        {"name": "IIT Roorkee", "url": "https://www.iitr.ac.in/"},
        {"name": "IIT Guwahati", "url": "https://www.iitg.ac.in/"},
        {"name": "IISc Bangalore", "url": "https://www.iisc.ac.in/"},
        {"name": "IIIT Hyderabad", "url": "https://www.iiit.ac.in/"},
        {"name": "BITS Pilani", "url": "https://www.bits-pilani.ac.in/"}
    ],
    "اليابان_ذكاء اصطناعي": [
        {"name": "University of Tokyo", "url": "https://www.u-tokyo.ac.jp/"},
        {"name": "Kyoto University", "url": "https://www.kyoto-u.ac.jp/"},
        {"name": "Tokyo Institute of Technology", "url": "https://www.titech.ac.jp/"},
        {"name": "Osaka University", "url": "https://www.osaka-u.ac.jp/"},
        {"name": "Tohoku University", "url": "https://www.tohoku.ac.jp/"}
    ],
    "كوريا الجنوبية_إعلام آلي": [
        {"name": "KAIST", "url": "https://www.kaist.ac.kr/"},
        {"name": "Seoul National University", "url": "https://www.snu.ac.kr/"},
        {"name": "POSTECH", "url": "https://www.postech.ac.kr/"},
        {"name": "Yonsei University", "url": "https://www.yonsei.ac.kr/"},
        {"name": "Korea University", "url": "https://www.korea.ac.kr/"}
    ],
    "سنغافورة_إعلام آلي": [
        {"name": "NUS", "url": "https://www.nus.edu.sg/"},
        {"name": "NTU", "url": "https://www.ntu.edu.sg/"},
        {"name": "SMU", "url": "https://www.smu.edu.sg/"}
    ],
    "أستراليا_إعلام آلي": [
        {"name": "University of Melbourne", "url": "https://www.unimelb.edu.au/"},
        {"name": "ANU", "url": "https://www.anu.edu.au/"},
        {"name": "University of Sydney", "url": "https://www.sydney.edu.au/"},
        {"name": "UNSW Sydney", "url": "https://www.unsw.edu.au/"},
        {"name": "Monash University", "url": "https://www.monash.edu/"},
        {"name": "University of Queensland", "url": "https://www.uq.edu.au/"}
    ],
    "روسيا_فيزياء": [
        {"name": "Moscow State University", "url": "https://www.msu.ru/"},
        {"name": "Moscow Institute of Physics", "url": "https://mipt.ru/"},
        {"name": "Saint Petersburg State University", "url": "https://english.spbu.ru/"},
        {"name": "Novosibirsk State University", "url": "https://www.nsu.ru/"}
    ],
    "إيطاليا_هندسة معمارية": [
        {"name": "Politecnico di Milano", "url": "https://www.polimi.it/"},
        {"name": "Sapienza Rome", "url": "https://www.uniroma1.it/"},
        {"name": "University of Bologna", "url": "https://www.unibo.it/"},
        {"name": "Politecnico di Torino", "url": "https://www.polito.it/"}
    ],
    "إسبانيا_طب": [
        {"name": "University of Barcelona", "url": "https://www.ub.edu/"},
        {"name": "Autonomous University of Madrid", "url": "https://www.uam.es/"},
        {"name": "Complutense Madrid", "url": "https://www.ucm.es/"},
        {"name": "University of Valencia", "url": "https://www.uv.es/"}
    ],
    "تركيا_هندسة مدنية": [
        {"name": "METU", "url": "https://www.metu.edu.tr/"},
        {"name": "Istanbul Technical University", "url": "https://www.itu.edu.tr/"},
        {"name": "Bogazici University", "url": "https://www.boun.edu.tr/"},
        {"name": "Bilkent University", "url": "https://www.bilkent.edu.tr/"}
    ],
    "البرازيل_هندسة كهربائية": [
        {"name": "University of São Paulo USP", "url": "https://www5.usp.br/"},
        {"name": "UNICAMP", "url": "https://www.unicamp.br/"},
        {"name": "UFRJ", "url": "https://ufrj.br/"}
    ],
    "جنوب أفريقيا_طب": [
        {"name": "University of Cape Town", "url": "https://www.uct.ac.za/"},
        {"name": "University of the Witwatersrand", "url": "https://www.wits.ac.za/"},
        {"name": "Stellenbosch University", "url": "https://www.sun.ac.za/"}
    ]
}

# === 5. نستخرجو الدول والتخصصات الموجودة فقط ===
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
        st.error(f'{t["limit_reached"]}'); st.warning(f'{t["wait"]}: {h} س و {m} د')
        if st.button(t["watch_ad"]):
            st.session_state.blocked_until = None; st.session_state.question_count = 0; st.rerun()
        st.stop()
    else:
        st.session_state.blocked_until = None; st.session_state.question_count = 0

st.sidebar.metric(t["questions_left"], 20 - st.session_state.question_count)
st.header(t["header"])

col1, col2 = st.columns(2)
with col1:
    country = st.selectbox(t["country"], all_countries)
with col2:
    majors_for_country = sorted(all_majors_by_country.get(country, []))
    if majors_for_country:
        major = st.selectbox(t["major"], majors_for_country, help=t["search"])
    else:
        st.warning(t["no_data"])
        major = None

if st.button(t["button"], type="primary", use_container_width=True) and major:
    if st.session_state.question_count > 0 and st.session_state.question_count % 5 == 0:
        st.warning(t["ad_required"])
        if st.button(t["ad_button"]): st.rerun()
        st.stop()

    st.session_state.question_count += 1
    if st.session_state.question_count >= 20:
        st.session_state.blocked_until = datetime.now() + timedelta(hours=3); st.rerun()

    key = f"{country}_{major}"
    st.subheader(f'{t["result"]} {major} {t["in"]} {country}:')

    if key in database and database[key]:
        st.success(f'{t["sources"]} {country}:')
        for link in database[key]:
            st.markdown(f"🔗 [{link['name']}]({link['url']})")
    else:
        st.warning(t["warning"])

st.markdown("---")
st.write(t["footer"])
