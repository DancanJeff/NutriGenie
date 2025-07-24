from food_database import FoodDatabase
# meal_planner.py
class MealPlanner:
    def __init__(self, food_db: FoodDatabase):
        self.food_db = food_db
    
    def create_meal_plan(self, target_calories, target_protein, target_carbs, target_fat):
        """Create a meal plan meeting specific nutritional targets"""
        meal_plan = {
            'breakfast': [],
            'lunch': [],
            'dinner': [],
            'snacks': []
        }
        
        # Breakfast - 25% of daily calories
        breakfast_calories = target_calories * 0.25
        breakfast_foods = self._find_foods_for_calories(breakfast_calories, 
                                                       ['eggs', 'oatmeal', 'yogurt', 'banana'])
        meal_plan['breakfast'] = breakfast_foods
        
        # Similar logic for other meals...
        
        return meal_plan
    
    def _find_foods_for_calories(self, target_calories, food_hints):
        """Find foods that match calorie target"""
        suitable_foods = []
        
        for hint in food_hints:
            matching_foods = self.food_db.search_food(hint)
            for food in matching_foods:
                nutrition = self.food_db.get_food_nutrition(food)
                if nutrition and abs(nutrition.calories - target_calories) < 100:
                    suitable_foods.append({
                        'food': food,
                        'calories': nutrition.calories,
                        'protein': nutrition.protein,
                        'carbs': nutrition.carbs,
                        'fat': nutrition.fat
                    })
        
        return suitable_foods[:3]  # Return top 3 matches