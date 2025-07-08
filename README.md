# Staggered Pricing Dashboard

A Streamlit web application that calculates and displays staggered pricing levels to achieve exact target discount percentages. This dashboard is designed for businesses that want to implement tiered pricing strategies while maintaining precise control over their average pricing and revenue targets.

## Features

- **Exact Target Discount Achievement**: Calculates pricing levels that achieve precise discount percentages
- **Initial Full-Price Subject Handling**: Properly accounts for subjects who pay full price initially
- **Minimum Price Floor Constraints**: Respects minimum pricing limits while optimizing the pricing structure
- **Interactive Dashboard**: Real-time calculations with adjustable parameters
- **Comprehensive Analytics**: Detailed revenue projections and effective pricing analysis
- **Clean Table Layout**: Optimized display without horizontal scrolling

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/staggered-pricing-dashboard.git
cd staggered-pricing-dashboard
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit application:
```bash
streamlit run app/staggered_pricing_dashboard.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Adjust the parameters in the sidebar:
   - **Base Price**: Starting price for your product/service
   - **Total Subjects**: Total number of customers/users
   - **Initial Full-Price Subjects**: Number of customers paying full price initially
   - **Target Discount**: Desired overall discount percentage
   - **Minimum Price Floor**: Lowest acceptable price
   - **Number of Levels**: How many pricing tiers to create
   - **Engagement Period**: Duration in months for revenue calculations

## Key Components

### Main Application
- `app/staggered_pricing_dashboard.py`: Main Streamlit dashboard application

### Testing Suite
- `test_pricing_fix.py`: Unit tests for the corrected pricing algorithm
- `test_odd_values.py`: Tests for decimal discount percentages
- `test_table_layout.py`: Tests for table display functionality

### Development Files
- `debug_pricing.py`: Debugging script for pricing calculations
- `corrected_algorithm.py`: Standalone implementation of the corrected algorithm

## Algorithm Overview

The dashboard uses a corrected pricing algorithm that:

1. **Accounts for Initial Full-Price Subjects**: Separates customers who pay full price from those in the staggered pricing levels
2. **Calculates Required Revenue**: Determines the revenue needed from staggered levels to achieve the target discount
3. **Optimizes Price Distribution**: Creates a linear price distribution across levels while respecting minimum price floors
4. **Validates Results**: Ensures the effective average price matches the target discount percentage

## Example Output

The dashboard displays:
- **Initial Subjects Metrics**: Full-price customer count, price, and revenue
- **Staggered Pricing Table**: Level-by-level breakdown with cumulative analysis
- **Summary Metrics**: Total revenue, effective average price, and monthly projections

## Technical Details

- **Framework**: Streamlit for web interface
- **Data Processing**: Pandas for table management
- **Calculations**: NumPy for numerical computations
- **Encoding**: Uses "Rs." instead of Unicode symbols for Windows compatibility

## Testing

Run the test suite to verify functionality:

```bash
python test_pricing_fix.py
python test_odd_values.py
python test_table_layout.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Created as part of a pricing optimization project to help businesses implement effective staggered pricing strategies.
