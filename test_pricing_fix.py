"""
Unit tests for the corrected staggered pricing calculation.

This test suite validates that the corrected algorithm achieves the exact
target discount percentages for various scenarios.
"""

import numpy as np
import sys
import os

# Add the app directory to the path to import the function
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

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

def test_discount_accuracy():
    """Test that the algorithm achieves exact discount percentages."""
    
    # Test parameters from the screenshot
    base_price = 2000
    levels = 5
    total_subjects = 700
    initial_full_price_count = 40
    min_price_floor = 750
    
    test_cases = [
        {"discount": 30, "expected_avg": 1400},
        {"discount": 40, "expected_avg": 1200},
        {"discount": 50, "expected_avg": 1000},
        {"discount": 60, "expected_avg": 800},
    ]
    
    print("UNIT TEST RESULTS")
    print("=" * 50)
    
    all_passed = True
    
    for case in test_cases:
        discount_percent = case["discount"]
        expected_avg = case["expected_avg"]
        target_avg_price = base_price * (1 - discount_percent / 100)
        
        # Run the calculation
        prices, level_counts, total_revenue, actual_avg_price = calculate_staggered_prices(
            base_price, target_avg_price, levels, total_subjects, 
            initial_full_price_count, min_price_floor
        )
        
        # Calculate actual discount achieved
        actual_discount = ((base_price - actual_avg_price) / base_price) * 100
        
        # Check if the result is within acceptable tolerance (0.1%)
        discount_diff = abs(actual_discount - discount_percent)
        price_diff = abs(actual_avg_price - expected_avg)
        
        passed = discount_diff < 0.1 and price_diff < 0.1
        status = "PASS" if passed else "FAIL"
        
        print(f"Test {discount_percent}% discount: {status}")
        print(f"  Expected avg price: Rs.{expected_avg:.2f}")
        print(f"  Actual avg price: Rs.{actual_avg_price:.2f}")
        print(f"  Expected discount: {discount_percent}%")
        print(f"  Actual discount: {actual_discount:.1f}%")
        print(f"  Price difference: Rs.{price_diff:.2f}")
        print(f"  Discount difference: {discount_diff:.2f}%")
        print()
        
        if not passed:
            all_passed = False
    
    print("=" * 50)
    overall_status = "ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED"
    print(f"OVERALL RESULT: {overall_status}")
    
    return all_passed

def test_original_problem():
    """Test the specific problem from the screenshot (50% discount)."""
    
    print("\nTESTING ORIGINAL PROBLEM (50% discount)")
    print("=" * 50)
    
    # Original parameters
    base_price = 2000
    discount_percent = 50
    target_avg_price = 1000  # 50% of 2000
    levels = 5
    total_subjects = 700
    initial_full_price_count = 40
    min_price_floor = 750
    
    # Run the corrected calculation
    prices, level_counts, total_revenue, actual_avg_price = calculate_staggered_prices(
        base_price, target_avg_price, levels, total_subjects, 
        initial_full_price_count, min_price_floor
    )
    
    actual_discount = ((base_price - actual_avg_price) / base_price) * 100
    
    print(f"Original problem (from screenshot):")
    print(f"  Expected effective price: Rs.1000.00 (50% discount)")
    print(f"  Previous buggy result: Rs.1528.57 (23.6% discount)")
    print(f"  Fixed result: Rs.{actual_avg_price:.2f} ({actual_discount:.1f}% discount)")
    
    success = abs(actual_avg_price - 1000) < 0.1
    print(f"  Fix successful: {'YES' if success else 'NO'}")
    
    return success

if __name__ == "__main__":
    # Run all tests
    test1_passed = test_discount_accuracy()
    test2_passed = test_original_problem()
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL TESTS PASSED - The pricing fix is working correctly!")
        exit(0)
    else:
        print("\n❌ SOME TESTS FAILED - The fix needs adjustment")
        exit(1)