import math
from typing import List, Dict, Tuple
from enum import Enum
from food_database import FoodDatabase, FoodCategory, FoodNutrient

class ActivityLevel(Enum):
    SEDENTARY = 1.2
    MODERATE = 1.55
    ACTIVE = 1.725

class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"

def calculate_bmi(weight: float, height: float) -> float:
    """Calculate BMI given weight in kg and height in cm"""
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 1)

def classify_bmi(bmi: float) -> str:
    """Classify BMI into categories"""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obesity"

def calculate_bmr(age: int, weight: float, height: float, gender: str) -> float:
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    return bmr

def calculate_tdee(bmr: float, activity: str) -> float:
    """Calculate Total Daily Energy Expenditure"""
    activity_multipliers = {
        "Sedentary": 1.2,
        "Moderate": 1.55,
        "Active": 1.725
    }
    return bmr * activity_multipliers.get(activity, 1.55)

def get_calorie_needs(age: int, weight: float, height: float, gender: str, activity: str) -> Dict[str, float]:
    """Calculate daily calorie needs and macronutrient distribution"""
    bmr = calculate_bmr(age, weight, height, gender)
    tdee = calculate_tdee(bmr, activity)
    
    # Macronutrient distribution based on activity level
    if activity == "Active":
        protein_ratio = 0.30
        carb_ratio = 0.45
        fat_ratio = 0.25
    elif activity == "Moderate":
        protein_ratio = 0.25
        carb_ratio = 0.50
        fat_ratio = 0.25
    else:  # Sedentary
        protein_ratio = 0.25
        carb_ratio = 0.45
        fat_ratio = 0.30
    
    return {
        "calories": round(tdee),
        "protein_g": round((tdee * protein_ratio) / 4),
        "carbs_g": round((tdee * carb_ratio) / 4),
        "fat_g": round((tdee * fat_ratio) / 9),
        "protein_percent": round(protein_ratio * 100),
        "carbs_percent": round(carb_ratio * 100),
        "fat_percent": round(fat_ratio * 100)
    }

def get_food_recommendations(bmi: float, activity: str, health_conditions: List[str], genetic_traits: List[str]) -> Dict[str, List[str]]:
    """Get personalized food recommendations based on profile"""
    recommendations = {
        "protein_sources": [],
        "carb_sources": [],
        "vegetable_sources": [],
        "fruit_sources": [],
        "healthy_fats": [],
        "superfoods": [],
        "avoid_foods": []
    }
    
    # Base recommendations
    base_proteins = ["Lean chicken breast", "Fish (salmon, tuna)", "Eggs", "Greek yogurt", "Tofu", "Lentils"]
    base_carbs = ["Quinoa", "Brown rice", "Sweet potatoes", "Oats", "Whole wheat bread"]
    base_vegetables = ["Broccoli", "Spinach", "Kale", "Bell peppers", "Carrots", "Tomatoes"]
    base_fruits = ["Berries", "Apples", "Bananas", "Oranges", "Avocado"]
    base_fats = ["Olive oil", "Nuts (almonds, walnuts)", "Seeds (chia, flax)", "Fatty fish"]
    
    # Adjust based on BMI
    if bmi < 18.5:  # Underweight
        recommendations["protein_sources"] = base_proteins + ["Protein shakes", "Nut butters"]
        recommendations["carb_sources"] = base_carbs + ["Pasta", "Rice", "Potatoes"]
        recommendations["healthy_fats"] = base_fats + ["Coconut oil", "Cheese", "Whole milk"]
    elif bmi > 25:  # Overweight/Obese
        recommendations["protein_sources"] = ["Lean proteins: " + ", ".join(base_proteins[:4])]
        recommendations["carb_sources"] = ["Complex carbs: " + ", ".join(base_carbs[:3])]
        recommendations["vegetable_sources"] = ["High-fiber vegetables: " + ", ".join(base_vegetables)]
        recommendations["avoid_foods"] = ["Processed foods", "Sugary drinks", "Refined carbs", "Fried foods"]
    else:  # Normal weight
        recommendations["protein_sources"] = base_proteins
        recommendations["carb_sources"] = base_carbs
        recommendations["healthy_fats"] = base_fats
    
    recommendations["vegetable_sources"] = base_vegetables
    recommendations["fruit_sources"] = base_fruits
    
    # Activity-based adjustments
    if activity == "Active":
        recommendations["superfoods"] = ["Beetroot (nitrates)", "Tart cherry juice", "Chocolate milk (post-workout)", "Bananas"]
    elif activity == "Sedentary":
        recommendations["superfoods"] = ["Green tea", "Berries (antioxidants)", "Leafy greens", "Nuts"]
    
    # Health condition adjustments
    if "Diabetes" in health_conditions:
        recommendations["carb_sources"] = ["Low-GI carbs: Steel-cut oats, quinoa, legumes"]
        recommendations["superfoods"].extend(["Cinnamon", "Bitter melon", "Chromium-rich foods"])
        recommendations["avoid_foods"].extend(["High-sugar fruits", "White bread", "Sugary snacks"])
    
    if "Hypertension" in health_conditions:
        recommendations["superfoods"].extend(["Potassium-rich foods (bananas, spinach)", "Garlic", "Hibiscus tea"])
        recommendations["avoid_foods"].extend(["High-sodium foods", "Processed meats", "Canned foods"])
    
    if "Lactose Intolerance" in health_conditions:
        recommendations["protein_sources"] = [p for p in base_proteins if "yogurt" not in p.lower()]
        recommendations["protein_sources"].extend(["Lactose-free dairy", "Plant-based proteins"])
        recommendations["avoid_foods"].extend(["Regular dairy products", "Milk-based supplements"])
    
    # Genetic trait adjustments
    if "Gluten Sensitivity" in genetic_traits:
        recommendations["carb_sources"] = ["Gluten-free grains: Rice, quinoa, buckwheat"]
        recommendations["avoid_foods"].extend(["Wheat products", "Barley", "Rye"])
    
    if "Obesity Risk" in genetic_traits:
        recommendations["superfoods"].extend(["Metabolism boosters: Green tea, chili peppers", "High-protein foods"])
        recommendations["avoid_foods"].extend(["High-calorie processed foods", "Sugary beverages"])
    
    if "High Metabolism" in genetic_traits:
        recommendations["carb_sources"].extend(["Higher calorie carbs: Dates, dried fruits"])
        recommendations["healthy_fats"].extend(["Calorie-dense fats: Nuts, seeds, olive oil"])
    
    return recommendations

def recommend_nutrition(age: int, bmi: float, activity: str, health_conditions: List[str], genetic_traits: List[str]) -> List[str]:
    """Generate comprehensive nutrition recommendations"""
    recommendations = []
    
    # BMI-based recommendations
    if bmi < 18.5:
        recommendations.append("🎯 Focus on healthy weight gain: Increase caloric intake with nutrient-dense foods")
        recommendations.append("💪 Eat frequent, smaller meals throughout the day")
        recommendations.append("🥤 Consider protein smoothies between meals")
    elif bmi > 25:
        recommendations.append("🎯 Focus on sustainable weight loss: Create a moderate caloric deficit")
        recommendations.append("🍽️ Practice portion control and mindful eating")
        recommendations.append("💧 Increase water intake before meals")
    else:
        recommendations.append("✅ Maintain your healthy weight with balanced nutrition")
    
    # Activity-based recommendations
    if activity == "Active":
        recommendations.append("🏃‍♂️ Pre-workout: Consume carbs 1-2 hours before exercise")
        recommendations.append("🍌 Post-workout: Eat protein + carbs within 30 minutes")
        recommendations.append("💧 Stay well-hydrated, especially during intense training")
    elif activity == "Sedentary":
        recommendations.append("🚶‍♀️ Consider incorporating light physical activity to boost metabolism")
        recommendations.append("🍎 Focus on fiber-rich foods to maintain satiety")
    
    # Age-based recommendations
    if age > 50:
        recommendations.append("🦴 Ensure adequate calcium and vitamin D for bone health")
        recommendations.append("🧠 Include omega-3 fatty acids for brain health")
        recommendations.append("💊 Consider B12 supplementation (consult your doctor)")
    elif age < 25:
        recommendations.append("🌱 Focus on building healthy eating habits for life")
        recommendations.append("💪 Ensure adequate protein for growth and development")
    
    # Health condition-specific recommendations
    if "Diabetes" in health_conditions:
        recommendations.append("📊 Monitor blood sugar levels and pair carbs with protein")
        recommendations.append("🕐 Maintain consistent meal timing")
        recommendations.append("🥗 Choose low glycemic index foods")
    
    if "Hypertension" in health_conditions:
        recommendations.append("🧂 Limit sodium intake to less than 1,500mg per day")
        recommendations.append("🍌 Include potassium-rich foods in your diet")
        recommendations.append("🍷 Limit alcohol consumption")
    
    if "Lactose Intolerance" in health_conditions:
        recommendations.append("🥛 Choose lactose-free dairy or plant-based alternatives")
        recommendations.append("💊 Consider lactase enzyme supplements when consuming dairy")
    
    # Genetic trait-specific recommendations
    if "Gluten Sensitivity" in genetic_traits:
        recommendations.append("🌾 Choose certified gluten-free grains and products")
        recommendations.append("📖 Read food labels carefully for hidden gluten")
    
    if "Obesity Risk" in genetic_traits:
        recommendations.append("⚖️ Pay extra attention to portion sizes and calorie density")
        recommendations.append("🔥 Include metabolism-boosting foods like green tea and spices")
    
    if "High Metabolism" in genetic_traits:
        recommendations.append("🍽️ Eat more frequent, calorie-dense meals")
        recommendations.append("🥜 Include healthy fats and complex carbs for sustained energy")
    
    # General recommendations
    recommendations.append("🥗 Aim for 5-7 servings of fruits and vegetables daily")
    recommendations.append("💧 Drink at least 8 glasses of water per day")
    recommendations.append("😴 Maintain consistent meal timing to support your circadian rhythm")
    recommendations.append("📱 Consider using a food diary to track your intake")
    
    return recommendations

def get_meal_timing_recommendations(activity: str, health_conditions: List[str]) -> List[str]:
    """Get meal timing recommendations"""
    timing_tips = []
    
    if activity == "Active":
        timing_tips.append("🕐 Eat main meals 2-3 hours before intense workouts")
        timing_tips.append("🍌 Quick snack 30-60 minutes before exercise if needed")
        timing_tips.append("🥤 Post-workout meal within 30-60 minutes")
    
    if "Diabetes" in health_conditions:
        timing_tips.append("⏰ Maintain consistent meal times to help regulate blood sugar")
        timing_tips.append("🍽️ Consider smaller, more frequent meals")
    
    if not timing_tips:
        timing_tips.append("🍽️ Eat regular, balanced meals every 3-4 hours")
        timing_tips.append("🌅 Don't skip breakfast - it kick-starts your metabolism")
    
    return timing_tips

def get_hydration_recommendations(age: int, activity: str, weight: float) -> Dict[str, str]:
    """Calculate hydration needs"""
    base_water = weight * 35  # ml per kg
    
    if activity == "Active":
        base_water *= 1.2
    elif activity == "Moderate":
        base_water *= 1.1
    
    if age > 65:
        base_water *= 1.1  # Older adults need more water
    
    return {
        "daily_water_ml": round(base_water),
        "daily_water_cups": round(base_water / 240),  # 240ml per cup
        "recommendation": f"Aim for {round(base_water/240)} cups ({round(base_water/1000, 1)}L) of water daily"
    }

class EnhancedNutritionEngine:
    def __init__(self):
        self.food_db = FoodDatabase()
    
    def get_specific_food_recommendations(self, bmi, activity, health_conditions, genetic_traits):
        """Get specific food recommendations instead of generic categories"""
        recommendations = {}
        
        # High-protein foods for muscle building
        if activity == "Active":
            protein_foods = self.food_db.get_food_by_category(FoodCategory.MEAT)
            # Sort by protein content
            protein_rich = []
            for food in protein_foods[:10]:  # Top 10
                nutrition = self.food_db.get_food_nutrition(food)
                if nutrition and nutrition.protein > 20:  # High protein
                    protein_rich.append({
                        'food': food,
                        'protein': nutrition.protein,
                        'calories': nutrition.calories
                    })
            recommendations['high_protein'] = sorted(protein_rich, 
                                                   key=lambda x: x['protein'], 
                                                   reverse=True)[:5]
        
        # Low-sodium foods for hypertension
        if "Hypertension" in health_conditions:
            all_foods = self.food_db.food_data['food'].tolist()
            low_sodium = []
            for food in all_foods[:50]:  # Sample foods
                nutrition = self.food_db.get_food_nutrition(food)
                if nutrition and nutrition.sodium < 100:  # Low sodium
                    low_sodium.append({
                        'food': food,
                        'sodium': nutrition.sodium,
                        'potassium': nutrition.potassium
                    })
            recommendations['low_sodium'] = sorted(low_sodium, 
                                                 key=lambda x: x['sodium'])[:10]
        
        return recommendations