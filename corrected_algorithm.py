"""
Corrected Algorithm for Staggered Pricing Calculation

This script demonstrates the corrected algorithm that properly calculates
staggered pricing levels to achieve any target discount percentage, not just 50%.

The key insight is that we need to work backwards from the target average price
to determine what the level prices should be, accounting for initial full-price subjects.
"""

import numpy as np

def calculate_corrected_staggered_prices(base_price, discount_percent, levels, total_subjects, initial_full_price_count, min_price_floor=0):
    """
    Calculate staggered prices that achieve the exact target discount percentage.
    
    Algorithm Steps:
    1. Calculate target average price from discount percentage
    2. Calculate required revenue from levels (excluding initial full-price subjects)
    3. Create a price distribution that averages to the required level average
    4. Apply minimum price floor constraint if needed
    5. Verify the final average matches the target
    
    Args:
        base_price: Base price per subject
        discount_percent: Target discount percentage (0-100)
        levels: Number of pricing levels
        total_subjects: Total number of subjects
        initial_full_price_count: Number of subjects paying full price
        min_price_floor: Minimum price floor (optional)
    
    Returns:
        dict: Contains prices, level_counts, total_revenue, actual_avg_price
    """
    
    # Step 1: Calculate target average price
    target_avg_price = base_price * (1 - discount_percent / 100)
    
    # Step 2: Calculate level distribution
    remaining_subjects = total_subjects - initial_full_price_count
    level_size = remaining_subjects // levels
    last_level_size = remaining_subjects - level_size * (levels - 1)
    level_counts = [level_size] * (levels - 1) + [last_level_size]
    
    # Step 3: Calculate required revenue from levels
    initial_revenue = initial_full_price_count * base_price
    required_total_revenue = target_avg_price * total_subjects
    required_levels_revenue = required_total_revenue - initial_revenue
    required_levels_avg = required_levels_revenue / remaining_subjects if remaining_subjects > 0 else 0
    
    print(f"CORRECTED ALGORITHM CALCULATION:")
    print(f"Target average price: Rs.{target_avg_price:.2f}")
    print(f"Required levels average: Rs.{required_levels_avg:.2f}")
    
    # Step 4: Create price distribution that averages to required_levels_avg
    # We'll use a linear distribution from base_price down to a calculated minimum
    # such that the weighted average equals required_levels_avg
    
    # For a linear distribution from max_price to min_price:
    # average = (max_price + min_price) / 2
    # So: min_price = 2 * average - max_price
    
    max_level_price = base_price  # Start from base price
    min_level_price = 2 * required_levels_avg - max_level_price
    
    # Apply minimum price floor constraint
    if min_level_price < min_price_floor:
        print(f"Adjusting for minimum price floor: Rs.{min_price_floor}")
        min_level_price = min_price_floor
        # Recalculate max_price to maintain the required average
        max_level_price = 2 * required_levels_avg - min_level_price
        
        # If max_price exceeds base_price, we need a different approach
        if max_level_price > base_price:
            print("WARNING: Cannot achieve target discount with given price floor")
            max_level_price = base_price
            # Calculate what average we can actually achieve
            actual_levels_avg = (max_level_price + min_level_price) / 2
            actual_total_revenue = initial_revenue + actual_levels_avg * remaining_subjects
            actual_avg_price = actual_total_revenue / total_subjects
            actual_discount = ((base_price - actual_avg_price) / base_price) * 100
            print(f"Best achievable discount: {actual_discount:.1f}%")
    
    # Create linear price distribution
    prices = np.linspace(max_level_price, min_level_price, levels)
    
    # Step 5: Calculate actual results
    level_revenues = [p * c for p, c in zip(prices, level_counts)]
    total_revenue = initial_revenue + sum(level_revenues)
    actual_avg_price = total_revenue / total_subjects
    actual_discount = ((base_price - actual_avg_price) / base_price) * 100
    
    print(f"\nPRICE DISTRIBUTION:")
    for i, (price, count) in enumerate(zip(prices, level_counts)):
        print(f"   Level {i+1}: Rs.{price:.2f} x {count} subjects = Rs.{price * count:,.2f}")
    
    print(f"\nRESULTS:")
    print(f"   Target average price: Rs.{target_avg_price:.2f}")
    print(f"   Actual average price: Rs.{actual_avg_price:.2f}")
    print(f"   Target discount: {discount_percent}%")
    print(f"   Actual discount: {actual_discount:.1f}%")
    print(f"   Difference: Rs.{abs(actual_avg_price - target_avg_price):.2f}")
    
    return {
        'prices': prices,
        'level_counts': level_counts,
        'total_revenue': total_revenue,
        'actual_avg_price': actual_avg_price,
        'actual_discount': actual_discount,
        'target_avg_price': target_avg_price,
        'target_discount': discount_percent
    }

def test_algorithm():
    """Test the corrected algorithm with different discount percentages."""
    
    # Test parameters from the screenshot
    base_price = 2000
    levels = 5
    total_subjects = 700
    initial_full_price_count = 40
    min_price_floor = 750
    
    print("TESTING CORRECTED ALGORITHM")
    print("=" * 60)
    
    # Test different discount percentages
    test_discounts = [30, 40, 50, 60, 70]
    
    for discount in test_discounts:
        print(f"\n{'='*20} TESTING {discount}% DISCOUNT {'='*20}")
        result = calculate_corrected_staggered_prices(
            base_price, discount, levels, total_subjects, 
            initial_full_price_count, min_price_floor
        )
        
        success = abs(result['actual_discount'] - discount) < 0.1
        status = "SUCCESS" if success else "FAILED"
        print(f"Status: {status}")

if __name__ == "__main__":
    test_algorithm()