# app.py

import streamlit as st
import altair as alt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from nutrition_engine import (
    calculate_bmi, classify_bmi, recommend_nutrition,
    get_calorie_needs, get_food_recommendations,
    get_meal_timing_recommendations, get_hydration_recommendations
)
from food_database import FoodDatabase, FoodCategory
from meal_planner import MealPlanner
from nutrition_analyzer import NutritionAnalyzer
from food_comparator import FoodComparator
from smart_recommendations import SmartRecommendations

import time
import traceback

# Initialize session state to prevent resets
def initialize_session_state():
    """Initialize all session state variables to prevent resets"""
    if 'app_initialized' not in st.session_state:
        st.session_state.app_initialized = True
        st.session_state.user_profile = {}
        st.session_state.logged_foods = []
        st.session_state.selected_category = FoodCategory
        st.session_state.last_activity = time.time()

    st.session_state.last_activity = time.time()

# Add error handling wrapper for critical functions
def safe_execute(func, *args, **kwargs):
    """Execute a function safely with error handling"""
    try:
         return func(*args, **kwargs)
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.write("Debug info", traceback.format_exc())
        return None

# Session health check
def check_session_health():
    """Check if session is still healthy and recover if needed"""
    try:
        if 'last_activity' in st.session_state:
            time_since_activity = time.time() - st.session_state.last_activity
            if time_since_activity > 1800:  # 30 minutes of inactivity
                st.warning("Session expired due to inactivity. Please refresh the page.")
    except Exception as e:
        st.error(f"Session health check failed: {str(e)}")

# Initialize food database
@st.cache_data
def load_food_database():
    try:
        return FoodDatabase()
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        return None

food_db = load_food_database()
if food_db is None:
    st.error("❌ Failed to initialize food database. Please check your database configuration.")
    st.stop()

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

# Food Logger Functions


def create_food_logger():
    st.subheader("📝 Daily Food Logger")

    # Initialize session state for logged foods
    if 'logged_foods' not in st.session_state:
        st.session_state.logged_foods = []

    # Add food form
    with st.form("add_food_form"):
        col1, col2 = st.columns(2)

        with col1:
            food_search = st.text_input(
                "Search for food:", placeholder="e.g., apple, chicken breast")

        with col2:
            quantity = st.number_input(
                "Quantity (grams):", min_value=1, value=100)

        selected_food = None
        if food_search:
            try:
                matching_foods = food_db.search_food(food_search)
                if matching_foods:
                    selected_food = st.selectbox("Select food:", matching_foods)
                else:
                    st.warning( "No matching foods found. Try a different search term.")
            except Exception as e:
                st.error(f" Error searching for food: {str(e)}")
                selected_food = None
        if st.form_submit_button("➕ Add Food"):
            if selected_food:
                st.session_state.logged_foods.append({
                    'food': selected_food,
                    'quantity': quantity,
                    'timestamp': datetime.now()
                })
                st.success(f"✅ Added {selected_food} ({quantity}g)")
                st.rerun()

    # Display logged foods
    if st.session_state.logged_foods:
        st.subheader(" Today's Nutrition Summary")

        try:
            # Create summary
            analyzer = NutritionAnalyzer(food_db)
            foods = [item['food'] for item in st.session_state.logged_foods]
            quantities = [item['quantity'] for item in st.session_state.logged_foods]

            daily_nutrition = analyzer.analyze_daily_intake(foods, quantities)

            # Display nutrition summary in metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Calories", f"{daily_nutrition['calories']:.0f}")
            with col2:
                st.metric("Protein", f"{daily_nutrition['protein']:.1f}g")
            with col3:
                st.metric("Carbs", f"{daily_nutrition['carbs']:.1f}g")
            with col4:
                st.metric("Fat", f"{daily_nutrition['fat']:.1f}g")

            # Additional nutrition metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Fiber", f"{daily_nutrition['fiber']:.1f}g")
            with col2:
                st.metric("Vitamin C", f"{daily_nutrition['vitamin_c']:.1f}mg")
            with col3:
                st.metric("Iron", f"{daily_nutrition['iron']:.1f}mg")
            with col4:
                st.metric("Calcium", f"{daily_nutrition['calcium']:.1f}mg")

            # Nutrition visualization
            st.subheader("📈 Macronutrient Breakdown")
            macro_data = pd.DataFrame({
                'Nutrient': ['Protein', 'Carbs', 'Fat'],
                'Grams': [daily_nutrition['protein'], daily_nutrition['carbs'], daily_nutrition['fat']]
            })

            fig = px.pie(macro_data, values='Grams', names='Nutrient',
                         title="Today's Macronutrient Distribution",
                         color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error analyzing nutrition:{str(e)}")
        # Display food list
        st.subheader("🍽️ Today's Logged Foods")

        for i, item in enumerate(st.session_state.logged_foods):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

                with col1:
                    st.markdown(f"<div class='logged-food-item'><strong>{item['food']}</strong></div>",
                                unsafe_allow_html=True)
                with col2:
                    st.write(f"{item['quantity']}g")
                with col3:
                    # Get nutrition for this specific food item
                    nutrition = food_db.get_food_nutrition(item['food'])
                    if nutrition:
                        calories_per_100g = nutrition.calories
                        item_calories = (calories_per_100g *
                                         item['quantity']) / 100
                        st.write(f"{item_calories:.0f} kcal")
                with col4:
                    if st.button("🗑️", key=f"remove_{i}", help="Remove this food"):
                        st.session_state.logged_foods.pop(i)
                        st.rerun()

        # Clear all foods button
        if st.button("🗑️ Clear All Foods", type="secondary"):
            st.session_state.logged_foods = []
            st.rerun()

        # Export functionality
        st.subheader("📤 Export Data")
        if st.button("📄 Export Today's Log as CSV"):
            # Create DataFrame for export
            export_data = []
            for item in st.session_state.logged_foods:
                nutrition = food_db.get_food_nutrition(item['food'])
                if nutrition:
                    calories_per_100g = nutrition.calories
                    item_calories = (calories_per_100g *
                                     item['quantity']) / 100
                    protein_per_100g = nutrition.protein
                    item_protein = (protein_per_100g * item['quantity']) / 100

                    export_data.append({
                        'Food': item['food'],
                        'Quantity (g)': item['quantity'],
                        'Calories': item_calories,
                        'Protein (g)': item_protein,
                        'Timestamp': item['timestamp']
                    })

            if export_data:
                df = pd.DataFrame(export_data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"nutrition_log_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

    else:
        st.info("👆 Start by adding some foods to your daily log!")

        # Show some example foods
        st.subheader("💡 Popular Foods to Track")
        example_foods = [
            "🍎 Apple", "🥚 Egg", "🍌 Banana", "🥛 Milk", "🍞 Bread",
            "🐟 Salmon", "🥗 Lettuce", "🍚 Rice", "🥑 Avocado", "🍗 Chicken"
        ]

        cols = st.columns(5)
        for i, food in enumerate(example_foods):
            with cols[i % 5]:
                st.markdown(f"• {food}")


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
generate_plan = st.sidebar.button(
    "🚀 Generate My Nutrition Plan", type="primary")

# Main Content
if generate_plan:
    # Calculate metrics
    try:
        bmi = calculate_bmi(weight, height)
        bmi_status = classify_bmi(bmi)
        calorie_needs = get_calorie_needs(age, weight, height, gender, activity)
        nutrition_plan = recommend_nutrition(age, bmi, activity, health_conditions, genetic_traits)
        food_recommendations = get_food_recommendations(bmi, activity, health_conditions, genetic_traits)
        meal_timing = get_meal_timing_recommendations(activity, health_conditions)
        hydration = get_hydration_recommendations(age, activity, weight)
        
        # Success message
        st.success("✅ Your personalized nutrition plan has been generated!")
    except Exception as e:
        st.error(f"Error generating nutrition plan: {str(e)}")
        st.stop()
    # Create tabs for organized content
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs([
        "📊 Health Metrics",
        "🍽️ Nutrition Plan",
        "🥗 Food Recommendations",
        "⏰ Meal Timing",
        "💧 Hydration",
        "🔍 Food Database",
        "🍱 Meal Plan",
        "🧪 Analyze My Intake",
        "📊 Compare Foods",
        "📝 Food Logger",
        "🧠 Smart Recommendations"
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
            st.metric(
                "Protein", f"{calorie_needs['protein_g']}g", f"{calorie_needs['protein_percent']}%")
        with col2:
            st.metric(
                "Carbohydrates", f"{calorie_needs['carbs_g']}g", f"{calorie_needs['carbs_percent']}%")
        with col3:
            st.metric(
                "Fat", f"{calorie_needs['fat_g']}g", f"{calorie_needs['fat_percent']}%")

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
            st.metric("Daily Water Goal",
                      f"{hydration['daily_water_cups']} cups")

        with col2:
            st.metric("Daily Water Goal",
                      f"{hydration['daily_water_ml']/1000:.1f} liters")

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

    with tab6:
        st.subheader("🔍 Food Database Explorer")

        # Food search
        search_query = st.text_input(
            "Search for foods:", placeholder="e.g., chicken, apple, rice")
        matching_foods = []  # Initialize empty list

        if search_query:
            try:
                matching_foods = food_db.search_food(search_query)
                if matching_foods:
                    st.write(f"Found {len(matching_foods)} matching foods:")
                else:
                    st.warning("No matching foods found.")
            except Exception as e:
                st.error(f"Error searching for food: {str(e)}")
        # Let user select a food
        selected_food = None
        if matching_foods:
            selected_food = st.selectbox("Select a food for detailed nutrition:", matching_foods)

        if selected_food:
            try:
                nutrition = food_db.get_food_nutrition(selected_food)

                if nutrition:
                    # Display nutrition info
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Calories", f"{nutrition.calories:.1f}")
                        st.metric("Protein", f"{nutrition.protein:.1f}g")
                        st.metric("Carbs", f"{nutrition.carbs:.1f}g")
                        st.metric("Fat", f"{nutrition.fat:.1f}g")
                    with col2:
                        st.metric("Fiber", f"{nutrition.fiber:.1f}g")
                        st.metric("Vitamin C", f"{nutrition.vitamin_c:.1f}mg")
                        st.metric("Iron", f"{nutrition.iron:.1f}mg")
                        st.metric("Calcium", f"{nutrition.calcium:.1f}mg")

                    with col3:
                        st.metric("Sodium", f"{nutrition.sodium:.1f}mg")
                        st.metric("Potassium", f"{nutrition.potassium:.1f}mg")
                        st.metric("Nutrition Density",
                              f"{nutrition.nutrition_density:.2f}")

                    # Macronutrient breakdown chart
                    macro_data = pd.DataFrame({
                        'Nutrient': ['Protein', 'Carbs', 'Fat'],
                        'Grams': [nutrition.protein, nutrition.carbs, nutrition.fat]
                   })

                    fig = px.pie(macro_data, values='Grams', names='Nutrient',
                                 title=f"Macronutrient Breakdown - {selected_food}")
                    st.plotly_chart(fig, use_container_width=True)    
                else:
                    st.warning(f"No nutrition data available for {selected_food}")
            except Exception as e:
                st.error(f"Error retrieving nutrition data: {str(e)}")
    # Browse food category
    st.markdown("---")
    st.subheader("📂 Browse by Category")

    category_names = {
        FoodCategory.DAIRY: "🥛 Dairy",
        FoodCategory.MEAT: "🥩 Meat",
        FoodCategory.VEGETABLES: "🥬 Vegetables",
        FoodCategory.FRUITS: "🍎 Fruits",
        FoodCategory.GRAINS: "🌾 Grains",
        FoodCategory.BEVERAGES: "🥤 Beverages",
        FoodCategory.SNACKS: "🍿 Snacks",
        FoodCategory.DESSERTS: "🍰 Desserts"
    }
    try:
       # Get the list of category enums for the selectbox options
        selected_category = st.selectbox("Select a category:",
                                      list(category_names.keys()),
                                      format_func=lambda x: category_names[x],
                                      key="category_selector")

        if selected_category:
            st.session_state.selected_category = selected_category
            try:   
               category_foods = food_db.get_food_by_category(
                   st.session_state.selected_category)

               if category_foods:
                   st.success(f"✅ Found {len(category_foods)} foods in {category_names[st.session_state.selected_category]}")

                   # Display foods in a more organized way
                   if len(category_foods) > 30:
                        st.info(f"Showing first 30 of {len(category_foods)} foods. Use search to find specific items.")

                   # Create columns for better layout
                   cols = st.columns(3)
                   for i, food in enumerate(category_foods[:30]):
                       with cols[i % 3]:
                            st.write(f"• {food}")
               else:
                    st.warning(f"⚠️ No foods found in {category_names[st.session_state.selected_category]}")

            except Exception as e:
                st.error(f"❌ Error loading category: {str(e)}")
                st.write("Debug info:", traceback.format_exc())

    except Exception as e:
            st.error(f"❌ Error with category selection: {str(e)}")


    with tab7:
        st.subheader("🍱 AI-Powered Meal Planner")

        st.info(
            "This tool helps generate meals that meet your nutrition targets using real foods.")

        # Example: Get targets from user input
        target_calories = st.number_input(
            "Target Calories", min_value=1000, max_value=4000, value=2000)
        target_protein = st.number_input(
            "Target Protein (g)", min_value=30, max_value=200, value=100)
        target_carbs = st.number_input(
            "Target Carbs (g)", min_value=50, max_value=400, value=250)
        target_fat = st.number_input(
            "Target Fat (g)", min_value=20, max_value=150, value=70)

        if st.button("Generate Meal Plan"):
            planner = MealPlanner(food_db)
            plan = planner.create_meal_plan(
                target_calories, target_protein, target_carbs, target_fat)

            for meal, items in plan.items():
                st.subheader(f"🍽️ {meal.capitalize()}")
                if items:
                    for item in items:
                        st.markdown(f"• **{item['food']}** — {item['calories']} kcal | "
                                    f"{item['protein']}g P / {item['carbs']}g C / {item['fat']}g F")
                else:
                    st.warning("No suitable items found.")

    with tab8:
        st.subheader("🧪 Analyze My Daily Nutritional Intake")

        st.markdown(
            "Enter the foods you've eaten today and the quantity (in grams):")

        analyzer = NutritionAnalyzer(food_db)

        food_inputs = []
        quantity_inputs = []

        for i in range(5):  # Let user enter up to 5 items
            col1, col2 = st.columns([2, 1])
            with col1:
                food = st.text_input(f"Food {i+1}", key=f"food_{i}")
            with col2:
                qty = st.number_input(
                    f"Quantity (g)", min_value=0.0, step=10.0, key=f"qty_{i}")

        if food and qty > 0:
            food_inputs.append(food)
            quantity_inputs.append(qty)

        if st.button("🔍 Analyze"):
            intake = analyzer.analyze_daily_intake(
                food_inputs, quantity_inputs)
            st.success("Total Nutrition Intake:")
            st.json(intake)

            # You can use sample target values or calculate dynamically
            target_nutrition = {
                'calories': 2000,
                'protein': 75,
                'carbs': 250,
                'fat': 70,
                'fiber': 25,
                'vitamin_c': 90,
                'iron': 18,
                'calcium': 1000
            }

            gaps = analyzer.identify_nutritional_gaps(intake, target_nutrition)

            if gaps:
                st.warning("⚠️ Nutritional Gaps Detected:")
                for nutrient, gap in gaps.items():
                    st.markdown(
                        f"- **{nutrient.capitalize()}**: {gap['current']:.1f} / {gap['target']} → {gap['percentage']:.1f}% of target")
            else:
                st.success("✅ You're meeting your nutritional goals!")
        else:
            st.warning("Please enter at least one food item with quantity.")

    with tab9:
        st.subheader("🍽️ Compare Two Foods")

        try:
            comparator = FoodComparator(food_db)

            col1, col2 = st.columns(2)
            with col1:
                st.session_state.food1 = st.text_input("Enter first food", key="compare_food1", value=st.session_state.get('food1', ''))
            with col2:
                st.session_state.food2 = st.text_input("Enter second food", key="compare_food2", value=st.session_state.get('food2', ''))

            def compare_foods(food1, food2):
                try:
                    # First check if foods exist in database
                    food1_matches = food_db.search_food(food1)
                    food2_matches = food_db.search_food(food2)
                    
                    if not food1_matches:
                        st.error(f"❌ Food '{food1}' not found in database. Try a different search term.")
                        return
                    if not food2_matches:
                        st.error(f"❌ Food '{food2}' not found in database. Try a different search term.")
                        return
                    
                    # Use exact matches or first match
                    exact_food1 = food1 if food1 in food1_matches else food1_matches[0]
                    exact_food2 = food2 if food2 in food2_matches else food2_matches[0]
                    
                    if exact_food1 != food1:
                        st.info(f"Using closest match for '{food1}': {exact_food1}")
                    if exact_food2 != food2:
                        st.info(f"Using closest match for '{food2}': {exact_food2}")
                    
                    result = comparator.compare_foods(exact_food1, exact_food2)
                    
                    if result:
                        st.success(f"Comparison between **{exact_food1}** and **{exact_food2}**")
 
                        for nutrient, data in result['comparison'].items():
                            col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
                            with col1:
                                st.metric(f"{nutrient.capitalize()} ({food1})", f"{data['food1_value']:.1f}")
                            with col2:
                                st.metric(f"{nutrient.capitalize()} ({food2})", f"{data['food2_value']:.1f}")
                            with col3:
                                st.metric("Diff", f"{data['difference']:.1f}")
                            with col4:
                                st.metric("Winner", data['winner'])
                    else:
                        st.warning("❗ Could not retrieve nutrition info for one or both foods.")
                except Exception as e:
                    st.error(f"❌ Error comparing foods: {str(e)}")
                    st.write("Debug info:", traceback.format_exc())
            if food1 and food2:
                compare_foods(food1, food2)
            else:
                st.warning("Please enter both food names to compare.")
        
        except Exception as e:
            st.error(f"❌ Error initializing food comparator: {str(e)}")

    with tab10:
        create_food_logger()

    with tab11:
        st.subheader("🤖 AI-Powered Food Recommendations")

    # Assume user profile already exists from earlier tabs
        user_profile = {
            'age': age,
            'weight': weight,
            'height': height,
            'gender': gender,
            'activity': activity
        }

    if 'logged_foods' in st.session_state and st.session_state.logged_foods:
        analyzer = NutritionAnalyzer(food_db)
        foods = [f['food'] for f in st.session_state.logged_foods]
        quantities = [f['quantity'] for f in st.session_state.logged_foods]
        current_intake = analyzer.analyze_daily_intake(foods, quantities)

        engine = SmartRecommendations(food_db)
        smart_recs = engine.get_personalized_recommendations(
            user_profile, current_intake)

        st.subheader("🔍 Recommended Foods to Improve Your Nutrition:")
        for rec in smart_recs:
            st.markdown(f"• {rec}")
    else:
        st.info("Please log your food intake first in the 📝 Food Logger tab.")


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
        st.info(
            "**Meal frequency**: 3 main meals + 2-3 snacks works well for most people")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🍎 NutriGenie - Your AI Nutrition Assistant</p>
    <p><small>⚠️ This tool provides general nutritional guidance. Always consult with healthcare professionals for personalized medical advice.</small></p>
</div>
""", unsafe_allow_html=True)
