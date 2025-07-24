from typing import List, Dict, Optional
from food_database import FoodNutrient, FoodDatabase

class FoodComparator:
    """Class for comparing different foods based on their nutritional values"""
    
    def __init__(self, food_db: FoodDatabase):
        """Initialize FoodComparator with a FoodDatabase instance
        
        Args:
            food_db: Instance of FoodDatabase containing food nutrition data
        """
        self.food_db = food_db
    
    def compare_foods(self, food1: str, food2: str, nutrients: List[str] = None) -> Dict:
        """Compare two foods based on specified nutrients
        
        Args:
            food1: Name of the first food
            food2: Name of the second food
            nutrients: List of nutrients to compare (defaults to all nutrients)
            
        Returns:
            Dictionary containing comparison results
        """
        if nutrients is None:
            nutrients = ['calories', 'fat', 'carbs', 'protein', 'fiber', 'sodium', 'vitamin_c', 'iron']
            
        # Get nutrition data for both foods
        food1_nutrition = self.food_db.get_food_nutrition(food1)
        food2_nutrition = self.food_db.get_food_nutrition(food2)
        
        if food1_nutrition is None or food2_nutrition is None:
            raise ValueError(f"One or both foods not found in database: {food1}, {food2}")
            
        comparison = {
            'food1': food1,
            'food2': food2,
            'comparison': {}
        }
        
        # Compare each nutrient
        for nutrient in nutrients:
            value1 = getattr(food1_nutrition, nutrient, 0)
            value2 = getattr(food2_nutrition, nutrient, 0)
            
            # Calculate percentage difference
            if value1 == 0 and value2 == 0:
                diff_percent = 0
            else:
                diff_percent = ((value1 - value2) / value2) * 100 if value2 != 0 else 100
                
            comparison['comparison'][nutrient] = {
                'food1_value': value1,
                'food2_value': value2,
                'difference': value1 - value2,
                'percentage_diff': diff_percent,
                'better_food': food1 if diff_percent > 0 else food2
            }
            
        return comparison
    
    def find_similar_foods(self, food: str, category: str = None, max_results: int = 5) -> List[str]:
        """Find foods similar to the given food based on nutritional profile
        
        Args:
            food: Name of the food to find similar foods for
            category: Optional category to limit search
            max_results: Maximum number of similar foods to return
            
        Returns:
            List of similar food names
        """
        target_nutrition = self.food_db.get_food_nutrition(food)
        if target_nutrition is None:
            return []
            
        all_foods = self.food_db.food_data
        if category:
            all_foods = all_foods[all_foods['category'] == category]
            
        similarities = []
        for _, row in all_foods.iterrows():
            if row['food_name'] == food:
                continue
                
            # Calculate similarity score based on key nutrients
            score = 0
            for nutrient in ['calories', 'protein', 'fat', 'carbs', 'fiber']:
                value = getattr(target_nutrition, nutrient, 0)
                diff = abs(value - row[nutrient])
                score += diff
                
            similarities.append((row['food_name'], score))
            
        # Sort by similarity score and get top results
        similarities.sort(key=lambda x: x[1])
        return [food[0] for food in similarities[:max_results]]