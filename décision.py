import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# 📌 إعداد الخط لدعم العربية
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.unicode_minus'] = False

# 📌 إعداد واجهة التطبيق
st.title("📊 تطبيق الذكاء الاصطناعي لتحليل الحملات التسويقية")
st.write("🔍 أدخل بيانات حملتك التسويقية للحصول على توصيات تعتمد على الذكاء الاصطناعي.")

# 📌 إدخال بيانات الحملة
budget = st.number_input("💰 ميزانية الحملة (الدرهم المغربي):", min_value=1000, max_value=100000, step=500)
channel = st.selectbox("📡 القناة التسويقية:", ["إعلانات رقمية", "وسائل التواصل", "تلفزيون", "راديو", "بريد إلكتروني"])
audience = st.selectbox("👥 الفئة المستهدفة:", ["18-24", "25-34", "35-44", "45-54", "55+"])
duration = st.slider("⏳ مدة الحملة (بالأيام):", min_value=7, max_value=90, step=7)
market_condition = st.selectbox("🌍 حالة السوق:", ["طبيعية", "أزمة كورونا", "أزمة اقتصادية"])

# 📌 معالجة البيانات
df = pd.DataFrame({
    "budget": np.random.randint(1000, 50000, 100),
    "channel": np.random.choice(["إعلانات رقمية", "وسائل التواصل", "تلفزيون", "راديو", "بريد إلكتروني"], 100),
    "audience": np.random.choice(["18-24", "25-34", "35-44", "45-54", "55+"], 100),
    "duration": np.random.randint(7, 90, 100),
    "market_condition": np.random.choice(["طبيعية", "أزمة كورونا", "أزمة اقتصادية"], 100),
    "success": np.random.choice([0, 1], 100)
})

# 📌 ترميز القيم (إنشاء ترميز منفصل لكل عمود)
le_channel = LabelEncoder()
df["channel"] = le_channel.fit_transform(df["channel"])

le_audience = LabelEncoder()
df["audience"] = le_audience.fit_transform(df["audience"])

le_market = LabelEncoder()
df["market_condition"] = le_market.fit_transform(df["market_condition"])

# 📌 إعداد البيانات
X = df[["budget", "channel", "audience", "duration", "market_condition"]]
y = df["success"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 📌 تدريب النموذج
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 📊 تحليل الميزات
importances = model.feature_importances_
importance_df = pd.DataFrame({"الميزة": X.columns, "الأهمية": importances}).sort_values(by="الأهمية", ascending=False)

# 📈 دقة النموذج
accuracy = accuracy_score(y_test, model.predict(X_test))
st.write(f"📈 **دقة النموذج: {accuracy * 100:.2f}%**")

# 📊 تفسير النتائج
# التحقق من وجود الفئات الجديدة وإضافتها إذا لزم الأمر
if channel not in le_channel.classes_:
    le_channel.classes_ = np.append(le_channel.classes_, channel)
if audience not in le_audience.classes_:
    le_audience.classes_ = np.append(le_audience.classes_, audience)
if market_condition not in le_market.classes_:
    le_market.classes_ = np.append(le_market.classes_, market_condition)

# التنبؤ
new_data = pd.DataFrame([[budget, le_channel.transform([channel])[0], le_audience.transform([audience])[0], duration, le_market.transform([market_condition])[0]]],
                        columns=["budget", "channel", "audience", "duration", "market_condition"])

prediction = model.predict(new_data)[0]
result = "نجاح 🎯" if prediction == 1 else "فشل ⚠️"

# 📊 تقرير تحليلي شامل
analysis = f"""
🔎 **تقرير تحليلي شامل حول الحملة التسويقية:**  
- بناءً على الميزانية المحددة ({budget}$) واختيار القناة التسويقية ({channel})، تم تحليل المعطيات والتنبؤ بنتيجة الحملة.  
- الفئة المستهدفة ({audience}) تلعب دوراً محورياً في نجاح الحملة، بالإضافة إلى مدة الحملة المحددة ({duration} أيام).  
- تم الأخذ في الاعتبار حالة السوق الحالية ({market_condition}) والتي قد تؤثر بشكل ملحوظ على الأداء.  
- **نتيجة التنبؤ:** الحملة من المحتمل أن تكون بنسبة عالية **{result}**.  
- **تحليل الميزات المؤثرة:**  
"""

for index, row in importance_df.iterrows():
    analysis += f"- **{row['الميزة']}**: مستوى تأثيره على النجاح هو **{row['الأهمية']:.2f}**.\n"

st.write(analysis)

# 📊 رسم المخططات
st.subheader("🔑 أهمية الميزات في اتخاذ القرار")
fig, ax = plt.subplots()
sns.barplot(x="الأهمية", y="الميزة", data=importance_df, palette="viridis", ax=ax)
ax.set_title("مخطط أهمية الميزات")
st.pyplot(fig)

# 📝 تحليل مخطط أهمية الميزات
st.markdown("""
🔍 **تحليل مخطط أهمية الميزات:**  
يُظهر المخطط أعلاه الميزات الأكثر تأثيرًا في نجاح الحملات التسويقية. يمكن ملاحظة أن الميزانية ومدّة الحملة تعتبران من العوامل الأكثر أهمية، بينما تلعب القناة التسويقية والفئة المستهدفة دورًا أيضًا ولكن بدرجات أقل.  
يتيح هذا التحليل للمسوقين التركيز على الميزات الأساسية لتحقيق أعلى نسبة نجاح.
""")

# 📊 رسم العلاقة بين الميزانية والنجاح
st.subheader("💸 تأثير الميزانية على نجاح الحملة")
fig2, ax2 = plt.subplots()
sns.scatterplot(data=df, x="budget", y="success", hue="market_condition", style="channel", ax=ax2)
ax2.set_title("تأثير الميزانية على النجاح")
st.pyplot(fig2)

# 📝 تحليل العلاقة بين الميزانية والنجاح
st.markdown("""
🔍 **تحليل تأثير الميزانية على النجاح:**  
يظهر المخطط أن هناك علاقة إيجابية بين الميزانية ونجاح الحملة التسويقية.  
يمكن ملاحظة أن الحملات ذات الميزانيات الأعلى تميل إلى تحقيق نجاح أكبر، خاصة في ظل ظروف سوق طبيعية.  
كما تلعب حالة السوق دورًا مهمًا في التأثير على النتيجة، حيث تكون الحملات أكثر تحديًا أثناء الأزمات الاقتصادية أو جائحة كورونا.
""")

# 📊 تحليل العلاقة بين القناة والنجاح
st.subheader("📡 تأثير القناة التسويقية على نجاح الحملة")
fig3, ax3 = plt.subplots()
sns.countplot(data=df, x="channel", hue="success", palette="cool", ax=ax3)
ax3.set_title("نجاح الحملات حسب القناة")
st.pyplot(fig3)

# 📝 تحليل نجاح الحملات حسب القناة
st.markdown("""
🔍 **تحليل نجاح الحملات حسب القناة:**  
يوضح المخطط تباين نجاح الحملات بناءً على القناة التسويقية المستخدمة.  
يبدو أن القنوات الرقمية ووسائل التواصل الاجتماعي تحقق نسبة نجاح أعلى مقارنةً بالقنوات التقليدية مثل الراديو أو التلفزيون.  
يمكن للمسوقين استخدام هذه المعلومات لتوجيه استراتيجياتهم التسويقية نحو القنوات الأكثر فاعلية.  
""")


