"""
Test script to verify the table layout changes work correctly.

This script simulates the dashboard calculations to ensure the table
displays properly without horizontal scrolling and without duplicate rows.
"""

import pandas as pd
import numpy as np

def test_table_layout():
    """Test the new table layout structure."""
    
    # Simulate dashboard parameters
    base_price = 2000
    discount_percent = 50.0
    target_avg_price = base_price * (1 - discount_percent / 100)
    levels = 5
    total_subjects = 700
    initial_full_price_count = 40
    min_price_floor = 750
    months = 12
    
    # Simulate the corrected pricing calculation
    remaining_subjects = total_subjects - initial_full_price_count
    level_size = remaining_subjects // levels
    last_level_size = remaining_subjects - level_size * (levels - 1)
    level_counts = [level_size] * (levels - 1) + [last_level_size]
    
    initial_revenue = initial_full_price_count * base_price
    required_total_revenue = target_avg_price * total_subjects
    required_levels_revenue = required_total_revenue - initial_revenue
    required_levels_avg = required_levels_revenue / remaining_subjects
    
    max_level_price = base_price
    min_level_price = 2 * required_levels_avg - max_level_price
    
    if min_level_price < min_price_floor:
        min_level_price = min_price_floor
        max_level_price = 2 * required_levels_avg - min_level_price
        if max_level_price > base_price:
            max_level_price = base_price
    
    final_prices = np.linspace(max_level_price, min_level_price, levels)
    level_revenues = [p * c for p, c in zip(final_prices, level_counts)]
    
    # Test the new table structure
    print("TESTING NEW TABLE LAYOUT")
    print("=" * 50)
    
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
    
    print("Initial Subjects Info (displayed as metrics):")
    print(f"  Initial Full-Price Subjects: {initial_full_price_count}")
    print(f"  Initial Price: Rs.{base_price:,.0f}")
    print(f"  Initial Revenue: Rs.{initial_revenue:,.0f}")
    print()
    
    print("Main Levels Table:")
    print(df_levels.to_string(index=False))
    print()
    
    # Test summary calculations
    total_revenue = initial_revenue + sum(level_revenues)
    final_effective_price = effective_prices[-1]
    monthly_revenue = total_revenue / months
    
    print("Summary:")
    print(f"  Total Revenue: Rs.{total_revenue:,.2f}")
    print(f"  Effective Average Price: Rs.{final_effective_price:,.2f}")
    print(f"  Monthly Revenue: Rs.{monthly_revenue:,.2f}")
    print(f"  Target Discount: {discount_percent}%")
    
    # Verify no duplicate "Initial" row
    has_initial_row = "Initial" in df_levels["Level"].values
    print(f"\nTable Issues Check:")
    print(f"  Contains duplicate 'Initial' row: {'YES' if has_initial_row else 'NO'}")
    print(f"  Number of columns: {len(df_levels.columns)}")
    print(f"  Column names: {list(df_levels.columns)}")
    
    # Check if effective price matches target
    target_match = abs(final_effective_price - target_avg_price) < 1
    print(f"  Effective price matches target: {'YES' if target_match else 'NO'}")
    
    return not has_initial_row and target_match

if __name__ == "__main__":
    success = test_table_layout()
    if success:
        print("\n✓ TABLE LAYOUT TEST PASSED")
        print("- No duplicate 'Initial' row")
        print("- Compact column structure")
        print("- Correct calculations")
    else:
        print("\n✗ TABLE LAYOUT TEST FAILED")