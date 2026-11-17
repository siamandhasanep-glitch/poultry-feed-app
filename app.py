import pandas as pd
import streamlit as st

st.set_page_config(page_title="LASTFEED - سیستمی دروستکردنی خۆراکی پەلەوەری", page_icon="🌾", layout="wide")

# Factory Header / Logo Sign
st.markdown(
    """
    <div style="text-align: center; padding: 10px; background-color: #1e3d2f; border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: #ffffff; margin: 0; font-family: sans-serif; letter-spacing: 2px;">🌾 LASTFEED 🌾</h1>
        <p style="color: #a3e4d7; margin: 5px 0 0 0; font-size: 16px;">کارگەی دروستکردنی خۆراکی پەلەوەر | لاست فید</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("سیستمی پیشەسازی دروستکردنی خۆراکی پەلەوەر و حیسابکردنی پێکهاتەکان")
st.write("پانێڵی ڕاستەقینەی کڕیارانی B2B: داڕشتنی کێشی داینامیکی و هاوسەنگی خۆراکی ڕاستەقینە.")

# 1. Initialize Complete Poultry Recipe & Nutrient Matrix (Includes 40% Sunflower Meal)
if "recipe_df" not in st.session_state:
    st.session_state.recipe_df = pd.DataFrame({
        "Ingredient": [
            "طحين - Flour", 
            "ذرة صفراء - Corn", 
            "صويا 45% - Soya", 
            "صويا 46% - Soya", 
            "قمح - Wheat", 
            "ردة القمح - Wheat Bran", 
            "مسحوق سمك - Fish meal", 
            "مسحوق لحم 55% - Meat meal", 
            "مركز بروتيني - Premix 0.25%", 
            "جلوتين ذرة - Gluten corn", 
            "ميثيونين - Methionine", 
            "ليسين - Lysine", 
            "كربونات كالسيوم - Calcium carbonate", 
            "مونوكالسيوم - Monocalcium phosphate", 
            "زيت - Oil", 
            "ملح - Salt", 
            "حجر جيري - Limestone",
            "كسب عباد الشمس 40% - Sunflower Meal (40%)"
        ],
        "Inclusion (kg or parts)": [5.0, 42.0, 15.0, 10.0, 5.0, 8.0, 2.0, 2.0, 0.25, 2.0, 0.1, 0.15, 1.0, 1.0, 3.0, 0.35, 1.55, 3.0],
        "Cost/Ton ($)": [320, 280, 510, 530, 290, 210, 1200, 900, 2500, 750, 4500, 4000, 150, 950, 900, 150, 80, 280],
        "Protein %": [11.0, 8.5, 45.0, 46.0, 13.0, 15.5, 65.0, 55.0, 0.0, 60.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 40.0],
        "Fat %": [1.5, 3.8, 1.2, 1.5, 2.0, 4.0, 8.0, 12.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 99.0, 0.0, 0.0, 1.5],
        "Energy (kcal/kg)": [3400, 3350, 2400, 2450, 3200, 2050, 2900, 2800, 0, 3900, 0, 0, 0, 0, 8800, 0, 0, 2150],
        "Calcium %": [0.03, 0.02, 0.25, 0.30, 0.05, 0.12, 5.0, 4.5, 0.0, 0.03, 0.0, 0.0, 40.0, 24.0, 0.0, 0.0, 38.0, 0.35],
        "Avail. P %": [0.10, 0.08, 0.18, 0.20, 0.12, 0.35, 2.5, 2.2, 0.0, 0.10, 0.0, 0.0, 0.0, 18.0, 0.0, 0.0, 0.0, 0.30]
    })

# Sidebar Navigation (Translated to Kurdish)
menu = st.sidebar.selectbox("پێڕستی سەرەکی (Navigation)", ["خشتەی ڕەچەتە و خۆراک (Workbench)", "ڕێنماییە خۆراکییەکان (Guidelines)"])

if menu == "ڕێنماییە خۆراکییەکان (Guidelines)":
    st.subheader("📊 ڕێنمایی و پێوانە ستانداردەکانی خۆراکی پەلەوەر")
    st.markdown("""
    * **قۆناغی سەرەتایی (Starter):** پروتینی خاو ~22٪، وزە ~3000 کیلۆکالۆری/کیلۆگرام
    * **قۆناغی گەشە (Grower):** پروتینی خاو ~20٪، وزە ~3100 کیلۆکالۆری/کیلۆگرام
    * **قۆناغی کۆتایی (Finisher):** پروتینی خاو ~18٪، وزە ~3200 کیلۆکالۆری/کیلۆگرام
    """)

elif menu == "خشتەی ڕەچەتە و خۆراک (Workbench)":
    st.subheader("🧪 کارگەی دروستکردنی ڕەچەتەی تایبەت")
    st.write("کێش یان بەشەکان بنووسە. سیستەمەکە خۆکارانە ڕێژەکان هاوسەنگ دەکات بۆ نیشاندانی ڕێژەی ڕاستی پروتین و پێکهاتەکان.")

    # 2. Interactive Data Editor with Dynamic Rows Enabled
    edited_recipe = st.data_editor(
        st.session_state.recipe_df,
        use_container_width=True,
        key="custom_recipe_editor",
        height=600,
        num_rows="dynamic"  # Allows adding/removing custom ingredients on the fly
    )
    
    st.session_state.recipe_df = edited_recipe

    # 3. Live Calculations with Automatic Normalization
    try:
        total_weight = edited_recipe["Inclusion (kg or parts)"].sum()
        if total_weight <= 0:
            total_weight = 1.0  # Prevent division by zero

        # AUTOMATIC NORMALIZATION
        fraction = edited_recipe["Inclusion (kg or parts)"] / total_weight

        # Calculate Total Cost per Ton
        partial_costs = fraction * edited_recipe["Cost/Ton ($)"]
        total_batch_cost = partial_costs.sum()

        # Calculate True Nutritional Ratios
        total_protein = (fraction * edited_recipe["Protein %"]).sum()
        total_fat = (fraction * edited_recipe["Fat %"]).sum()
        total_energy = (fraction * edited_recipe["Energy (kcal/kg)"]).sum()
        total_calcium = (fraction * edited_recipe["Calcium %"]).sum()
        total_phosphorus = (fraction * edited_recipe["Avail. P %"]).sum()

        # Display Top Metrics Banner
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("کۆی گشتی کێش (Total Sum)", f"{total_weight:,.2f}")
        with col2:
            st.metric("تێچووی گشتی بۆ یەک تۆن", f"${total_batch_cost:,.2f}")
        with col3:
            st.metric("بارودۆخی ڕەچەتە", "✅ هاوسەنگ و کارا")

        st.markdown("---")
        st.subheader("📈 ئەنجامی بەرهەمی خۆراکی و ڕێژەکان")
        
        # Nutrient Summary Cards
        n_col1, n_col2, n_col3, n_col4, n_col5 = st.columns(5)
        with n_col1:
            st.metric("پروتینی خاو (Protein)", f"{total_protein:.2f}%")
        with n_col2:
            st.metric("چەوری خاو (Fat)", f"{total_fat:.2f}%")
        with n_col3:
            st.metric("وزە (Energy)", f"{total_energy:.0f} kcal/kg")
        with n_col4:
            st.metric("کالیسیۆم (Calcium)", f"{total_calcium:.2f}%")
        with n_col5:
            st.metric("فۆسفۆری بەردەست", f"{total_phosphorus:.2f}%")

    except Exception as e:
        st.error(f"هەڵە لە حیسابکردندا: دڵنیابە لەوەی سەرجەم خانەکان ژمارەن.")

    st.markdown("---")
    if st.button("پەسەندکردن و قفڵکردنی ڕەچەتە بۆ بەرهەمهێنان"):
        st.success("🎉 ڕەچەتەکە بە سەرکەوتوویی پەسەندکرا و ئامادەیە!")
