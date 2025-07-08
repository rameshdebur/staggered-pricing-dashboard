"""
Test the corrected staggered pricing algorithm with odd/decimal discount values.

This test validates that the algorithm works correctly for non-integer discount
percentages like 32.5%, 47.3%, etc.
"""

import numpy as np

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

def test_odd_discount_values():
    """Test the algorithm with odd/decimal discount percentages."""
    
    # Test parameters
    base_price = 2000
    levels = 5
    total_subjects = 700
    initial_full_price_count = 40
    min_price_floor = 750
    
    # Test cases with odd/decimal discount values
    test_cases = [
        32.5,   # 32.5% discount
        47.3,   # 47.3% discount
        55.7,   # 55.7% discount
        23.8,   # 23.8% discount
        61.2,   # 61.2% discount
        15.5,   # 15.5% discount
        72.9    # 72.9% discount
    ]
    
    print("TESTING ODD/DECIMAL DISCOUNT VALUES")
    print("=" * 60)
    
    all_passed = True
    
    for discount_percent in test_cases:
        # Calculate expected values
        expected_avg_price = base_price * (1 - discount_percent / 100)
        target_avg_price = expected_avg_price
        
        # Run the calculation
        prices, level_counts, total_revenue, actual_avg_price = calculate_staggered_prices(
            base_price, target_avg_price, levels, total_subjects, 
            initial_full_price_count, min_price_floor
        )
        
        # Calculate actual discount achieved
        actual_discount = ((base_price - actual_avg_price) / base_price) * 100
        
        # Check accuracy (tolerance of 0.01% for decimal precision)
        discount_diff = abs(actual_discount - discount_percent)
        price_diff = abs(actual_avg_price - expected_avg_price)
        
        passed = discount_diff < 0.01 and price_diff < 0.01
        status = "PASS" if passed else "FAIL"
        
        print(f"Test {discount_percent}% discount: {status}")
        print(f"  Expected avg price: Rs.{expected_avg_price:.2f}")
        print(f"  Actual avg price: Rs.{actual_avg_price:.2f}")
        print(f"  Expected discount: {discount_percent}%")
        print(f"  Actual discount: {actual_discount:.3f}%")
        print(f"  Price difference: Rs.{price_diff:.4f}")
        print(f"  Discount difference: {discount_diff:.4f}%")
        
        # Show the price distribution for verification
        print(f"  Price levels: {[f'Rs.{p:.2f}' for p in prices]}")
        print()
        
        if not passed:
            all_passed = False
    
    print("=" * 60)
    overall_status = "ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED"
    print(f"OVERALL RESULT: {overall_status}")
    
    return all_passed

def test_specific_32_5_percent():
    """Test the specific case mentioned: 32.5% discount."""
    
    print("\nSPECIFIC TEST: 32.5% DISCOUNT")
    print("=" * 40)
    
    # Parameters
    base_price = 2000
    discount_percent = 32.5
    expected_avg_price = base_price * (1 - discount_percent / 100)  # Rs.1350
    levels = 5
    total_subjects = 700
    initial_full_price_count = 40
    min_price_floor = 750
    
    # Run calculation
    prices, level_counts, total_revenue, actual_avg_price = calculate_staggered_prices(
        base_price, expected_avg_price, levels, total_subjects, 
        initial_full_price_count, min_price_floor
    )
    
    actual_discount = ((base_price - actual_avg_price) / base_price) * 100
    
    print(f"Target: 32.5% discount (Rs.{expected_avg_price:.2f} average)")
    print(f"Result: {actual_discount:.3f}% discount (Rs.{actual_avg_price:.2f} average)")
    print(f"Accuracy: {abs(actual_discount - 32.5):.4f}% difference")
    
    # Show detailed breakdown
    print(f"\nPrice Distribution:")
    for i, (price, count) in enumerate(zip(prices, level_counts)):
        print(f"  Level {i+1}: Rs.{price:.2f} x {count} subjects = Rs.{price * count:,.2f}")
    
    initial_revenue = initial_full_price_count * base_price
    print(f"\nRevenue Breakdown:")
    print(f"  Initial full-price: Rs.{initial_revenue:,.2f}")
    print(f"  Levels total: Rs.{total_revenue - initial_revenue:,.2f}")
    print(f"  Grand total: Rs.{total_revenue:,.2f}")
    
    success = abs(actual_discount - 32.5) < 0.01
    print(f"\nResult: {'SUCCESS' if success else 'FAILED'}")
    
    return success

if __name__ == "__main__":
    # Run tests
    test1_passed = test_odd_discount_values()
    test2_passed = test_specific_32_5_percent()
    
    if test1_passed and test2_passed:
        print("\nALL TESTS PASSED - Algorithm works correctly for odd/decimal values!")
        exit(0)
    else:
        print("\nSOME TESTS FAILED - Algorithm needs adjustment for decimal values")
        exit(1)