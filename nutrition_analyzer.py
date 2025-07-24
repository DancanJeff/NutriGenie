from typing import List, Dict
from food_database import FoodDatabase
# nutrition_analyzer.py
class NutritionAnalyzer:
    def __init__(self, food_db: FoodDatabase):
        self.food_db = food_db
    
    def analyze_daily_intake(self, consumed_foods: List[str], quantities: List[float]):
        """Analyze nutritional intake from consumed foods"""
        total_nutrition = {
            'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0,
            'fiber': 0, 'vitamin_c': 0, 'iron': 0, 'calcium': 0
        }
        
        for food, quantity in zip(consumed_foods, quantities):
            nutrition = self.food_db.get_food_nutrition(food)
            if nutrition:
                # Scale by quantity (assuming 100g portions)
                scale_factor = quantity / 100
                total_nutrition['calories'] += nutrition.calories * scale_factor
                total_nutrition['protein'] += nutrition.protein * scale_factor
                total_nutrition['carbs'] += nutrition.carbs * scale_factor
                total_nutrition['fat'] += nutrition.fat * scale_factor
                total_nutrition['fiber'] += nutrition.fiber * scale_factor
                total_nutrition['vitamin_c'] += nutrition.vitamin_c * scale_factor
                total_nutrition['iron'] += nutrition.iron * scale_factor
                total_nutrition['calcium'] += nutrition.calcium * scale_factor
        
        return total_nutrition
    
    def identify_nutritional_gaps(self, intake: Dict, targets: Dict):
        """Identify nutritional deficiencies"""
        gaps = {}
        
        for nutrient, target in targets.items():
            current = intake.get(nutrient, 0)
            if current < target * 0.8:  # Less than 80% of target
                gaps[nutrient] = {
                    'current': current,
                    'target': target,
                    'deficit': target - current,
                    'percentage': (current / target) * 100
                }
        
        return gaps