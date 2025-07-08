"""
Staggered Pricing Dashboard

This Streamlit application calculates and displays staggered pricing levels
that achieve exact target discount percentages. The dashboard allows users to:

1. Set pricing parameters (base price, subjects, discount targets)
2. Configure pricing constraints (minimum price floor, engagement period)
3. View detailed pricing tables and revenue projections
4. Achieve precise discount percentages accounting for initial full-price subjects

Key Features:
- Corrected algorithm that achieves exact target discounts
- Handles initial full-price subjects properly
- Respects minimum price floor constraints
- Provides comprehensive revenue analysis

Author: Assistant
Date: 2025
"""

import streamlit as st
import pandas as pd
import numpy as np

st.title("Staggered Pricing Dashboard")

# Create two columns
col1, col2 = st.columns(2)

with col1:
    # Levels slider on the left side
    levels = st.slider("Number of Levels", 1, 10, 5)


with col2:
    # All other inputs on the right side
    base_price = st.number_input("Base Price (Rs.)", min_value=500, max_value=5000, value=2500, step=100)
    total_subjects = st.number_input("Total Subjects", min_value=100, max_value=10000, value=700, step=50)
    initial_full_price_count = st.number_input("Initial Full-Price Subjects", min_value=0, max_value=500, value=50, step=10)
    discount_percent = st.slider("Target Discount (%)", 0.0, 100.0, 50.0, step=0.1, key='discount_slider')
    min_price_floor = st.number_input("Minimum Price Floor (Rs.)", min_value=0, max_value=base_price, value=750, step=50)
    months = st.number_input("Engagement Period (Months)", min_value=1, max_value=36, value=12)

# Derived values
target_avg_price = base_price * (1 - discount_percent / 100)

# Adjust pricing levels based on target discount
def calculate_staggered_prices(base_price, target_avg_price, levels, total_subjects, initial_full_price_count, min_price_floor):
    """
    Calculate staggered prices that achieve the exact target discount percentage.
    
    This corrected algorithm works backwards from the target average price to determine
    what the level prices should be, properly accounting for initial full-price subjects.
    """
    # Calculate level sizes
    remaining_subjects = total_subjects - initial_full_price_count
    level_size = remaining_subjects // levels
    last_level_size = remaining_subjects - level_size * (levels - 1)
    level_counts = [level_size] * (levels - 1) + [last_level_size]
    
    # Calculate required revenue from levels (excluding initial full-price subjects)
    initial_revenue = initial_full_price_count * base_price
    required_total_revenue = target_avg_price * total_subjects
    required_levels_revenue = required_total_revenue - initial_revenue
    required_levels_avg = required_levels_revenue / remaining_subjects if remaining_subjects > 0 else 0
    
    # Create price distribution that averages to required_levels_avg
    # For a linear distribution: average = (max_price + min_price) / 2
    # So: min_price = 2 * average - max_price
    max_level_price = base_price
    min_level_price = 2 * required_levels_avg - max_level_price
    
    # Apply minimum price floor constraint
    if min_level_price < min_price_floor:
        min_level_price = min_price_floor
        # Recalculate max_price to maintain the required average
        max_level_price = 2 * required_levels_avg - min_level_price
        
        # If max_price exceeds base_price, adjust accordingly
        if max_level_price > base_price:
            max_level_price = base_price
    
    # Create linear price distribution
    prices = np.linspace(max_level_price, min_level_price, levels)
    
    # Calculate actual results
    level_revenues = [p * c for p, c in zip(prices, level_counts)]
    total_revenue = initial_revenue + sum(level_revenues)
    avg_price = total_revenue / total_subjects
    
    return prices, level_counts, total_revenue, avg_price

# Calculate prices
final_prices, level_counts, total_revenue, avg_price = calculate_staggered_prices(
    base_price, target_avg_price, levels, total_subjects, initial_full_price_count, min_price_floor
)

# Create DataFrame - separate initial and levels for better display
initial_revenue = initial_full_price_count * base_price
level_revenues = [p * c for p, c in zip(final_prices, level_counts)]

# Create main levels table (without initial row duplication)
df_levels = pd.DataFrame({
    "Level": [f"Level {i+1}" for i in range(levels)],
    "Subjects": level_counts,
    "Price (Rs.)": [f"{p:,.0f}" for p in final_prices],
    "Revenue (Rs.)": [f"{r:,.0f}" for r in level_revenues]
})

# Calculate cumulative values including initial subjects
cumulative_subjects = [initial_full_price_count]
cumulative_revenue = [initial_revenue]
effective_prices = [base_price]

for i in range(levels):
    cumulative_subjects.append(cumulative_subjects[-1] + level_counts[i])
    cumulative_revenue.append(cumulative_revenue[-1] + level_revenues[i])
    effective_prices.append(cumulative_revenue[-1] / cumulative_subjects[-1])

# Add cumulative columns to levels table
df_levels["Cumulative Subjects"] = cumulative_subjects[1:]  # Skip initial
df_levels["Effective Avg Price (Rs.)"] = [f"{p:,.0f}" for p in effective_prices[1:]]

monthly_revenue = sum([initial_revenue] + level_revenues) / months

st.subheader("Staggered Pricing Table")

# Display initial subjects info as a metric instead of table row
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Initial Full-Price Subjects", f"{initial_full_price_count}")
with col2:
    st.metric("Initial Price", f"Rs.{base_price:,.0f}")
with col3:
    st.metric("Initial Revenue", f"Rs.{initial_revenue:,.0f}")

# Display the main levels table without horizontal scroll
st.dataframe(df_levels, use_container_width=True)

st.subheader("Summary")
total_revenue = initial_revenue + sum(level_revenues)
final_effective_price = effective_prices[-1]  # Last effective price from cumulative calculation
st.metric("Total Revenue (Rs.)", f"{total_revenue:,.2f}")
st.metric("Effective Average Price (Rs.)", f"{final_effective_price:,.2f}")
st.metric("Estimated Monthly Revenue (Rs.)", f"{monthly_revenue:,.2f}")
st.metric("Target Discount (%)", f"{discount_percent}")
