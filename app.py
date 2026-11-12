import pandas as pd
import streamlit as st

st.set_page_config(page_title="Poultry Feed Formulation System", page_icon="🌾", layout="wide")

st.title("🌾 Industrial Poultry Feed Formulation & Nutrient Calculator")
st.write("Live B2B Client Workbench: Custom Ingredient Formulation & Real-Time Nutritional Balancing.")

# 1. Initialize Complete Poultry Recipe & Nutrient Matrix with your custom ingredients (Total = 100%)
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
            "حجر جيري - Limestone"
        ],
        "Inclusion %": [5.0, 45.0, 15.0, 10.0, 5.0, 8.0, 2.0, 2.0, 0.25, 2.0, 0.1, 0.15, 1.0, 1.0, 3.0, 0.35, 1.55],
        "Cost/Ton ($)": [320, 280, 510, 530, 290, 210, 1200, 900, 2500, 750, 4500, 4000, 150, 950, 900, 150, 80],
        "Protein %": [11.0, 8.5, 45.0, 46.0, 13.0, 15.5, 65.0, 55.0, 0.0, 60.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Fat %": [1.5, 3.8, 1.2, 1.5, 2.0, 4.0, 8.0, 12.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 99.0, 0.0, 0.0],
        "Energy (kcal/kg)": [3400, 3350, 2400, 2450, 3200, 2050, 2900, 2800, 0, 3900, 0, 0, 0, 0, 8800, 0, 0],
        "Calcium %": [0.03, 0.02, 0.25, 0.30, 0.05, 0.12, 5.0, 4.5, 0.0, 0.03, 0.0, 0.0, 40.0, 24.0, 0.0, 0.0, 38.0],
        "Avail. P %": [0.10, 0.08, 0.18, 0.20, 0.12, 0.35, 2.5, 2.2, 0.0, 0.10, 0.0, 0.0, 0.0, 18.0, 0.0, 0.0, 0.0]
    })

# Sidebar Navigation
menu = st.sidebar.selectbox("Navigation Menu", ["Recipe & Nutrient Workbench", "Nutritional Guidelines"])

if menu == "Nutritional Guidelines":
    st.subheader("📊 Poultry Nutritional Standards Reference")
    st.markdown("""
    * **Starter Phase:** Crude Protein ~22%, Energy ~3000 kcal/kg
    * **Grower Phase:** Crude Protein ~20%, Energy ~3100 kcal/kg
    * **Finisher Phase:** Crude Protein ~18%, Energy ~3200 kcal/kg
    * *Note: Total inclusion across all ingredients must sum exactly to **100%**.*
    """)

elif menu == "Recipe & Nutrient Workbench":
    st.subheader("🧪 Custom Ingredient Formulation Workbench")
    st.write("Modify the **Inclusion %** for your ingredients below. The totals, costs, and nutritional yields will update instantly.")

    # 2. Interactive Data Editor
    edited_recipe = st.data_editor(
        st.session_state.recipe_df,
        use_container_width=True,
        key="custom_recipe_editor",
        height=600
    )
    
    st.session_state.recipe_df = edited_recipe

    # 3. Live Calculations
    try:
        total_inclusion = edited_recipe["Inclusion %"].sum()
        
        # Calculate Costs & Nutrient Yields
        partial_costs = (edited_recipe["Inclusion %"] / 100.0) * edited_recipe["Cost/Ton ($)"]
        total_batch_cost = partial_costs.sum()

        total_protein = ((edited_recipe["Inclusion %"] / 100.0) * edited_recipe["Protein %"]).sum()
        total_fat = ((edited_recipe["Inclusion %"] / 100.0) * edited_recipe["Fat %"]).sum()
        total_energy = ((edited_recipe["Inclusion %"] / 100.0) * edited_recipe["Energy (kcal/kg)"]).sum()
        total_calcium = ((edited_recipe["Inclusion %"] / 100.0) * edited_recipe["Calcium %"]).sum()
        total_phosphorus = ((edited_recipe["Inclusion %"] / 100.0) * edited_recipe["Avail. P %"]).sum()

        # Display Top Metrics Banner
        col1, col2, col3 = st.columns(3)
        with col1:
            diff = total_inclusion - 100.0
            st.metric("Total Batch Inclusion", f"{total_inclusion:.2f}%", delta=f"{diff:+.2f}%" if abs(diff) > 0.01 else "Perfect (100%)")
        with col2:
            st.metric("Total Cost per Ton", f"${total_batch_cost:,.2f}")
        with col3:
            status = "✅ Balanced" if abs(total_inclusion - 100.0) <= 0.01 else "⚠️ Must equal 100%"
            st.metric("Formulation Status", status)

        st.markdown("---")
        st.subheader("📈 Delivered Nutritional Yield Profile")
        
        # Nutrient Summary Cards
        n_col1, n_col2, n_col3, n_col4, n_col5 = st.columns(5)
        with n_col1:
            st.metric("Crude Protein", f"{total_protein:.2f}%")
        with n_col2:
            st.metric("Crude Fat", f"{total_fat:.2f}%")
        with n_col3:
            st.metric("Energy", f"{total_energy:.0f} kcal/kg")
        with n_col4:
            st.metric("Calcium", f"{total_calcium:.2f}%")
        with n_col5:
            st.metric("Avail. Phosphorus", f"{total_phosphorus:.2f}%")

    except Exception as e:
        st.error(f"Calculation error: Ensure all table inputs are numeric values.")

    st.markdown("---")
    if st.button("Validate & Lock Batch Formulation"):
        if abs(edited_recipe["Inclusion %"].sum() - 100.0) <= 0.01:
            st.success("🎉 Batch successfully validated and locked for production!")
        else:
            st.error("❌ Batch cannot be locked: Total inclusion percentage must equal exactly 100%. Adjust your percentages.")