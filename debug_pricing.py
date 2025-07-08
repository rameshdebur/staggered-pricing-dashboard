"""
Debug script to analyze the staggered pricing calculation issue.
This script reproduces the pricing logic and shows detailed diagnostics
to identify why the effective price doesn't match the 50% target discount.
"""

import numpy as np

def calculate_staggered_prices_debug(base_price, target_avg_price, levels, total_subjects, initial_full_price_count):
    """
    Calculate staggered prices with detailed debugging information.
    
    Args:
        base_price: Base price per subject
        target_avg_price: Target average price (base_price * (1 - discount/100))
        levels: Number of pricing levels
        total_subjects: Total number of subjects
        initial_full_price_count: Number of subjects paying full price
    
    Returns:
        Detailed analysis of the pricing calculation
    """
    print("DEBUGGING STAGGERED PRICING CALCULATION")
    print("=" * 50)
    
    # Calculate level sizes
    level_size = (total_subjects - initial_full_price_count) // levels
    last_level_size = (total_subjects - initial_full_price_count) - level_size * (levels - 1)
    level_counts = [level_size] * (levels - 1) + [last_level_size]
    
    print(f"INPUT PARAMETERS:")
    print(f"   Base Price: Rs.{base_price}")
    print(f"   Target Average Price: Rs.{target_avg_price}")
    print(f"   Target Discount: {((base_price - target_avg_price) / base_price) * 100:.1f}%")
    print(f"   Total Subjects: {total_subjects}")
    print(f"   Initial Full-Price Subjects: {initial_full_price_count}")
    print(f"   Number of Levels: {levels}")
    print()
    
    print(f"LEVEL DISTRIBUTION:")
    print(f"   Subjects to distribute across levels: {total_subjects - initial_full_price_count}")
    print(f"   Level sizes: {level_counts}")
    print()
    
    # Create linear price distribution (current logic)
    prices = np.linspace(base_price, target_avg_price, levels)
    
    print(f"PRICE DISTRIBUTION (Current Linear Logic):")
    for i, (price, count) in enumerate(zip(prices, level_counts)):
        print(f"   Level {i+1}: Rs.{price:.2f} x {count} subjects = Rs.{price * count:,.2f}")
    print()
    
    # Calculate revenues
    initial_revenue = initial_full_price_count * base_price
    level_revenues = [p * c for p, c in zip(prices, level_counts)]
    total_revenue = initial_revenue + sum(level_revenues)
    actual_avg_price = total_revenue / total_subjects
    
    print(f"REVENUE BREAKDOWN:")
    print(f"   Initial full-price revenue: Rs.{initial_revenue:,.2f} ({initial_full_price_count} x Rs.{base_price})")
    for i, revenue in enumerate(level_revenues):
        print(f"   Level {i+1} revenue: Rs.{revenue:,.2f}")
    print(f"   Total revenue: Rs.{total_revenue:,.2f}")
    print()
    
    print(f"RESULTS:")
    print(f"   Expected average price: Rs.{target_avg_price:.2f}")
    print(f"   Actual average price: Rs.{actual_avg_price:.2f}")
    print(f"   Difference: Rs.{actual_avg_price - target_avg_price:.2f}")
    print(f"   Actual discount achieved: {((base_price - actual_avg_price) / base_price) * 100:.1f}%")
    print()
    
    # Analyze the problem
    print(f"PROBLEM ANALYSIS:")
    
    # Calculate what happens without initial full-price subjects
    levels_only_revenue = sum(level_revenues)
    levels_only_subjects = sum(level_counts)
    levels_only_avg = levels_only_revenue / levels_only_subjects if levels_only_subjects > 0 else 0
    
    print(f"   Average price for levels only: Rs.{levels_only_avg:.2f}")
    print(f"   Impact of initial full-price subjects:")
    print(f"     - They pay Rs.{base_price} instead of discounted price")
    print(f"     - This pulls the overall average UP by Rs.{actual_avg_price - levels_only_avg:.2f}")
    
    # Calculate required adjustment
    required_total_revenue = target_avg_price * total_subjects
    required_levels_revenue = required_total_revenue - initial_revenue
    required_levels_avg = required_levels_revenue / levels_only_subjects if levels_only_subjects > 0 else 0
    
    print(f"   To achieve target average:")
    print(f"     - Required total revenue: Rs.{required_total_revenue:,.2f}")
    print(f"     - Required levels revenue: Rs.{required_levels_revenue:,.2f}")
    print(f"     - Required levels average: Rs.{required_levels_avg:.2f}")
    
    return {
        'actual_avg_price': actual_avg_price,
        'target_avg_price': target_avg_price,
        'required_levels_avg': required_levels_avg,
        'prices': prices,
        'level_counts': level_counts
    }

def main():
    """Run the debug analysis with the values from the screenshot."""
    # Values from the screenshot
    base_price = 2000
    discount_percent = 50
    target_avg_price = base_price * (1 - discount_percent / 100)  # Rs.1000
    levels = 5
    total_subjects = 700
    initial_full_price_count = 40
    
    result = calculate_staggered_prices_debug(
        base_price, target_avg_price, levels, total_subjects, initial_full_price_count
    )
    
    print("DIAGNOSIS:")
    print("   The main issue is that the linear price distribution from base_price to target_avg_price")
    print("   does NOT account for the weighted impact of initial full-price subjects.")
    print("   The algorithm needs to calculate prices that will result in the target average")
    print("   AFTER considering the full-price subjects.")

if __name__ == "__main__":
    main()