import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والهوية البصرية للعيادة
st.set_page_config(page_title="العيادة الرياضياتية العلاجية", page_icon="🩺", layout="centered")

# تنسيق CSS مخصص للواجهة الكحيلية/النعناعية
st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    .stButton>button { 
        background-color: #10B981; 
        color: white; 
        border-radius: 10px; 
        font-weight: bold; 
        width: 100%; 
        height: 50px; 
        font-size: 18px;
        border: none;
    }
    .psych-card { 
        background-color: #ECFDF5; 
        border-right: 5px solid #10B981; 
        padding: 15px; 
        border-radius: 8px; 
        margin-bottom: 20px;
        color: #064E3B;
    }
    .question-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🩺 العيادة الرياضياتية العلاجية")
st.caption("منصة قائمة على الذكاء الاصطناعي لعلاج الأخطاء الشائعة وخفض قلق الرياضيات للمرحلة الإعدادية")

# رسالة الدعم النفسي لتقليل القلق
st.markdown("""
<div class="psych-card">
    🌱 <b>رسالة العيادة:</b> الخطأ ليس حكماً عليك، بل هو أول خطوة عملية نحو الفهم العميق! خذ نفساً عميقاً وفكر بهدوء.
</div>
""", unsafe_allow_html=True)

# القائمة الجانبية لمفتاح API
with st.sidebar:
    st.header("⚙️ إعدادات العيادة")
    api_key = st.text_input("مفتاح Gemini API الخاص بك:", type="password")
    st.caption("يمكنك الحصول عليه مجاناً 100% من Google AI Studio.")

# عرض المسألة ببطاقة منسقة
st.markdown("""
<div class="question-card">
    <h3 style="color: #1E293B;">📌 المسألة الحالية:</h3>
    <h1 style="color: #0F172A;">(x + 3)²</h1>
    <p style="color: #64748B;">المطلوب: فك المقدار الجبري وتطويره إلى أبسط صورة.</p>
</div>
""", unsafe_allow_html=True)

# متابعة عداد المحاولات
if 'attempt' not in st.session_state:
    st.session_state.attempt = 1

student_answer = st.text_input("اكتب إجابتك هنا:", placeholder="مثال: x² + 6x + 9")

if st.button("🩺 افحص إجابتي في العيادة"):
    if not api_key:
        st.error("يرجى إدخال مفتاح Gemini API في القائمة الجانبية أولاً.")
    elif not student_answer:
        st.warning("يرجى كتابة إجابتك قبل الفحص.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            أنت معلم رياضيات داعم ومخصص للمرحلة الإعدادية.
            المسألة: (x + 3)²
            إجابة الطالب: {student_answer}
            رقم المحاولة الحالية: {st.session_state.attempt}
            الخطأ الشائع المتوقع: نسيان الحد الأوسط (6x) وتوزيع الأس لتصبح الإجابة x² + 9.

            قم بصياغة التغذية الراجعة باللغة العربية وبتقسيم أنيق كالتالي:
            1. [🟢 الدعم النفسي]: عبارة مشجعة ومطمئنة لخفض قلق الرياضيات.
            2. [💡 التشخيص والتلميح]: 
               - إذا كانت المحاولة 1: قدم تلميحاً مفهومياً بسيطاً دون إعطاء الحل النهائي.
               - إذا كانت المحاولة 2 أو أكثر: لا تكرر التلميح، بل أنشئ نشاطاً فرعياً تبسيطياً (مثل سؤال الطالب أولاً عن حاصل ضرب 2 × x × 3).
            3. [🎯 خطوة العمل التالية]: سؤال تفاعلي محدد يدفع الطالب للمحاولة مجدداً.
            
            تنبيه هام: استخدم الأسس المرفوعة الرمزية (x², 9) والعلامات المنسقة، ولا تستخدم رموز البرمجة الخام مثل ^.
            """
            
            with st.spinner("جاري تحليل الإجابة بواسطة الذكاء الاصطناعي..."):
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.attempt += 1
                
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال: {e}")
      
