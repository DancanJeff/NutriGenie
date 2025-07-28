# 🍎 NutriGenie: AI Nutrition Assistant

A comprehensive, AI-powered nutrition recommendation system that provides personalized dietary advice, food logging, meal planning, and nutritional analysis based on individual health profiles, genetics, and lifestyle factors.

## ✨ Key Features

### Core Functionality
- **Personalized Nutrition Plans**: Customized dietary recommendations based on age, gender, height, weight, activity level, health conditions, and genetic traits
- **Health Metrics Dashboard**: BMI calculation, daily calorie needs, macronutrient distribution with interactive visualizations
- **Daily Food Logger**: Track food intake with comprehensive nutrition analysis and export capabilities
- **AI-Powered Meal Planner**: Generate optimized meal plans based on nutrition targets
- **Food Database Explorer**: Search and browse extensive food database with detailed nutrition information
- **Smart Food Recommendations**: AI-driven suggestions based on current intake and nutritional gaps
- **Food Comparison Tool**: Side-by-side nutritional comparison of different foods
- **Nutrition Analysis**: Analyze daily intake and identify nutritional gaps

### Advanced Features
- **Meal Timing Optimization**: Personalized meal scheduling recommendations
- **Hydration Planning**: Custom water intake goals with daily schedules
- **Genetic Integration**: Nutrigenomic recommendations based on genetic predispositions
- **Health Condition Awareness**: Tailored advice for diabetes, hypertension, lactose intolerance
- **Interactive Visualizations**: Beautiful charts and graphs powered by Plotly
- **Real-time Analysis**: Live nutrition tracking and gap identification
- **Export Functionality**: Download food logs as CSV files

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
streamlit run nutrigenie_app.py
```

4. Open your browser and navigate to `http://localhost:8501`

## 📋 Requirements

Create a `requirements.txt` file with the following dependencies:

```
streamlit>=1.28.0
altair>=4.2.0
pandas>=1.5.0
plotly>=5.15.0
numpy>=1.21.0
scikit-learn>=1.0.0
```

## 🏗️ Project Structure

```
nutrigenie/
├── nutrigenie_app.py         # Main Streamlit application
├── nutrition_engine.py       # Core nutrition calculation engine
├── food_database.py          # Food database management and search
├── meal_planner.py           # AI-powered meal planning system
├── nutrition_analyzer.py     # Daily intake analysis and gap identification
├── food_comparator.py        # Food comparison functionality
├── smart_recommendations.py  # AI-driven personalized recommendations
├── requirements.txt          # Python dependencies
├── README.md                # This file
└── assets/                  # Static assets (if any)
```

## 🔧 Core Components

### `nutrigenie_app.py`
The main application file containing:
- 11 comprehensive tabs with full functionality
- User interface components and forms
- Interactive data visualization
- Session state management with error handling
- Food logging system with export capabilities
- Real-time nutrition analysis

### Required Module Files

#### `nutrition_engine.py`
Core nutrition calculation functions:
- `calculate_bmi(weight, height)` - BMI calculation and classification
- `classify_bmi(bmi)` - BMI status determination
- `recommend_nutrition()` - Personalized nutrition recommendations
- `get_calorie_needs()` - Daily calorie requirements calculation
- `get_food_recommendations()` - Categorized food suggestions
- `get_meal_timing_recommendations()` - Optimal meal scheduling
- `get_hydration_recommendations()` - Personalized hydration planning

#### `food_database.py`
Food database management:
- `FoodDatabase` class - Main database interface
- `FoodCategory` enum - Food categorization system
- `search_food()` - Intelligent food search functionality
- `get_food_nutrition()` - Detailed nutrition information retrieval
- `get_food_by_category()` - Category-based food browsing

#### `meal_planner.py`
Intelligent meal planning:
- `MealPlanner` class - AI-powered meal generation
- `create_meal_plan()` - Generate balanced meal plans based on targets
- Optimization algorithms for nutritional balance

#### `nutrition_analyzer.py`
Advanced nutrition analysis:
- `NutritionAnalyzer` class - Daily intake analysis
- `analyze_daily_intake()` - Comprehensive nutrition breakdown
- `identify_nutritional_gaps()` - Gap analysis and recommendations

#### `food_comparator.py`
Food comparison system:
- `FoodComparator` class - Side-by-side food analysis
- `compare_foods()` - Detailed nutritional comparison with winners

#### `smart_recommendations.py`
AI-powered recommendations:
- `SmartRecommendations` class - Personalized suggestion engine
- `get_personalized_recommendations()` - Context-aware food suggestions

## 📊 Application Tabs Overview

### 1. 📊 Health Metrics
- BMI calculation and visualization
- Daily calorie requirements
- Macronutrient distribution charts
- Activity level assessment
- Health status indicators

### 2. 🍽️ Nutrition Plan
- Personalized dietary recommendations
- Daily calorie breakdown by meal
- Meal distribution visualization
- Comprehensive nutrition guidance

### 3. 🥗 Food Recommendations
- Categorized food suggestions:
  - 🥩 Protein Sources
  - 🌾 Carbohydrate Sources
  - 🥬 Vegetable Sources
  - 🍎 Fruit Sources
  - 🥑 Healthy Fats
  - ⭐ Superfoods
- Foods to avoid based on health conditions

### 4. ⏰ Meal Timing
- Personalized meal scheduling
- Sample daily meal schedule
- Timing optimization based on activity level

### 5. 💧 Hydration
- Daily water intake goals
- Hourly hydration schedule
- Hydration tips and recommendations

### 6. 🔍 Food Database
- Comprehensive food search functionality
- Detailed nutrition information display
- Category-based food browsing
- Interactive nutrition charts

### 7. 🍱 Meal Plan
- AI-powered meal plan generation
- Target-based meal optimization
- Balanced nutrition distribution
- Custom calorie and macronutrient targets

### 8. 🧪 Analyze My Intake
- Daily nutrition analysis
- Nutritional gap identification
- Target vs. actual comparison
- Comprehensive intake assessment

### 9. 📊 Compare Foods
- Side-by-side food comparison
- Nutritional winner identification
- Detailed nutrient analysis
- Smart food search and matching

### 10. 📝 Food Logger
- Daily food intake tracking
- Real-time nutrition calculations
- Comprehensive nutrition summary
- CSV export functionality
- Interactive food management

### 11. 🧠 Smart Recommendations
- AI-driven personalized suggestions
- Context-aware recommendations
- Based on current intake and goals
- Intelligent gap-filling suggestions

## 🎨 UI/UX Features

- **Modern Design**: Custom CSS with gradient headers and metric cards
- **Responsive Layout**: Mobile-friendly multi-column layouts
- **Interactive Charts**: Plotly-powered visualizations with hover effects
- **Real-time Updates**: Live nutrition calculations and updates
- **Error Handling**: Comprehensive error management with user feedback
- **Session Management**: Persistent state across interactions
- **Export Functionality**: CSV download capabilities
- **Search Intelligence**: Fuzzy matching and suggestion systems

## 🛠️ Technical Architecture

### Error Handling & Reliability
- Comprehensive try-catch blocks throughout
- Session health monitoring
- Safe execution wrappers for critical functions
- Graceful degradation on errors
- Debug information for troubleshooting

### Performance Optimizations
- `@st.cache_data` for database loading
- Efficient session state management
- Optimized chart rendering
- Smart data loading strategies

### Data Management
- Persistent session state
- Real-time calculation updates
- Efficient food database searches
- CSV export capabilities

## 🔒 Health & Safety Considerations

### Supported Health Conditions
- Diabetes management
- Hypertension considerations
- Lactose intolerance accommodations
- Custom health condition support

### Genetic Traits Integration
- Gluten sensitivity considerations
- Obesity risk factors
- Metabolic rate adjustments
- Personalized genetic recommendations

### Fitness Goals Support
- Weight loss optimization
- Weight gain strategies
- Muscle building nutrition
- Maintenance planning

## 📱 Usage Guide

### Getting Started
1. **Complete Profile**: Fill in basic information in the sidebar
2. **Health Details**: Select relevant health conditions and genetic traits
3. **Set Goals**: Define your primary fitness objective
4. **Generate Plan**: Click "Generate My Nutrition Plan"
5. **Explore Features**: Navigate through all 11 tabs for comprehensive analysis

### Advanced Usage
1. **Daily Logging**: Use the Food Logger to track daily intake
2. **Meal Planning**: Generate custom meal plans based on targets
3. **Food Comparison**: Compare nutritional values of different foods
4. **Gap Analysis**: Identify and address nutritional deficiencies
5. **Export Data**: Download your nutrition logs for external analysis

## 🔧 Customization & Extension

### Adding New Features
- Extend nutrition calculation algorithms
- Add new food categories or health conditions
- Implement additional visualization types
- Create new analysis modules

### Database Expansion
- Add new food items to the database
- Extend nutrition profile attributes
- Implement additional food categories
- Add regional food variations

## ⚠️ Important Disclaimers

- This tool provides general nutritional guidance based on established principles
- Always consult healthcare professionals for personalized medical advice
- Individual nutritional needs may vary based on specific health conditions
- The app is designed for educational and informational purposes
- Genetic recommendations are based on general research, not personalized genetic testing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Implement your changes with proper error handling
4. Add comprehensive documentation
5. Test across all application tabs
6. Commit changes (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Create a Pull Request

## 🐛 Troubleshooting

### Common Issues
- **Food Database Loading**: Check database file integrity and permissions
- **Session State Resets**: Ensure proper session state initialization
- **Chart Rendering**: Verify Plotly installation and data format
- **Export Functionality**: Check file permissions and data availability

### Debug Features
- Comprehensive error messages with stack traces
- Session health monitoring
- Debug information display options
- Safe execution wrappers for critical functions

## 🔮 Future Enhancements

### Planned Features
- **Recipe Integration**: Meal planning with detailed recipes
- **Shopping Lists**: Automated grocery list generation
- **Progress Tracking**: Long-term nutrition and health analytics
- **API Integration**: Connect with fitness trackers and health apps
- **Multi-user Support**: Family nutrition planning
- **Mobile App**: Native iOS and Android applications

### Advanced Analytics
- **Trend Analysis**: Long-term nutrition pattern recognition
- **Predictive Modeling**: Future health outcome predictions
- **Social Features**: Community nutrition challenges
- **Professional Integration**: Dietitian collaboration tools

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support & Community

For support and questions:
1. **Documentation**: Review this comprehensive README
2. **Issues**: Check existing GitHub issues
3. **Bug Reports**: Create detailed issue reports with reproduction steps
4. **Feature Requests**: Propose new features with use cases
5. **Community**: Join discussions and share experiences

## 📧 Contact

For technical questions or collaboration opportunities, please create an issue in the repository.

---

**Built with ❤️ using Streamlit, Plotly, Pandas, and Python**

*Empowering healthier lives through intelligent nutrition guidance*
