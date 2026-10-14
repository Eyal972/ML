import pandas as pd
import streamlit as st

# הגדרת תצורת הדף (תיקון הפרמטר ל-layout)
st.set_page_config(
    page_title="ניתוח נתוני מכירות משחקי וידאו",
    layout="wide",
    initial_sidebar_state="expanded",
)


# טעינת הנתונים (שימוש במנגנון מטמון של Streamlit לשיפור ביצועים)
@st.cache_data
def load_data():
    import kagglehub
    from kagglehub import KaggleDatasetAdapter

    # טעינת הנתונים מ-Kaggle
    df = kagglehub.dataset_load(
        KaggleDatasetAdapter.PANDAS,
        "rush4ratio/video-game-sales-with-ratings",
        "Video_Games_Sales_as_at_22_Dec_2016.csv",
    )
    return df


# טעינת הדאטה-סט
try:
    df = load_data()
except Exception as e:
    st.error(f"שגיאה בטעינת הנתונים: {e}")
    st.stop()

# כותרת ראשית
st.title("🎮 ניתוח נתוני מכירות ודירוגים של משחקי וידאו")
st.write(
    "אפליקציה זו מציגה ניתוח חוקר (EDA) של דאטה-סט מכירות משחקי וידאו מ-Kaggle, כולל הגדרת משתני למידת מכונה."
)

st.markdown("---")

# חלק 1: הסבר על הדאטה שנבחר
st.header("1. הסבר על הדאטה שנבחר")
st.write("""
**על מה הדאטה?** 
הדאטה-סט כולל מידע על מכירות משחקי וידאו ברחבי העולם, לצד דירוגי מבקרים ומשתמשים, פלטפורמות, ז'אנרים וחברות מפיצות/מפתחות.

**מה מייצגת כל שורה?**
כל שורה בדאטה-סט מייצגת **משחק וידאו יחיד** ויציאתו לפלטפורמה ספציפית (לדוגמה: המשחק Wii Sports עבור קונסולת Wii).
""")

with st.expander("🔍 הצג דוגמה מתוך הנתונים (5 שורות ראשונות)"):
    st.dataframe(df.head())

st.markdown("---")

# חלק 2: מידע על הנתונים
st.header("2. מידע סטטיסטי על הנתונים")

# מספר שורות ועמודות
col1, col2 = st.columns(2)
col1.metric("מספר שורות", f"{df.shape[0]:,}")
col2.metric("מספר עמודות", f"{df.shape[1]}")

st.subheader("ערכים חסרים ועקומים סטטיסטיים (ממוצעים)")

# עיבוד הנתונים לצורך חישוב ממוצעים וערכים חסרים
df_processed = df.copy()
df_processed["User_Score"] = pd.to_numeric(
    df_processed["User_Score"], errors="coerce"
)

# חישוב ערכים חסרים וממוצעים
missing_vals = df.isnull().sum()
numeric_cols = df_processed.select_dtypes(include="number").columns
means = df_processed[numeric_cols].mean()

# יצירת טבלה מרכזת
stats_summary = pd.DataFrame(
    {
        "סוג נתונים (Dtype)": df.dtypes.astype(str),
        "ערכים חסרים": missing_vals,
        "אחוז ערכים חסרים": (missing_vals / len(df) * 100).round(2).astype(str)
        + "%",
        "ממוצע (עבור עמודות מספריות)": means.round(2),
    }
)

st.dataframe(stats_summary, use_container_width=True)

st.info("""
**תובנה לגבי ערכים חסרים וממוצעים:**
* **ערכים חסרים:** קיימים ערכים חסרים רבים בעמודות הדירוגים (`Critic_Score`, `User_Score`, `Rating` וכו'). הדבר נובע מכך שמשחקים ישנים רבים או משחקים יפניים לא עברו תהליך דירוג רשמי במערב.
* **שנת יציאה ממוצעת:** 2006.5. בתקופה זו חלה קפיצה משמעותית בפופולריות המשחקים.
""")

st.markdown("---")

# חלק 3: הגדרת y ו-X כולל נימוקים
st.header("3. הגדרת משתנה המטרה (y) והתכונות (X)")

st.subheader("🎯 משתנה המטרה: `Global_Sales` (y)")
st.write("""
* **הסבר:** סך המכירות העולמיות של המשחק (במיליוני יחידות).
* **נימוק:** יצירת מודל לחיזוי מכירות עולמיות מאפשרת לחברות פיתוח והפצה להעריך את הפוטנציאל הכלכלי של משחק עוד בשלבי התכנון.
""")

st.subheader("💡 התכונות שנבחרו לחיזוי (X):")

col_x1, col_x2, col_x3 = st.columns(3)

with col_x1:
    st.markdown("### 1. Year_of_Release")
    st.write(
        "**נימוק:** שנת היציאה משפיעה על גודל השוק והביקוש באותה תקופה (כפי שראינו, תקופת השיא הייתה באזור שנת 2006)."
    )

with col_x2:
    st.markdown("### 2. Critic_Score")
    st.write(
        "**נימוק:** ציון המבקרים המקצועיים משקף את איכות המשחק. ככל שהציון גבוה יותר, כך גדל הסיכוי שהמשחק ימכור עותקים רבים יותר."
    )

with col_x3:
    st.markdown("### 3. Critic_Count")
    st.write(
        "**נימוק:** כמות המבקרים שסיקרו את המשחק מעידה על רמת ההד התקשורתי והפופולריות שלו בשוק."
    )
