# app.py

import streamlit as st
import altair as alt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from nutrition_engine import (
    calculate_bmi, classify_bmi, recommend_nutrition, 
    get_calorie_needs, get_food_recommendations, 
    get_meal_timing_recommendations, get_hydration_recommendations
)

# Page configuration
st.set_page_config(
    page_title="NutriGenie: AI Nutrition Assistant", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .food-category {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🍎 NutriGenie: AI Nutrition Assistant</h1>
    <p>Personalized nutrition recommendations based on your health, genetics, and lifestyle</p>
</div>
""", unsafe_allow_html=True)

# Sidebar: User Information
st.sidebar.header("👤 User Profile")

# Basic Information
st.sidebar.subheader("Basic Information")
age = st.sidebar.number_input("Age", min_value=1, max_value=120, value=30)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=250, value=170)
weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=300, value=70)

# Activity Level
st.sidebar.subheader("Activity Level")
activity = st.sidebar.selectbox(
    "Select your activity level", 
    ["Sedentary", "Moderate", "Active"],
    help="Sedentary: Little to no exercise, Moderate: Exercise 3-5 times/week, Active: Exercise 6+ times/week"
)

# Health and Genetics
st.sidebar.subheader("Health Information")
health_conditions = st.sidebar.multiselect(
    "Health conditions:",
    ["Diabetes", "Hypertension", "Lactose Intolerance", "None"],
    default=["None"]
)

genetic_traits = st.sidebar.multiselect(
    "Genetic predispositions:",
    ["Gluten Sensitivity", "Obesity Risk", "High Metabolism", "None"],
    default=["None"]
)

# Goals
st.sidebar.subheader("Goals")
fitness_goal = st.sidebar.selectbox(
    "Primary fitness goal:",
    ["Weight Loss", "Weight Gain", "Muscle Building", "Maintenance"]
)

# Generate Plan Button
generate_plan = st.sidebar.button("🚀 Generate My Nutrition Plan", type="primary")

# Main Content
if generate_plan:
    # Calculate metrics
    bmi = calculate_bmi(weight, height)
    bmi_status = classify_bmi(bmi)
    calorie_needs = get_calorie_needs(age, weight, height, gender, activity)
    nutrition_plan = recommend_nutrition(age, bmi, activity, health_conditions, genetic_traits)
    food_recommendations = get_food_recommendations(bmi, activity, health_conditions, genetic_traits)
    meal_timing = get_meal_timing_recommendations(activity, health_conditions)
    hydration = get_hydration_recommendations(age, activity, weight)
    
    # Success message
    st.success("✅ Your personalized nutrition plan has been generated!")
    
    # Create tabs for organized content
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Health Metrics", 
        "🍽️ Nutrition Plan", 
        "🥗 Food Recommendations", 
        "⏰ Meal Timing", 
        "💧 Hydration"
    ])
    
    with tab1:
        st.subheader("📊 Your Health Metrics")
        
        # BMI Section
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>BMI</h3>
                <h2>{bmi}</h2>
                <p>{bmi_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Daily Calories</h3>
                <h2>{calorie_needs['calories']}</h2>
                <p>Based on your profile</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Activity Level</h3>
                <h2>{activity}</h2>
                <p>Current lifestyle</p>
            </div>
            """, unsafe_allow_html=True)
        
        # BMI Comparison Chart
        st.subheader("BMI Comparison")
        bmi_data = pd.DataFrame({
            'Category': ['Underweight', 'Normal', 'Overweight', 'Obesity', 'You'],
            'BMI': [17, 22, 27, 32, bmi],
            'Color': ['#81C784', '#4CAF50', '#FF9800', '#F44336', '#9C27B0']
        })
        
        fig_bmi = px.bar(
            bmi_data, 
            x='Category', 
            y='BMI', 
            color='Color',
            title="BMI Category Comparison",
            color_discrete_map={color: color for color in bmi_data['Color']}
        )
        fig_bmi.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_bmi, use_container_width=True)
        
        # Macronutrient Distribution
        st.subheader("Macronutrient Distribution")
        macro_data = pd.DataFrame({
            'Nutrient': ['Protein', 'Carbohydrates', 'Fat'],
            'Percentage': [calorie_needs['protein_percent'], calorie_needs['carbs_percent'], calorie_needs['fat_percent']],
            'Grams': [calorie_needs['protein_g'], calorie_needs['carbs_g'], calorie_needs['fat_g']]
        })
        
        fig_macro = px.pie(
            macro_data, 
            values='Percentage', 
            names='Nutrient',
            title="Daily Macronutrient Breakdown",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1']
        )
        st.plotly_chart(fig_macro, use_container_width=True)
        
        # Detailed macronutrient info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Protein", f"{calorie_needs['protein_g']}g", f"{calorie_needs['protein_percent']}%")
        with col2:
            st.metric("Carbohydrates", f"{calorie_needs['carbs_g']}g", f"{calorie_needs['carbs_percent']}%")
        with col3:
            st.metric("Fat", f"{calorie_needs['fat_g']}g", f"{calorie_needs['fat_percent']}%")
    
    with tab2:
        st.subheader("🍽️ Personalized Nutrition Plan")
        
        # Display recommendations in a nice format
        for i, recommendation in enumerate(nutrition_plan, 1):
            st.markdown(f"**{i}.** {recommendation}")
        
        # Calorie breakdown
        st.subheader("📈 Daily Calorie Breakdown")
        calorie_breakdown = pd.DataFrame({
            'Meal': ['Breakfast', 'Morning Snack', 'Lunch', 'Afternoon Snack', 'Dinner', 'Evening Snack'],
            'Calories': [
                calorie_needs['calories'] * 0.25,  # Breakfast
                calorie_needs['calories'] * 0.10,  # Morning snack
                calorie_needs['calories'] * 0.30,  # Lunch
                calorie_needs['calories'] * 0.10,  # Afternoon snack
                calorie_needs['calories'] * 0.20,  # Dinner
                calorie_needs['calories'] * 0.05   # Evening snack
            ]
        })
        
        fig_meals = px.bar(
            calorie_breakdown, 
            x='Meal', 
            y='Calories',
            title="Suggested Calorie Distribution Throughout the Day",
            color='Calories',
            color_continuous_scale='viridis'
        )
        fig_meals.update_layout(height=400)
        st.plotly_chart(fig_meals, use_container_width=True)
    
    with tab3:
        st.subheader("🥗 Food Recommendations")
        
        # Display food recommendations by category
        categories = [
            ("🥩 Protein Sources", "protein_sources"),
            ("🌾 Carbohydrate Sources", "carb_sources"),
            ("🥬 Vegetable Sources", "vegetable_sources"),
            ("🍎 Fruit Sources", "fruit_sources"),
            ("🥑 Healthy Fats", "healthy_fats"),
            ("⭐ Superfoods", "superfoods")
        ]
        
        for title, key in categories:
            if key in food_recommendations and food_recommendations[key]:
                st.markdown(f"### {title}")
                for food in food_recommendations[key]:
                    st.markdown(f"• {food}")
                st.markdown("---")
        
        # Foods to avoid
        if food_recommendations.get("avoid_foods"):
            st.markdown("### ⚠️ Foods to Limit or Avoid")
            for food in food_recommendations["avoid_foods"]:
                st.markdown(f"• {food}")
    
    with tab4:
        st.subheader("⏰ Meal Timing Recommendations")
        
        for timing in meal_timing:
            st.markdown(f"• {timing}")
        
        # Sample meal schedule
        st.subheader("📅 Sample Daily Meal Schedule")
        meal_schedule = pd.DataFrame({
            'Time': ['7:00 AM', '10:00 AM', '1:00 PM', '4:00 PM', '7:00 PM', '9:00 PM'],
            'Meal': ['Breakfast', 'Morning Snack', 'Lunch', 'Afternoon Snack', 'Dinner', 'Evening Snack'],
            'Calories': [
                int(calorie_needs['calories'] * 0.25),
                int(calorie_needs['calories'] * 0.10),
                int(calorie_needs['calories'] * 0.30),
                int(calorie_needs['calories'] * 0.10),
                int(calorie_needs['calories'] * 0.20),
                int(calorie_needs['calories'] * 0.05)
            ]
        })
        
        st.dataframe(meal_schedule, use_container_width=True)
    
    with tab5:
        st.subheader("💧 Hydration Plan")
        
        # Hydration metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Daily Water Goal", f"{hydration['daily_water_cups']} cups")
        
        with col2:
            st.metric("Daily Water Goal", f"{hydration['daily_water_ml']/1000:.1f} liters")
        
        st.info(hydration['recommendation'])
        
        # Water intake throughout the day
        st.subheader("💧 Suggested Water Intake Schedule")
        water_schedule = pd.DataFrame({
            'Time': ['Wake up', 'Before breakfast', 'Mid-morning', 'Before lunch', 
                    'Afternoon', 'Before dinner', 'Evening'],
            'Amount (cups)': [2, 1, 1, 1, 2, 1, 1],
            'Purpose': ['Rehydrate after sleep', 'Prepare for meal', 'Maintain energy', 
                       'Aid digestion', 'Afternoon boost', 'Evening hydration', 'Light hydration']
        })
        
        st.dataframe(water_schedule, use_container_width=True)
        
        # Hydration tips
        st.subheader("💡 Hydration Tips")
        hydration_tips = [
            "💧 Start your day with a glass of water",
            "🍋 Add lemon or cucumber for flavor",
            "⏰ Set reminders to drink water regularly",
            "🥤 Monitor urine color - pale yellow is ideal",
            "🏃‍♂️ Increase intake during exercise",
            "🌡️ Drink more in hot weather"
        ]
        
        for tip in hydration_tips:
            st.markdown(f"• {tip}")

else:
    # Welcome message when no plan is generated
    st.info("👈 Please fill in your profile information in the sidebar and click 'Generate My Nutrition Plan' to get started!")
    
    # Display some general nutrition tips
    st.subheader("💡 General Nutrition Tips")
    general_tips = [
        "🥗 Eat a variety of colorful fruits and vegetables",
        "💧 Stay hydrated throughout the day",
        "🍽️ Practice portion control",
        "🏃‍♂️ Combine good nutrition with regular exercise",
        "😴 Get adequate sleep for optimal metabolism",
        "📱 Consider tracking your food intake",
        "👨‍⚕️ Consult healthcare providers for personalized advice"
    ]
    
    for tip in general_tips:
        st.markdown(f"• {tip}")
    
    # Sample nutrition facts
    st.subheader("📊 Did You Know?")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Protein needs**: 0.8-1.2g per kg of body weight for most adults")
        st.info("**Fiber intake**: 25-35g per day for optimal digestive health")
    
    with col2:
        st.info("**Water needs**: About 35ml per kg of body weight daily")
        st.info("**Meal frequency**: 3 main meals + 2-3 snacks works well for most people")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🍎 NutriGenie - Your AI Nutrition Assistant</p>
    <p><small>⚠️ This tool provides general nutritional guidance. Always consult with healthcare professionals for personalized medical advice.</small></p>
</div>
""", unsafe_allow_html=True)