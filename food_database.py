import pandas as pd
from typing import List, Dict, Optional
import os
from dataclasses import dataclass
from enum import Enum

@dataclass
class FoodNutrient:
    """Data structure for storing food nutrient information"""
    food_name: str
    calories: float
    fat: float
    saturated_fats: float
    monounsaturated_fats: float
    polyunsaturated_fats: float
    carbs: float
    sugars: float
    protein: float
    fiber: float
    cholesterol: float
    sodium: float
    water: float
    vitamin_a: float
    vitamin_b1: float
    vitamin_b2: float
    vitamin_b3: float
    vitamin_b5: float
    vitamin_b6: float
    vitamin_b12: float
    vitamin_c: float
    vitamin_d: float
    vitamin_e: float
    vitamin_k: float
    calcium: float
    copper: float
    iron: float
    magnesium: float
    manganese: float
    phosphorus: float
    potassium: float
    selenium: float
    zinc: float
    nutrition_density: float

class FoodCategory(Enum):
    """Enum for food categories"""
    DAIRY = "dairy"
    MEAT = "meat"
    VEGETABLES = "vegetables"
    FRUITS = "fruits"
    GRAINS = "grains"
    BEVERAGES = "beverages"
    SNACKS = "snacks"
    DESSERTS = "desserts"

class FoodDatabase:
    def __init__(self, data_directory: str = "FOOD DATASET/FINAL FOOD DATASET"):
        """Initialize the food database
        
        Args:
            data_directory: Path to the directory containing food data CSV files
        """
        self.data_directory = data_directory
        self.food_data = self._load_food_data()
        self.food_by_category = self._categorize_food()

    def _load_food_data(self) -> pd.DataFrame:
        """Load all food data CSV files into a single DataFrame"""
        # Get all CSV files in the directory
        csv_files = [f for f in os.listdir(self.data_directory) 
                    if f.endswith('.csv') and 'METADATA' not in f]
        
        # Load each file and concatenate
        dfs = []
        for file in csv_files:
            df = pd.read_csv(os.path.join(self.data_directory, file))
            dfs.append(df)
        
        return pd.concat(dfs, ignore_index=True)

    def _categorize_food(self) -> Dict[FoodCategory, List[str]]:
        """Categorize foods based on their properties"""
        categories = {
            FoodCategory.DAIRY: [],
            FoodCategory.MEAT: [],
            FoodCategory.VEGETABLES: [],
            FoodCategory.FRUITS: [],
            FoodCategory.GRAINS: [],
            FoodCategory.BEVERAGES: [],
            FoodCategory.SNACKS: [],
            FoodCategory.DESSERTS: []
        }
        
        # List of beverage-related keywords
        beverage_keywords = [
            'milk', 'coffee', 'tea', 'juice', 'water', 'soda', 'smoothie', 'shake', 'latte',
            'cocoa', 'lemonade', 'beverage', 'cocktail', 'alcohol', 'alcoholic',
            'wine', 'beer', 'cider', 'liqueur', 'margarita', 'martini', 'whiskey',
            'vodka', 'gin', 'rum', 'tequila', 'sangria', 'punch',
            'iced', 'hot', 'iced tea', 'hot chocolate',
            'espresso', 'cappuccino', 'frappuccino', 'matcha', 'chai', 'mocha',
            'protein shake', 'energy drink', 'sports drink', 'electrolyte',
            'tonic', 'seltzer', 'sparkling', 'mineral water', 'flavored water',
            'milkshake'
        ]

        for _, row in self.food_data.iterrows():
            food_name = row['food'].lower()
            
            # Check if it's a beverage
            if any(bev in food_name for bev in beverage_keywords):
                categories[FoodCategory.BEVERAGES].append(food_name)
            
            # Check other categories
            elif 'cheese' in food_name or 'milk' in food_name:
                categories[FoodCategory.DAIRY].append(food_name)
            elif any(meat in food_name for meat in ['chicken', 'beef', 'pork', 'fish', 'ham']):
                categories[FoodCategory.MEAT].append(food_name)
            elif any(veg in food_name for veg in ['veggie', 'vegetable', 'salad']):
                categories[FoodCategory.VEGETABLES].append(food_name)
            elif any(fruit in food_name for fruit in ['apple', 'banana', 'orange', 'berry']):
                categories[FoodCategory.FRUITS].append(food_name)
            elif any(grain in food_name for grain in ['rice', 'wheat', 'oat', 'bread']):
                categories[FoodCategory.GRAINS].append(food_name)
            elif any(snack in food_name for snack in ['crisp', 'chips', 'nut', 'popcorn']):
                categories[FoodCategory.SNACKS].append(food_name)
            elif any(dessert in food_name for dessert in ['cake', 'pie', 'pudding', 'chocolate']):
                categories[FoodCategory.DESSERTS].append(food_name)
        
        return categories

    def get_food_by_category(self, category: FoodCategory) -> List[str]:
        """Get list of foods in a specific category"""
        return self.food_by_category.get(category, [])

    def get_food_nutrition(self, food_name: str) -> Optional[FoodNutrient]:
        """Get detailed nutrition information for a specific food"""
        food_name = food_name.lower()
        row = self.food_data[self.food_data['food'].str.lower() == food_name].iloc[0]
        
        if row.empty:
            return None
            
        return FoodNutrient(
            food_name=row['food'],
            calories=row['Caloric Value'],
            fat=row['Fat'],
            saturated_fats=row['Saturated Fats'],
            monounsaturated_fats=row['Monounsaturated Fats'],
            polyunsaturated_fats=row['Polyunsaturated Fats'],
            carbs=row['Carbohydrates'],
            sugars=row['Sugars'],
            protein=row['Protein'],
            fiber=row['Dietary Fiber'],
            cholesterol=row['Cholesterol'],
            sodium=row['Sodium'],
            water=row['Water'],
            vitamin_a=row['Vitamin A'],
            vitamin_b1=row['Vitamin B1'],
            vitamin_b2=row['Vitamin B2'],
            vitamin_b3=row['Vitamin B3'],
            vitamin_b5=row['Vitamin B5'],
            vitamin_b6=row['Vitamin B6'],
            vitamin_b12=row['Vitamin B12'],
            vitamin_c=row['Vitamin C'],
            vitamin_d=row['Vitamin D'],
            vitamin_e=row['Vitamin E'],
            vitamin_k=row['Vitamin K'],
            calcium=row['Calcium'],
            copper=row['Copper'],
            iron=row['Iron'],
            magnesium=row['Magnesium'],
            manganese=row['Manganese'],
            phosphorus=row['Phosphorus'],
            potassium=row['Potassium'],
            selenium=row['Selenium'],
            zinc=row['Zinc'],
            nutrition_density=row['Nutrition Density']
        )

    def search_food(self, query: str) -> List[str]:
        """Search for foods matching the query"""
        query = query.lower()
        return [food for food in self.food_data['food'].str.lower() 
                if query in food]

    def get_nutrient_profile(self, food_name: str) -> Dict[str, float]:
        """Get a simplified nutrient profile for a food"""
        food = self.get_food_nutrition(food_name)
        if not food:
            return {}
            
        return {
            'calories': food.calories,
            'protein': food.protein,
            'carbs': food.carbs,
            'fat': food.fat,
            'fiber': food.fiber,
            'vitamin_c': food.vitamin_c,
            'iron': food.iron,
            'calcium': food.calcium
        }
