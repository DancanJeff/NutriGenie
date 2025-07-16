# 🍎 NutriGenie: AI Nutrition Assistant

A personalized nutrition recommendation system that provides tailored dietary advice based on individual health profiles, genetics, and lifestyle factors.

## ✨ Features

- **Personalized Nutrition Plans**: Get customized dietary recommendations based on your age, gender, height, weight, and activity level
- **Health Metrics Dashboard**: Track BMI, daily calorie needs, and macronutrient distribution
- **Food Recommendations**: Receive categorized food suggestions including protein sources, carbohydrates, vegetables, fruits, healthy fats, and superfoods
- **Meal Timing Guidance**: Get optimal meal scheduling recommendations
- **Hydration Planning**: Personalized daily water intake goals and schedules
- **Interactive Visualizations**: Beautiful charts and graphs powered by Plotly and Altair
- **Responsive Design**: Modern, mobile-friendly interface with custom styling

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd nutrigenie
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run streamlit_app.py
```

4. Open your browser and navigate to `http://localhost:8501`

## 📋 Requirements

Create a `requirements.txt` file with the following dependencies:

```
streamlit>=1.28.0
altair>=4.2.0
pandas>=1.5.0
plotly>=5.15.0
```

## 🏗️ Project Structure

```
nutrigenie/
├── streamlit_app.py          # Main Streamlit application
├── nutrition_engine.py       # Core nutrition calculation engine
├── requirements.txt          # Python dependencies
├── README.md                # This file
└── assets/                  # Static assets (if any)
```

## 🔧 Core Components

### `streamlit_app.py`
The main application file containing:
- User interface components
- Input forms and controls
- Data visualization
- Tab-based content organization

### `nutrition_engine.py` (Required)
This file should contain the core functions used by the app:
- `calculate_bmi(weight, height)` - BMI calculation
- `classify_bmi(bmi)` - BMI classification
- `recommend_nutrition(age, bmi, activity, health_conditions, genetic_traits)` - Nutrition recommendations
- `get_calorie_needs(age, weight, height, gender, activity)` - Calorie requirements
- `get_food_recommendations(bmi, activity, health_conditions, genetic_traits)` - Food suggestions
- `get_meal_timing_recommendations(activity, health_conditions)` - Meal timing advice
- `get_hydration_recommendations(age, activity, weight)` - Hydration planning

## 📊 Features Overview

### 1. Health Metrics Tab
- BMI calculation and classification
- Daily calorie requirements
- Macronutrient distribution (protein, carbs, fat)
- Interactive charts and comparisons

### 2. Nutrition Plan Tab
- Personalized dietary recommendations
- Daily calorie breakdown by meal
- Visual meal distribution chart

### 3. Food Recommendations Tab
- Categorized food suggestions:
  - 🥩 Protein Sources
  - 🌾 Carbohydrate Sources
  - 🥬 Vegetable Sources
  - 🍎 Fruit Sources
  - 🥑 Healthy Fats
  - ⭐ Superfoods
- Foods to avoid based on health conditions

### 4. Meal Timing Tab
- Optimal meal scheduling
- Sample daily meal schedule
- Timing recommendations based on activity level

### 5. Hydration Tab
- Daily water intake goals
- Hydration schedule throughout the day
- Practical hydration tips

## 🎨 User Interface

The application features:
- **Responsive sidebar** for user input
- **Tab-based organization** for easy navigation
- **Custom CSS styling** with gradient headers and card layouts
- **Interactive charts** using Plotly Express
- **Color-coded metrics** for quick understanding

## 🔒 Health Considerations

### Supported Health Conditions
- Diabetes
- Hypertension
- Lactose Intolerance
- None (default)

### Genetic Traits Consideration
- Gluten Sensitivity
- Obesity Risk
- High Metabolism
- None (default)

### Fitness Goals
- Weight Loss
- Weight Gain
- Muscle Building
- Maintenance

## 📱 Usage

1. **Fill Profile Information**: Enter your basic details in the sidebar
2. **Select Health Conditions**: Choose relevant health conditions and genetic traits
3. **Set Fitness Goals**: Define your primary fitness objective
4. **Generate Plan**: Click the "Generate My Nutrition Plan" button
5. **Explore Results**: Navigate through the tabs to view your personalized recommendations

## 🛠️ Customization

### Adding New Features
- Extend the `nutrition_engine.py` with additional calculation functions
- Add new tabs in the main application
- Include more health conditions or genetic traits
- Implement additional visualization types

### Styling
- Modify the CSS in the `st.markdown()` sections
- Adjust color schemes in the chart configurations
- Update the gradient backgrounds and card designs

## ⚠️ Important Notes

- This tool provides general nutritional guidance
- Always consult with healthcare professionals for personalized medical advice
- The recommendations are based on general nutritional principles
- Individual needs may vary significantly

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed description
4. Include steps to reproduce any bugs

## 🔮 Future Enhancements

- Integration with fitness tracking APIs
- Meal planning with recipe suggestions
- Shopping list generation
- Progress tracking and analytics
- Multi-language support
- Mobile app version

---

**Built with ❤️ using Streamlit, Plotly, and Python**