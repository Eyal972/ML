import streamlit as st

# הגדרת תצורת הדף
st.set_page_config(
    page_title="ניתוח נתוני מכירות משחקי וידאו",
    layout="wide",
    initial_sidebar_state="expanded",
)

# הוספת CSS לתמיכה מלאה בעברית (RTL) ויישור טקסטים
st.markdown(
    """
    <style>
    /* הגדרת כיוון הטקסט מימין לשמאל לכל הדף */
    html, body, [class*="css"], div, p, span, h1, h2, h3, h4, h5, h6 {
        direction: rtl;
        text-align: right;
    }
    
    /* יישור טבלאות וכותרות טבלה מימין לשמאל */
    .stDataFrame, .stTable, table {
        direction: rtl;
        text-align: right;
        width: 100%;
    }
    
    /* תיקון תצוגת אלמנטים של כרטיסיות (Metrics) */
    [data-testid="stMetricValue"] {
        direction: ltr;
        text-align: right;
    }
    
    /* יישור תיבות נפתחות (Expander) */
    .streamlit-expanderHeader {
        direction: rtl;
        text-align: right;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# כותרת ראשית
st.title("🎮 ניתוח נתוני מכירות ודירוגים של משחקי וידאו")
st.write(
    "אפליקציה זו מציגה תבנית לניתוח חוקר (EDA) של דאטה-סט מכירות משחקי וידאו, כולל הגדרת משתני למידת מכונה (הנתונים המוצגים הם להמחשה בלבד)."
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
    # שימוש בטבלת Markdown סטטית במקום Pandas DataFrame
    st.markdown("""
    | Name | Platform | Year_of_Release | Genre | Publisher | Global_Sales | Critic_Score |
    |---|---|---|---|---|---|---|
    | Wii Sports | Wii | 2006 | Sports | Nintendo | 82.53 | 76 |
    | Super Mario Bros. | NES | 1985 | Platform | Nintendo | 40.24 | - |
    | Mario Kart Wii | Wii | 2008 | Racing | Nintendo | 35.52 | 82 |
    | Wii Sports Resort | Wii | 2009 | Sports | Nintendo | 32.77 | 80 |
    | Pokemon Red/Blue | GB | 1996 | Role-Playing | Nintendo | 31.37 | - |
    """)

st.markdown("---")

# חלק 2: מידע על הנתונים
st.header("2. מידע סטטיסטי על הנתונים")

# מספר שורות ועמודות (נתונים פיקטיביים/המחשה)
col1, col2 = st.columns(2)
col1.metric("מספר שורות ממוצע בדאטה", "16,719")
col2.metric("מספר עמודות", "16")

st.subheader("ערכים חסרים ועקומים סטטיסטיים (ממוצעים)")

# טבלת סיכום סטטית במקום חישובים דינמיים
st.markdown("""
| שם עמודה | סוג נתונים | ערכים חסרים | אחוז ערכים חסרים | ממוצע (מספרי) |
|---|---|---|---|---|
| **Global_Sales** | `float64` | 0 | 0% | 0.53 |
| **Year_of_Release** | `float64` | 269 | 1.6% | 2006.5 |
| **Critic_Score** | `float64` | 8,582 | 51.3% | 68.9 |
| **User_Score** | `float64` | 9,129 | 54.5% | 7.1 |
""")

st.info("""
**תובנה לגבי ערכים חסרים וממוצעים:**
- **ערכים חסרים:** קיימים ערכים חסרים רבים בעמודות הדירוגים (`Critic_Score`, `User_Score`, `Rating` וכו'). הדבר נובע מכך שמשחקים ישנים רבים או משחקים יפניים לא עברו תהליך דירוג רשמי במערב.
- **שנת יציאה ממוצעת:** 2006.5. בתקופה זו חלה קפיצה משמעותית בפופולריות המשחקים.
""")

st.markdown("---")

# חלק 3: הגדרת y ו-X כולל נימוקים
st.header("3. הגדרת משתנה המטרה (y) והתכונות (X)")

st.subheader("🎯 משתנה המטרה: `Global_Sales` (y)")
st.write("""
- **הסבר:** סך המכירות העולמיות של המשחק (במיליוני יחידות).
- **נימוק:** יצירת מודל לחיזוי מכירות עולמיות מאפשרת לחברות פיתוח והפצה להעריך את הפוטנציאל הכלכלי של משחק עוד בשלבי התכנון.
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
