from typing import List, Dict, Optional
from food_database import FoodDatabase, FoodNutrient
from food_comparator import FoodComparator
from nutrition_analyzer import NutritionAnalyzer
import random

class SmartRecommendations:
    """Class for generating personalized food recommendations"""
    
    def __init__(self, food_db: FoodDatabase):
        """Initialize SmartRecommendations with a FoodDatabase instance
        
        Args:
            food_db: Instance of FoodDatabase containing food nutrition data
        """
        self.food_db = food_db
        self.analyzer = NutritionAnalyzer(food_db)
        self.comparator = FoodComparator(food_db)
        
    def get_personalized_recommendations(
        self,
        user_profile: Dict,
        current_intake: List[Dict],
        dietary_restrictions: List[str] = None,
        num_recommendations: int = 5
    ) -> List[Dict]:
        """Generate personalized food recommendations based on user profile and current intake
        
        Args:
            user_profile: Dictionary containing user information (age, weight, height, etc.)
            current_intake: List of current food intake with quantities
            dietary_restrictions: List of dietary restrictions (e.g., 'gluten-free', 'vegan')
            num_recommendations: Number of recommendations to generate
            
        Returns:
            List of recommended foods with nutritional information
        """
        # Analyze current intake
        current_nutrition = self.analyzer.analyze_daily_intake(
            [food['food'] for food in current_intake],
            [food['quantity'] for food in current_intake]
        )
        
        # Get nutritional needs based on profile
        age = user_profile.get('age', 30)
        weight = user_profile.get('weight', 70)  # kg
        height = user_profile.get('height', 170)  # cm
        gender = user_profile.get('gender', 'male')
        activity_level = user_profile.get('activity_level', 'moderate')
        
        # Calculate nutritional gaps
        nutritional_gaps = self._calculate_nutritional_gaps(current_nutrition, user_profile)
        
        # Get all foods
        all_foods = self.food_db.food_data
        
        # Apply dietary restrictions
        if dietary_restrictions:
            for restriction in dietary_restrictions:
                if restriction == 'gluten-free':
                    all_foods = all_foods[all_foods['gluten_free'] == True]
                elif restriction == 'vegan':
                    all_foods = all_foods[all_foods['category'].isin(['vegetables', 'fruits', 'legumes'])]
                elif restriction == 'dairy-free':
                    all_foods = all_foods[all_foods['category'] != 'dairy']
        
        # Find foods that complement current intake
        recommended_foods = []
        for _, row in all_foods.iterrows():
            # Skip if food doesn't address nutritional gaps
            if not self._addresses_nutritional_gaps(row, nutritional_gaps):
                continue
                
            # Skip if food is too similar to current intake
            if self._is_similar_to_current_intake(row, current_intake):
                continue
                
            recommended_foods.append(row)
            
            # Stop if we have enough recommendations
            if len(recommended_foods) >= num_recommendations * 2:  # Get extra to filter
                break
        
        # Sort by how well they address nutritional gaps
        recommended_foods.sort(
            key=lambda x: self._nutritional_gap_score(x, nutritional_gaps),
            reverse=True
        )
        
        # Return formatted recommendations
        return [{
            'food_name': food['food_name'],
            'calories': food['calories'],
            'protein': food['protein'],
            'carbs': food['carbs'],
            'fat': food['fat'],
            'fiber': food['fiber'],
            'category': food['category']
        } for food in recommended_foods[:num_recommendations]]

    def _calculate_nutritional_gaps(self, current_nutrition: Dict, user_profile: Dict) -> Dict:
        """Calculate nutritional gaps based on current intake and user needs"""
        gaps = {}
        
        # Calculate basic needs
        calorie_needs = self._calculate_calorie_needs(
            user_profile['age'],
            user_profile['weight'],
            user_profile['height'],
            user_profile['gender'],
            user_profile['activity_level']
        )
        protein_needs = self._calculate_protein_needs(user_profile['weight'])
        
        # Calculate gaps
        gaps['calories'] = calorie_needs - current_nutrition.get('calories', 0)
        gaps['protein'] = protein_needs - current_nutrition.get('protein', 0)
        gaps['fiber'] = 25 - current_nutrition.get('fiber', 0)  # General recommendation
        
        return gaps
    
    def _addresses_nutritional_gaps(self, food: Dict, gaps: Dict) -> bool:
        """Check if food addresses nutritional gaps"""
        scores = []
        
        # Check if food helps with any gaps
        for nutrient, gap in gaps.items():
            if gap > 0:  # If there's a gap
                value = food.get(nutrient, 0)
                if value > 0:  # If food provides this nutrient
                    scores.append(value / gap)
        
        # Food addresses gaps if it provides at least one nutrient that's needed
        return len(scores) > 0 and max(scores) > 0.1
    
    def _is_similar_to_current_intake(self, food: Dict, current_intake: List[Dict]) -> bool:
        """Check if food is too similar to current intake"""
        for intake in current_intake:
            if self.comparator.compare_foods(
                food['food_name'],
                intake['food'],
                ['calories', 'protein', 'fat', 'carbs']
            )['comparison']['calories']['percentage_diff'] < 20:
                return True
        return False
    
    def _nutritional_gap_score(self, food: Dict, gaps: Dict) -> float:
        """Calculate how well a food addresses nutritional gaps"""
        score = 0
        for nutrient, gap in gaps.items():
            if gap > 0:
                value = food.get(nutrient, 0)
                score += value / gap
        return score
    
    def _calculate_calorie_needs(
        self,
        age: int,
        weight: float,
        height: float,
        gender: str,
        activity_level: str
    ) -> float:
        """Calculate daily calorie needs based on user profile"""
        # Using Mifflin-St Jeor Equation
        if gender.lower() == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
            
        # Activity multiplier
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'heavy': 1.725,
            'very_heavy': 1.9
        }
        
        return bmr * activity_multipliers.get(activity_level.lower(), 1.55)
    
    def _calculate_protein_needs(self, weight: float) -> float:
        """Calculate daily protein needs based on weight"""
        # General recommendation: 0.8g - 1.2g protein per kg of body weight
        return weight * 1.0  # Using 1.0 as a balanced value
    
    def compare_recommendations(
        self,
        current_diet: List[str],
        new_recommendations: List[str],
        nutrients: List[str] = None
    ) -> Dict:
        """Compare current diet with new recommendations
        
        Args:
            current_diet: List of current food items
            new_recommendations: List of recommended food items
            nutrients: Specific nutrients to compare
            
        Returns:
            Comparison of nutritional changes between current diet and recommendations
        """
        return self.comparator.compare_foods(current_diet[0], new_recommendations[0], nutrients)