# Energy Consumption Database

This project processes energy consumption data for different regions, storing both commercial and residential usage data in a SQLite database.

## Overview

The system processes two CSV files containing energy consumption data:
- `q2-IC.csv`: Industrial and Commercial energy consumption
- `q2-domestic.csv`: Domestic energy consumption

The data is organized by location and includes different types of energy consumption:
- Electricity
- Gas
- Coal
- Oil
- Bioenergy and waste

## Database Structure

### Tables
1. `location_data`
   - `city_id` (PRIMARY KEY)
   - `city_name`

2. `sector_data`
   - `sector_id` (PRIMARY KEY)
   - `sector_name`

3. `fuel_types`
   - `fuel_id` (PRIMARY KEY)
   - `fuel_name`

4. `commercial_usage`
   - `usage_id` (PRIMARY KEY)
   - `city_ref` (FOREIGN KEY)
   - `sector_ref` (FOREIGN KEY)
   - `fuel_ref` (FOREIGN KEY)
   - `usage_amount`

5. `residential_usage`
   - `usage_id` (PRIMARY KEY)
   - `city_ref` (FOREIGN KEY)
   - `sector_ref` (FOREIGN KEY)
   - `fuel_ref` (FOREIGN KEY)
   - `usage_amount`

## Requirements

- Python 3.6+
- pandas
- openpyxl>=3.1.0
- sqlite3
- pathlib

## Installation

1. Clone the repository
2. Install required packages
pip install -r requirements.txt


## Usage

1. Ensure your CSV files are in the same directory as the script:
   - `q2-IC.csv`
   - `q2-domestic.csv`

2. Run the script:
python main.py

## File Structure
project/
│
├── main.py # Main script
├── requirements.txt # Project dependencies
├── README.md # Project documentation
├── q2-IC.csv # Commercial energy data
└── q2-domestic.csv # Residential energy data

