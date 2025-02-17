# Load trained model and encoders
import streamlit as st
import pandas as pd
from rapidfuzz import process

# Define base ingredient quantities
base_ingredients = {
    "Chicken Biryani": {"Rice": 0.025, "Chicken": 0.15, "Onion": 0.05, "Tomato": 0.04, "Yogurt": 0.03, "Ginger Garlic Paste": 0.01, "Spices": 0.01, "Oil": 0.02, "Cashew": 0.02},
    "Mutton Biryani": {"Rice": 0.025, "Mutton": 0.15, "Onion": 0.06, "Tomato": 0.05, "Yogurt": 0.04, "Ginger Garlic Paste": 0.01, "Spices": 0.015, "Oil": 0.03, "Cashew": 0.02},
    "Egg Curry": {"Eggs": 1, "Onion": 0.04, "Tomato": 0.03, "Spices": 0.005, "Oil": 0.01, "Ginger Garlic Paste": 0.01, "Coconut Milk": 0.02},
    "Fish Curry": {"Fish": 0.15, "Coconut Milk": 0.03, "Onion": 0.05, "Tomato": 0.04, "Tamarind": 0.02, "Oil": 0.015, "Spices": 0.01},
    "Chicken Fry": {"Chicken": 0.12, "Oil": 0.03, "Spices": 0.01, "Onion": 0.03, "Ginger Garlic Paste": 0.01},
    
    # Vegetarian Dishes
    "Vegetable Biryani": {"Rice": 0.025, "Carrot": 0.02, "Beans": 0.02, "Peas": 0.02, "Onion": 0.04, "Tomato": 0.03, "Yogurt": 0.02, "Spices": 0.01, "Oil": 0.02},
    "Sambar": {"Toor Dal": 0.05, "Turmeric": 0.002, "Tomato": 0.03, "Tamarind": 0.01, "Onion": 0.02, "Carrot": 0.02, "Drumstick": 0.02, "Mustard Seeds": 0.001, "Curry Leaves": 0.002, "Oil": 0.01},
    "Rasam": {"Tomato": 0.04, "Tamarind": 0.02, "Garlic": 0.005, "Black Pepper": 0.002, "Cumin": 0.002, "Curry Leaves": 0.002, "Mustard Seeds": 0.001, "Oil": 0.005},
    "Chapati": {"Wheat Flour": 0.12, "Salt": 0.002, "Oil": 0.005},
    "Dosa": {"Rice Flour": 0.15, "Urad Dal": 0.05, "Oil": 0.005},
    "Pulao": {"Basmati Rice": 0.2, "Carrot": 0.03, "Peas": 0.02, "Ghee": 0.01, "Spices": 0.005},
    "Curd Rice": {"Rice": 0.1, "Curd": 0.1, "Mustard Seeds": 0.001, "Green Chili": 0.002, "Curry Leaves": 0.002, "Salt": 0.002},
    "Dal Fry": {"Toor Dal": 0.07, "Ghee": 0.01, "Onion": 0.04, "Tomato": 0.03, "Garlic": 0.005, "Cumin": 0.002, "Spices": 0.005},
    "Paneer Butter Masala": {"Paneer": 0.1, "Tomato": 0.05, "Cashew": 0.01, "Cream": 0.02, "Butter": 0.02, "Spices": 0.01},
    "Aloo Gobi": {"Potato": 0.08, "Cauliflower": 0.08, "Onion": 0.03, "Tomato": 0.03, "Spices": 0.005, "Oil": 0.01},
    "Baingan Bharta": {"Brinjal": 0.12, "Tomato": 0.05, "Onion": 0.04, "Garlic": 0.005, "Spices": 0.005, "Oil": 0.01},
    "Vegetable Kurma": {"Carrot": 0.02, "Beans": 0.02, "Potato": 0.03, "Peas": 0.02, "Coconut Milk": 0.02, "Spices": 0.005, "Oil": 0.01},
    
    # Breakfast Items
    "Idli": {"Rice Flour": 0.12, "Urad Dal": 0.05, "Salt": 0.002},
    "Upma": {"Rava (Semolina)": 0.08, "Ghee": 0.02, "Mustard Seeds": 0.001, "Green Chili": 0.002, "Curry Leaves": 0.002},
    "Poha": {"Flattened Rice": 0.08, "Onion": 0.02, "Potato": 0.03, "Mustard Seeds": 0.001, "Green Chili": 0.002, "Oil": 0.01},
    "Paratha": {"Wheat Flour": 0.15, "Potato": 0.08, "Butter": 0.02, "Spices": 0.005},
    "Bread Omelette": {"Bread": 2, "Eggs": 1, "Butter": 0.02, "Salt": 0.002, "Pepper": 0.002},
    
    # Snacks
    "Samosa": {"Potato": 0.1, "Wheat Flour": 0.1, "Oil": 0.02, "Spices": 0.005},
    "Pakora": {"Besan (Gram Flour)": 0.08, "Onion": 0.05, "Spices": 0.005, "Oil": 0.02},
    "Bonda": {"Potato": 0.08, "Besan (Gram Flour)": 0.06, "Spices": 0.005, "Oil": 0.02}
    }

# Function to find the closest match
def get_closest_match(dish_name, dishes):
    match, score, _ = process.extractOne(dish_name, dishes)
    return match if score > 60 else None

# Streamlit UI
st.title("Ingredient Calculator for Dishes")

# User input
user_dish = st.text_input("Enter dish name:")
num_people = st.number_input("Enter number of people:", min_value=1, step=1)

if st.button("Calculate Ingredients"):
    if not user_dish:
        st.error("Please enter a dish name.")
    else:
        corrected_dish = get_closest_match(user_dish, base_ingredients.keys())
        
        if not corrected_dish:
            st.error(f"'{user_dish}' not found. Please check the spelling!")
        else:
            st.success(f"Ingredients for {num_people} people ({corrected_dish}):")
            data = {ingredient: qty * num_people for ingredient, qty in base_ingredients[corrected_dish].items()}
            
            # Create the DataFrame with numbering starting from 1
            df = pd.DataFrame(list(data.items()), columns=["Ingredient", "Quantity (Kg)"])
            df.index = df.index + 1  # Adjust the index to start from 1
            
            st.table(df)







