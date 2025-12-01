import streamlit as st
import requests
from datetime import datetime, timedelta
import json

# إعدادات الصفحة
st.set_page_config(
    page_title="Climate Alerts - إنذار مبكر مناخي",
    page_icon="🌍",
    layout="wide"
)

# CSS مخصص
st.markdown("""
<style>
    .alert-critical {
        background-color: #ff4444;
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .alert-warning {
        background-color: #ffaa00;
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .alert-info {
        background-color: #0088ff;
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .alert-safe {
        background-color: #00cc66;
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .safety-tip {
        background-color: #f0f0f0;
        padding: 15px;
        border-right: 5px solid #0088ff;
        border-radius: 5px;
        margin: 5px 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# العنوان
st.title("🌍 Climate Alerts - نظام الإنذار المناخي المبكر")
st.markdown("### راقب الأحوال الجوية واحصل على تنبيهات فورية")

# الشريط الجانبي للإعدادات
st.sidebar.header("⚙️ الإعدادات")
city = st.sidebar.text_input("🌆 أدخل اسم المدينة", "Muscat")
api_key = st.sidebar.text_input("🔑 مفتاح API من OpenWeatherMap", type="password", 
                                help="احصل على مفتاح مجاني من openweathermap.org")

# عتبات التنبيهات
st.sidebar.subheader("📊 عتبات التنبيهات")
temp_threshold = st.sidebar.slider("درجة حرارة موجة الحر (°C)", 35, 50, 42)
wind_threshold = st.sidebar.slider("سرعة الرياح للعواصف (كم/س)", 30, 100, 60)
aqi_threshold = st.sidebar.slider("عتبة جودة الهواء", 50, 200, 100)

# دالة للحصول على بيانات الطقس
def get_weather_data(city, api_key):
    try:
        # بيانات الطقس الحالية
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ar"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"خطأ في الاتصال: {str(e)}")
        return None

# دالة للحصول على بيانات جودة الهواء
def get_air_quality(lat, lon, api_key):
    try:
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

# دالة لتحديد مستوى التنبيه
def analyze_weather_alerts(weather_data, aqi_data, temp_threshold, wind_threshold, aqi_threshold):
    alerts = []
    
    if not weather_data:
        return alerts
    
    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    wind_speed = weather_data['wind']['speed'] * 3.6  # تحويل من م/ث إلى كم/س
    humidity = weather_data['main']['humidity']
    rain = weather_data.get('rain', {}).get('1h', 0)
    
    # فحص موجة الحر
    if temp >= temp_threshold or feels_like >= temp_threshold:
        alerts.append({
            'type': 'critical',
            'icon': '🔥',
            'title': 'تحذير: موجة حر شديدة',
            'message': f'درجة الحرارة {temp}°C والإحساس بـ {feels_like}°C',
            'safety': [
                '🚰 اشرب كميات كبيرة من الماء',
                '🏠 ابقَ في الداخل في الأوقات الحارة',
                '👕 ارتدِ ملابس خفيفة وفاتحة اللون',
                '🚫 تجنب الأنشطة الخارجية الشاقة',
                '❄️ استخدم المكيفات أو المراوح'
            ]
        })
    
    # فحص العواصف
    if wind_speed >= wind_threshold:
        alerts.append({
            'type': 'critical',
            'icon': '🌪️',
            'title': 'تحذير: عاصفة قوية',
            'message': f'سرعة الرياح {wind_speed:.1f} كم/س',
            'safety': [
                '🏠 ابقَ في الداخل بعيداً عن النوافذ',
                '🚗 تجنب القيادة إلا للضرورة',
                '🌳 ابتعد عن الأشجار والأعمدة',
                '📱 احتفظ بهاتفك مشحوناً',
                '🔦 جهّز مصباحاً يدوياً وبطاريات'
            ]
        })
    
    # فحص احتمالية الفيضانات
    if rain > 10:
        alerts.append({
            'type': 'warning',
            'icon': '🌊',
            'title': 'تحذير: أمطار غزيرة - احتمال فيضانات',
            'message': f'كمية الأمطار المتوقعة: {rain} مم/ساعة',
            'safety': [
                '🚫 تجنب المناطق المنخفضة',
                '🚗 لا تقد عبر المياه الجارية',
                '📍 اعرف طرق الإخلاء في منطقتك',
                '📦 احتفظ بمستلزمات الطوارئ',
                '📻 تابع نشرات الأخبار المحلية'
            ]
        })
    
    # فحص جودة الهواء
    if aqi_data and 'list' in aqi_data:
        aqi = aqi_data['list'][0]['main']['aqi']
        if aqi >= 4:  # جودة هواء سيئة
            alerts.append({
                'type': 'warning',
                'icon': '😷',
                'title': 'تحذير: جودة هواء سيئة',
                'message': f'مستوى جودة الهواء: {aqi} من 5',
                'safety': [
                    '😷 ارتدِ كمامة عند الخروج',
                    '🏠 أبقِ النوافذ مغلقة',
                    '🏃 تجنب التمارين الخارجية',
                    '💊 استخدم أجهزة تنقية الهواء',
                    '🩺 راجع الطبيب إذا كنت تعاني من مشاكل تنفسية'
                ]
            })
    
    # إذا لم يكن هناك تنبيهات
    if len(alerts) == 0:
        alerts.append({
            'type': 'safe',
            'icon': '✅',
            'title': 'الأحوال الجوية آمنة',
            'message': 'لا توجد تحذيرات مناخية حالياً',
            'safety': [
                '🌤️ استمتع بيومك بأمان',
                '🧴 استخدم واقي الشمس عند الخروج',
                '💧 حافظ على ترطيب جسمك',
                '👀 راقب تحديثات الطقس بانتظام'
            ]
        })
    
    return alerts

# الزر لجلب البيانات
if st.sidebar.button("🔄 تحديث البيانات", type="primary"):
    if not api_key:
        st.warning("⚠️ الرجاء إدخال مفتاح API من OpenWeatherMap")
    else:
        with st.spinner("جاري جلب البيانات..."):
            weather_data = get_weather_data(city, api_key)
            
            if weather_data:
                # جلب بيانات جودة الهواء
                lat = weather_data['coord']['lat']
                lon = weather_data['coord']['lon']
                aqi_data = get_air_quality(lat, lon, api_key)
                
                # تحليل التنبيهات
                alerts = analyze_weather_alerts(weather_data, aqi_data, temp_threshold, wind_threshold, aqi_threshold)
                
                # عرض المقاييس الرئيسية
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>🌡️ درجة الحرارة</h3>
                        <h1>{weather_data['main']['temp']:.1f}°C</h1>
                        <p>الإحساس: {weather_data['main']['feels_like']:.1f}°C</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>💨 الرياح</h3>
                        <h1>{weather_data['wind']['speed']*3.6:.1f}</h1>
                        <p>كم/ساعة</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>💧 الرطوبة</h3>
                        <h1>{weather_data['main']['humidity']}%</h1>
                        <p>نسبة الرطوبة</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    if aqi_data and 'list' in aqi_data:
                        aqi = aqi_data['list'][0]['main']['aqi']
                        aqi_labels = {1: 'ممتاز', 2: 'جيد', 3: 'متوسط', 4: 'سيء', 5: 'سيء جداً'}
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>😷 جودة الهواء</h3>
                            <h1>{aqi}/5</h1>
                            <p>{aqi_labels.get(aqi, 'غير متوفر')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="metric-card">
                            <h3>😷 جودة الهواء</h3>
                            <h1>-</h1>
                            <p>غير متوفر</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # عرض التنبيهات
                st.header("🚨 التنبيهات والإنذارات")
                
                for alert in alerts:
                    alert_class = f"alert-{alert['type']}"
                    st.markdown(f"""
                    <div class="{alert_class}">
                        <h2>{alert['icon']} {alert['title']}</h2>
                        <p style="font-size: 18px;">{alert['message']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.subheader("📋 إرشادات السلامة:")
                    for tip in alert['safety']:
                        st.markdown(f"""
                        <div class="safety-tip">
                            {tip}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                
                # معلومات إضافية
                with st.expander("ℹ️ معلومات تفصيلية عن الطقس"):
                    st.json(weather_data)
                
            else:
                st.error("❌ فشل في جلب بيانات الطقس. تأكد من اسم المدينة ومفتاح API.")

# معلومات في الشريط الجانبي
st.sidebar.markdown("---")
st.sidebar.info("""
### 💡 كيفية الاستخدام:
1. احصل على مفتاح API مجاني من [OpenWeatherMap](https://openweathermap.org/api)
2. أدخل اسم المدينة ومفتاح API
3. اضغط على "تحديث البيانات"
4. راجع التنبيهات وإرشادات السلامة

### 🔔 أنواع التنبيهات:
- 🔥 موجة حر
- 🌪️ عواصف
- 🌊 فيضانات محتملة
- 😷 جودة هواء سيئة
""")

st.sidebar.success("✅ التطبيق جاهز للاستخدام")

# تذييل
st.markdown("---")
st.caption("🌍 Climate Alerts - نظام الإنذار المناخي المبكر | Powered by OpenWeatherMap API")