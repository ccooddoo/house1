import streamlit as st
import pandas as pd
import joblib  # For loading the trained model
import plotly.express as px
import io  # To handle in-memory files for download

# Load the trained model (ensure the path is correct)
model = joblib.load("optimized_house_price_model_xgb.pkl")  # Updated to your optimized model

# Prices for materials and construction stages (adjust the multipliers for locations)
location_prices = {
    'Metro': 1.5,
    'Urban': 1.2,
    'Semi Urban': 1.0,
    'District': 0.9,
    'Taluka': 0.7,
    'Rural': 0.5
}

# BHK cost definitions
bhk_costs = {
    '1BHK': 10000,
    '2BHK': 15000,
    '3BHK': 20000,
    '4BHK': 25000
}

# Streamlit UI
st.set_page_config(page_title="House Price Prediction", layout="wide")
st.title("🏠 House Price Prediction")

# Sidebar for user inputs
st.sidebar.header("Input Options")

# User input for location and square footage (minimum 500 sq ft)
location = st.sidebar.selectbox("Select Location", list(location_prices.keys()))
sq_ft = st.sidebar.number_input("Enter Square Footage", min_value=100, value=1000)

# BHK selection with cost addition in pre-construction
bhk = st.sidebar.selectbox("Select BHK Type", list(bhk_costs.keys()))

# Pre-construction breakdown with BHK costs
pre_construction_items = {
    "Design Fees": 10000,
    "Borewell": 15000,
    bhk: bhk_costs[bhk]  # Add selected BHK cost to pre-construction
}

# Construction breakdown
construction_items = {
    "Marking/Excavation": 50000,
    "Sand": 30000,
    "Water": 5000,
    "Steel / Reinforcement": 70000,
    "Bricks": 20000,
    "Stone Aggregates": 10000,
    "Concrete Contractor": 50000,
    "Formwork / Framework": 30000,
    "Plumbing / Sanitation": 25000,
    "Electrical Work": 35000,
    "Compound Wall / Door Entrance": 40000,
    "Soil": 5000,
    "Cement": 60000
}

# Post-construction breakdown
post_construction_items = {
    "Painting": 20000,
    "Exterior Flooring": 15000,
    "Doors & Windows": 30000,
    "Miscellaneous": 10000
}

# Streamlit inputs for material selection
st.sidebar.subheader("Select Materials")

# Pre-Construction Material Selection
with st.sidebar.expander("Pre-Construction Materials", expanded=False):
    selected_pre_materials = st.multiselect(
        "Select Pre-Construction Materials",
        options=list(pre_construction_items.keys()),
        default=list(pre_construction_items.keys())  # Select all by default
    )

# Main Construction Material Selection
with st.sidebar.expander("Main Construction Materials", expanded=False):
    selected_construction_materials = st.multiselect(
        "Select Main Construction Materials",
        options=list(construction_items.keys()),
        default=list(construction_items.keys())  # Select all by default
    )

# Post-Construction Material Selection
with st.sidebar.expander("Post-Construction Materials", expanded=False):
    selected_post_materials = st.multiselect(
        "Select Post-Construction Materials",
        options=list(post_construction_items.keys()),
        default=list(post_construction_items.keys())  # Select all by default
    )

# Button to predict total cost
if st.button("Predict Total Cost"):
    # Prepare the feature set for the model
    features = pd.DataFrame([[ 
        sq_ft,
        location,  # Pass location directly as a categorical column
        int(bool(selected_pre_materials)),  # 1 if any pre-construction selected, else 0
        int(bool(selected_construction_materials)),  # 1 if any construction selected, else 0
        int(bool(selected_post_materials))  # 1 if any post-construction selected, else 0
    ]], columns=['SquareFootage', 'Location', 'PreConstruction', 'Construction', 'PostConstruction'])

    # Predict total cost using the machine learning model
    predicted_cost = model.predict(features)[0]

    # Calculate the total material costs based on square footage
    total_material_cost = sum(
        [pre_construction_items[item] for item in selected_pre_materials] +
        [construction_items[item] * (sq_ft / 1000) for item in selected_construction_materials] +  # Scale by sq ft
        [post_construction_items[item] for item in selected_post_materials]
    )

    # Calculate final total cost including model prediction and material costs
    final_total_cost = predicted_cost + total_material_cost

    # Display the predicted total cost
    st.subheader("Predicted Total Cost")
    st.write(f"**Predicted Cost:** ₹{final_total_cost:,.2f}")

    # Total expenditure breakdown across all materials
    expenditure_data = {}

    # Pre-construction costs
    for item in selected_pre_materials:
        expenditure_data[item] = pre_construction_items[item]

    # Main construction costs (scaled by sq ft)
    for item in selected_construction_materials:
        expenditure_data[item] = construction_items[item] * (sq_ft / 1000)

    # Post-construction costs
    for item in selected_post_materials:
        expenditure_data[item] = post_construction_items[item]

    # Data for pie chart breakdown
    pie_df = pd.DataFrame(expenditure_data.items(), columns=["Material", "Cost"])

    # Create pie chart if any costs are selected
    if not pie_df.empty:
        fig = px.pie(
            pie_df,
            values='Cost',
            names='Material',
            title="Cost Breakdown by Selected Materials",
            hover_name='Material',
            color_discrete_sequence=px.colors.qualitative.Plotly
        )
        
        # Update pie chart to show names and prices, without percentages
        fig.update_traces(textinfo='label+value')  # Show name and price
        fig.update_layout(showlegend=True)  # Show legend on the left side
        st.plotly_chart(fig)

    # Generate report for download
    report_data = f"""
    Location: {location}
    Square Footage: {sq_ft} sq ft
    BHK Type: {bhk}
    Predicted Total Cost: ₹{final_total_cost:,.2f}
    
    Selected Pre-Construction Materials: {', '.join(selected_pre_materials)}
    Selected Main Construction Materials: {', '.join(selected_construction_materials)}
    Selected Post-Construction Materials: {', '.join(selected_post_materials)}
    
    Detailed Cost Breakdown:
    """
    for item, cost in expenditure_data.items():
        report_data += f"\n - {item}: ₹{cost:,.2f}"

    # Allow users to download the report
    st.download_button(
        label="Download Report (Text)",
        data=report_data,
        file_name="house_price_prediction_report.txt",
        mime="text/plain"
    )

# Footer
st.sidebar.markdown("---")
st.sidebar.write("© 2024 House Price Prediction")

