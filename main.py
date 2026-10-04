
# FUTURE COST PREDICTOR
# Housing + Cars

from housing_data import get_state_growth_rate
import matplotlib.pyplot as plt
from datetime import datetime
from car_data import bmw_history

def predict_future_price(current_price, growth_rate, years):
    return current_price * ((1 + growth_rate) ** years)

def calculate_historical_depreciation(car):
    history = bmw_history.get(car, [])

    if len(history) < 2:
        return None

    first_price = history[0]["price"]
    last_price = history[-1]["price"]
    years = history[-1]["year"] - history[0]["year"]

    if years <= 0:
        return None

    annual_rate = 1 - (last_price / first_price) ** (1 / years)

    return annual_rate


car_data = {
    "1": {
        "name": "BMW M4 Competition xDrive",
        "depreciation": 0.08
    },
    "2": {
        "name": "BMW M5 Competition xDrive",
        "depreciation": 0.10
    }
}


# HOUSING PREDICTOR

def housing_predictor():
    print("\n--- Housing Price Predictor ---")

    states = {
        "AL": "Alabama",
        "AK": "Alaska",
        "AZ": "Arizona",
        "AR": "Arkansas",
        "CA": "California",
        "CO": "Colorado",
        "CT": "Connecticut",
        "DE": "Delaware",
        "FL": "Florida",
        "GA": "Georgia",
        "HI": "Hawaii",
        "ID": "Idaho",
        "IL": "Illinois",
        "IN": "Indiana",
        "IA": "Iowa",
        "KS": "Kansas",
        "KY": "Kentucky",
        "LA": "Louisiana",
        "ME": "Maine",
        "MD": "Maryland",
        "MA": "Massachusetts",
        "MI": "Michigan",
        "MN": "Minnesota",
        "MS": "Mississippi",
        "MO": "Missouri",
        "MT": "Montana",
        "NE": "Nebraska",
        "NV": "Nevada",
        "NH": "New Hampshire",
        "NJ": "New Jersey",
        "NM": "New Mexico",
        "NY": "New York",
        "NC": "North Carolina",
        "ND": "North Dakota",
        "OH": "Ohio",
        "OK": "Oklahoma",
        "OR": "Oregon",
        "PA": "Pennsylvania",
        "RI": "Rhode Island",
        "SC": "South Carolina",
        "SD": "South Dakota",
        "TN": "Tennessee",
        "TX": "Texas",
        "UT": "Utah",
        "VT": "Vermont",
        "VA": "Virginia",
        "WA": "Washington",
        "WV": "West Virginia",
        "WI": "Wisconsin",
        "WY": "Wyoming"
    }

    print("\nAvailable states:")
    print(", ".join(states.keys()))

    state = input("\nEnter state abbreviation: ").upper()

    if state not in states:
        print("Invalid state.")
        return

    current_price = float(input("Enter current home price: $"))
    years = int(input("How many years into the future? "))

    # Get historical growth rate from FHFA data
    growth_rate = get_state_growth_rate(state)

    if growth_rate is None:
        print("Could not calculate a growth rate for this state.")
        return

    future_price = current_price * ((1 + growth_rate) ** years)

    low = future_price * 0.90
    high = future_price * 1.10

    print("\n--- Prediction ---")
    print(f"State: {states[state]} ({state})")
    print(f"Current price: ${current_price:,.2f}")
    print(f"Growth assumption: {growth_rate * 100:.1f}%")
    print(f"Years: {years}")
    print(f"Predicted price: ${future_price:,.2f}")
    print(f"Estimated range: ${low:,.2f} - ${high:,.2f}")



# CAR PREDICTOR


def car_predictor():
    print("\n--- Car Price Predictor ---")


    print("\nChoose a car:")
    print("1. BMW M4 Competition xDrive")
    print("2. BMW M5 Competition xDrive")

    choice = input("Choose an option: ")

    if choice not in car_data:
        print("Invalid choice.")
        return

    car = car_data[choice]["name"]

    current_price = float(input("Enter current car price: $"))
    mileage = int(input("Enter current mileage: "))
    car_year = int(input("Enter car model year: "))
    years = int(input("Enter years into the future: "))

    current_year = datetime.now().year
    car_age = current_year - car_year
    depreciation_rate = car_data[choice]["depreciation"]

    historical_rate = calculate_historical_depreciation(car)

    if historical_rate is not None:
        depreciation_rate = historical_rate

    # Adjust depreciation based on car age
    age_adjustment = max(0, car_age - 3) * 0.005


    # Estimate future mileage
    annual_miles = 12000
    future_mileage = mileage + (annual_miles * years)

    # Adjust depreciation based on current mileage
    normal_mileage = 12000
    extra_miles = max(0, mileage - normal_mileage)

    # 1% additional depreciation for every 10,000 extra miles
    mileage_adjustment = (extra_miles / 10000) * 0.01
        # Calculate future value
    adjusted_depreciation = depreciation_rate + mileage_adjustment + age_adjustment

    future_price = current_price * ((1 - adjusted_depreciation) ** years)

    
    print("\n--- Future Car Price Prediction ---")
    print(f"Car: {car}")
    print(f"Current price: ${current_price:,.2f}")
    print(f"Base depreciation: {depreciation_rate * 100:.1f}% per year")
    print(f"Mileage adjustment: {mileage_adjustment * 100:.2f}%")
    print(f"Adjusted depreciation: {adjusted_depreciation * 100:.2f}% per year")
    print(f"Estimated value after {years} years: ${future_price:,.2f}")
    print(f"Current mileage: {mileage:,} miles")
    print(f"Car model year: {car_year}")
    print(f"Current car age: {car_age} years")
    print(f"Estimated mileage after {years} years: {future_mileage:,} miles")
    


def car_forecast(
    current_price,
    depreciation_rate,
    years,
    car,
    mileage_adjustment,
    car_age
):
    print(f"\n--- {car} Forecast ---")
    print(f"{'Year':<10}{'Estimated Value':>20}")

    years_list = list(range(0, years + 1))
    prices = []

    for year in years_list:
        future_age = car_age + year

        age_adjustment = max(0, future_age - 3) * 0.005

        adjusted_rate = (
            depreciation_rate
            + mileage_adjustment
            + age_adjustment
        )

        future_price = current_price * ((1 - adjusted_rate) ** year)

        prices.append(future_price)

        if year > 0:
            print(f"{year:<10}${future_price:>19,.2f}")
    # Graph
    plt.figure(figsize=(10, 6))

    plt.plot(
        years_list,
        prices,
        marker="o",
        label=car
    )

    plt.title(f"{car} Future Value Forecast")
    plt.xlabel("Years Into the Future")
    plt.ylabel("Estimated Car Value ($)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    #plt.close()


def car_scenario_forecast(
    current_price,
    base_rate,
    years,
    car,
    mileage=0,
    car_year=None
):
    current_year = datetime.now().year

    if car_year is None:
        car_age = 0
    else:
        car_age = current_year - car_year

    low_rate = max(0, base_rate - 0.02)
    high_rate = base_rate + 0.02

    annual_miles = 12000

    low_value = current_price
    base_value = current_price
    high_value = current_price

    for year in range(1, years + 1):

        future_mileage = mileage + (annual_miles * year)
        future_age = car_age + year

        # Age adjustment
        age_adjustment = max(0, future_age - 3) * 0.005

        # Mileage adjustment
        extra_miles = max(0, future_mileage - 12000)
        mileage_adjustment = (extra_miles / 10000) * 0.01

        # Cap mileage adjustment at 5%
        mileage_adjustment = min(mileage_adjustment, 0.05)

        low_adjusted_rate = (
            low_rate
            + age_adjustment
            + mileage_adjustment
        )

        base_adjusted_rate = (
            base_rate
            + age_adjustment
            + mileage_adjustment
        )

        high_adjusted_rate = (
            high_rate
            + age_adjustment
            + mileage_adjustment
        )

        low_value *= (1 - low_adjusted_rate)
        base_value *= (1 - base_adjusted_rate)
        high_value *= (1 - high_adjusted_rate)

    print(f"\n--- {car} Confidence Range ---")
    print(f"Best case:       ${low_value:,.2f}")
    print(f"Expected value:  ${base_value:,.2f}")
    print(f"Worst case:      ${high_value:,.2f}")

    print(
        f"Estimated range: "
        f"${high_value:,.2f} - ${low_value:,.2f}"
    )


def compare_cars(m4_price, m5_price, years, mileage, car_year):
    m4_rate = calculate_historical_depreciation(
        "BMW M4 Competition xDrive"
    )

    m5_rate = calculate_historical_depreciation(
        "BMW M5 Competition xDrive"
    )

    current_year = datetime.now().year
    car_age = current_year - car_year

    annual_miles = 12000
    years_list = list(range(current_year, current_year + years + 1))

    m4_prices = []
    m5_prices = []
    mileage_list = []

    for year_index, calendar_year in enumerate(years_list):

        # Future mileage
        future_mileage = mileage + (annual_miles * year_index)
        mileage_list.append(future_mileage)

        # Age adjustment
        future_age = car_age + year_index
        age_adjustment = max(0, future_age - 3) * 0.005

        # Mileage adjustment
        if future_mileage <= 12000:
            mileage_adjustment = 0

        else:
            extra_miles = future_mileage - 12000
            mileage_adjustment = (extra_miles / 10000) * 0.01

            # Cap mileage adjustment at 5%
            mileage_adjustment = min(mileage_adjustment, 0.05)

        # Adjusted depreciation
        m4_adjusted_rate = (
            m4_rate
            + age_adjustment
            + mileage_adjustment
        )

        m5_adjusted_rate = (
            m5_rate
            + age_adjustment
            + mileage_adjustment
        )

        # Future prices
        m4_future_price = (
            m4_price * ((1 - m4_adjusted_rate) ** year_index)
        )

        m5_future_price = (
            m5_price * ((1 - m5_adjusted_rate) ** year_index)
        )

        # Store prices
        m4_prices.append(m4_future_price)
        m5_prices.append(m5_future_price)


    print("\n--- BMW M4 vs. M5 Forecast ---")
    print(
        f"{'Year':<8}"
        f"{'M4 Value':>15}"
        f"{'M5 Value':>15}"
        f"{'Mileage':>15}"
    )

    for i, calendar_year in enumerate(years_list):
        print(
            f"{calendar_year:<8}"
            f"${m4_prices[i]:>14,.2f}"
            f"${m5_prices[i]:>14,.2f}"
            f"{mileage_list[i]:>15,}"
        )

    plt.figure(figsize=(10, 6))

    plt.plot(
        years_list,
        m4_prices,
        marker="o",
        label="BMW M4 Competition xDrive"
    )

    plt.plot(
        years_list,
        m5_prices,
        marker="o",
        label="BMW M5 Competition xDrive"
    )

    plt.title("BMW M4 vs. M5 Future Value Forecast")
    plt.xlabel("Years Into the Future")
    plt.ylabel("Estimated Car Value ($)")

    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    #plt.close()


def compare_scenarios(m4_price, m5_price, years, mileage, car_year):

    m4_rate = calculate_historical_depreciation(
        "BMW M4 Competition xDrive"
    )

    m5_rate = calculate_historical_depreciation(
        "BMW M5 Competition xDrive"
    )

    # Scenario rates
    m4_low = max(0, m4_rate - 0.02)
    m4_high = m4_rate + 0.02

    m5_low = max(0, m5_rate - 0.02)
    m5_high = m5_rate + 0.02

    current_year = datetime.now().year
    car_age = current_year - car_year
    annual_miles = 12000

    years_list = list(range(0, years + 1))

    m4_low_prices = []
    m4_base_prices = []
    m4_high_prices = []

    m5_low_prices = []
    m5_base_prices = []
    m5_high_prices = []

    for year in years_list:

        # Future mileage
        future_mileage = mileage + (annual_miles * year)

        # Future age
        future_age = car_age + year

        # Age adjustment
        age_adjustment = max(0, future_age - 3) * 0.005

        # Mileage adjustment
        if future_mileage <= 12000:
            mileage_adjustment = 0
        elif future_mileage <= 20000:
            mileage_adjustment = 0.01
        elif future_mileage <= 30000:
            mileage_adjustment = 0.02
        else:
            mileage_adjustment = 0.03

        # M4 rates
        m4_low_adjusted = (
            m4_low
            + age_adjustment
            + mileage_adjustment
        )

        m4_base_adjusted = (
            m4_rate
            + age_adjustment
            + mileage_adjustment
        )

        m4_high_adjusted = (
            m4_high
            + age_adjustment
            + mileage_adjustment
        )

        # M5 rates
        m5_low_adjusted = (
            m5_low
            + age_adjustment
            + mileage_adjustment
        )

        m5_base_adjusted = (
            m5_rate
            + age_adjustment
            + mileage_adjustment
        )

        m5_high_adjusted = (
            m5_high
            + age_adjustment
            + mileage_adjustment
        )

        # Future values
        m4_low_prices.append(
            m4_price * ((1 - m4_low_adjusted) ** year)
        )

        m4_base_prices.append(
            m4_price * ((1 - m4_base_adjusted) ** year)
        )

        m4_high_prices.append(
            m4_price * ((1 - m4_high_adjusted) ** year)
        )

        m5_low_prices.append(
            m5_price * ((1 - m5_low_adjusted) ** year)
        )

        m5_base_prices.append(
            m5_price * ((1 - m5_base_adjusted) ** year)
        )

        m5_high_prices.append(
            m5_price * ((1 - m5_high_adjusted) ** year)
        )

    # Print scenario results
    print("\n=== BMW M4 Scenario Forecast ===")

    print(
        f"Low depreciation:  "
        f"${m4_low_prices[-1]:,.2f}"
    )

    print(
        f"Expected value:    "
        f"${m4_base_prices[-1]:,.2f}"
    )

    print(
        f"High depreciation: "
        f"${m4_high_prices[-1]:,.2f}"
    )

    print("\n=== BMW M5 Scenario Forecast ===")

    print(
        f"Low depreciation:  "
        f"${m5_low_prices[-1]:,.2f}"
    )

    print(
        f"Expected value:    "
        f"${m5_base_prices[-1]:,.2f}"
    )

    print(
        f"High depreciation: "
        f"${m5_high_prices[-1]:,.2f}"
    )

    # Scenario graph
    plt.figure(figsize=(10, 6))

    plt.plot(
        years_list,
        m4_low_prices,
        marker="o",
        label="M4 Low Depreciation"
    )

    plt.plot(
        years_list,
        m4_base_prices,
        marker="o",
        label="M4 Expected"
    )

    plt.plot(
        years_list,
        m4_high_prices,
        marker="o",
        label="M4 High Depreciation"
    )

    plt.plot(
        years_list,
        m5_low_prices,
        marker="o",
        label="M5 Low Depreciation"
    )

    plt.plot(
        years_list,
        m5_base_prices,
        marker="o",
        label="M5 Expected"
    )

    plt.plot(
        years_list,
        m5_high_prices,
        marker="o",
        label="M5 High Depreciation"
    )

    plt.title("BMW M4 vs. M5 Scenario Forecast")
    plt.xlabel("Years Into the Future")
    plt.ylabel("Estimated Car Value ($)")

    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    #plt.close()


def car_scenario_forecast(
    current_price,
    base_rate,
    years,
    car,
    mileage=0,
    car_year=None
):
    current_year = datetime.now().year

    if car_year is None:
        car_age = 0
    else:
        car_age = current_year - car_year

    low_rate = max(0, base_rate - 0.02)
    high_rate = base_rate + 0.02

    annual_miles = 12000

    low_value = current_price
    base_value = current_price
    high_value = current_price

    for year in range(1, years + 1):

        future_mileage = mileage + (annual_miles * year)
        future_age = car_age + year

        # Age adjustment
        age_adjustment = max(0, future_age - 3) * 0.005

        # Mileage adjustment
        extra_miles = max(0, future_mileage - 12000)
        mileage_adjustment = (extra_miles / 10000) * 0.01

        # Cap mileage adjustment at 5%
        mileage_adjustment = min(mileage_adjustment, 0.05)

        low_adjusted_rate = (
            low_rate
            + age_adjustment
            + mileage_adjustment
        )

        base_adjusted_rate = (
            base_rate
            + age_adjustment
            + mileage_adjustment
        )

        high_adjusted_rate = (
            high_rate
            + age_adjustment
            + mileage_adjustment
        )

        low_value *= (1 - low_adjusted_rate)
        base_value *= (1 - base_adjusted_rate)
        high_value *= (1 - high_adjusted_rate)

    print(f"\n--- {car} Scenario Forecast ---")
    print(f"Low depreciation:  ${low_value:,.2f}")
    print(f"Expected value:    ${base_value:,.2f}")
    print(f"High depreciation: ${high_value:,.2f}")


def forecast_summary(state1, state2, price1, price2, years):
    print("\n==============================")
    print("       FORECAST SUMMARY")
    print("==============================")

    print(f"\nHousing Forecast ({years} years)")
    print(f"{state1}: ${price1:,.2f}")
    print(f"{state2}: ${price2:,.2f}")

    if price1 > price2:
        print(f"Best projected value: {state1}")
    elif price2 > price1:
        print(f"Best projected value: {state2}")
    else:
        print("Both states have the same projected value.")

    difference = abs(price1 - price2)
    print(f"Difference: ${difference:,.2f}")

    print("\n==============================")


# MAIN MENU

def main():

    while True:

        print("\n================================")
        print("       FUTURE COST PREDICTOR")
        print("================================")

        print("1. Housing Price Predictor")
        print("2. Car Price Predictor")
        print("3. Compare States")
        print("4. Compare BMW M4 vs. M5")
        print("5. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            housing_predictor()

        elif choice == "2":
            car_predictor()

        elif choice == "3":
            compare_states()

        elif choice == "4":
            m4_price = float(
                input("\nEnter current BMW M4 price: $")
            )

            m5_price = float(
                input("Enter current BMW M5 price: $")
            )

            mileage = int(
                input("Enter current mileage: ")
            )

            car_year = int(
                input("Enter car model year: ")
            )

            years = int(
                input("Enter years into the future: ")
            )

            compare_cars(
                m4_price,
                m5_price,
                years,
                mileage,
                car_year
            )

            compare_scenarios(
    m4_price,
    m5_price,
    years,
    mileage,
    car_year
)

        elif choice == "5":
            print("\nGoodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

# HOUSING COMPARISON

def show_forecast(current_price, growth_rate, years, state):
    print(f"\n--- {state} Housing Forecast ---")
    print(f"{'Year':<10}{'Estimated Price':>20}")

    price = current_price

    for year in range(1, years + 1):
        price = price * (1 + growth_rate)
        print(f"{year:<10}${price:>19,.2f}")

def compare_states():
    print("\n--- Compare States ---")

    state1 = input("Enter first state abbreviation: ").upper()
    state2 = input("Enter second state abbreviation: ").upper()

    growth1 = get_state_growth_rate(state1)
    growth2 = get_state_growth_rate(state2)

    if growth1 is None or growth2 is None:
        print("Could not calculate growth for one or both states.")
        return

    print("\n--- Historical Growth Comparison ---")
    print(f"{state1}: {growth1 * 100:.2f}% per year")
    print(f"{state2}: {growth2 * 100:.2f}% per year")

    current_price = float(
        input("\nEnter current home price: $")
    )

    years = int(
        input("Enter years into the future: ")
    )

    future1 = predict_future_price(
        current_price, growth1, years
    )

    future2 = predict_future_price(
        current_price, growth2, years
    )

    print("\n--- Future Price Prediction ---")
    print(f"{state1} after {years} years: ${future1:,.2f}")
    print(f"{state2} after {years} years: ${future2:,.2f}")

    show_forecast(current_price, growth1, years, state1)
    show_forecast(current_price, growth2, years, state2)

    scenario_forecast(current_price, growth1, years, state1)
    scenario_forecast(current_price, growth2, years, state2)

    plot_forecast(
        current_price,
        growth1,
        growth2,
        years,
        state1,
        state2
    )

    forecast_summary(
        state1,
        state2,
        future1,
        future2,
        years
    )

def scenario_forecast(current_price, growth_rate, years, state):
    conservative_rate = growth_rate - 0.01
    base_rate = growth_rate
    high_rate = growth_rate + 0.01

    conservative = predict_future_price(
        current_price, conservative_rate, years
    )

    base = predict_future_price(
        current_price, base_rate, years
    )

    high = predict_future_price(
        current_price, high_rate, years
    )

    print(f"\n--- {state} Scenario Forecast ---")
    print(f"Conservative: ${conservative:,.2f}")
    print(f"Base:         ${base:,.2f}")
    print(f"High:         ${high:,.2f}")


def plot_forecast(current_price, growth1, growth2, years, state1, state2):
    years_list = list(range(0, years + 1))

    prices1 = []
    prices2 = []

    for year in years_list:
        price1 = current_price * ((1 + growth1) ** year)
        price2 = current_price * ((1 + growth2) ** year)

        prices1.append(price1)
        prices2.append(price2)

    plt.figure(figsize=(10, 6))

    plt.plot(years_list, prices1, marker="o", label=state1)
    plt.plot(years_list, prices2, marker="o", label=state2)

    plt.title("Housing Price Forecast")
    plt.xlabel("Years Into the Future")
    plt.ylabel("Estimated Home Price ($)")

    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()
    #plt.close()

main()