# BMW historical resale data
# Source: Kelley Blue Book (KBB)
# Data accessed October 2026
#
# M4: 2023 BMW M4 Competition xDrive Coupe 2D
# M5: 2022 BMW M5 Sedan 4D
#
# These are historical resale values, not original MSRP.
# Actual vehicle value varies by mileage, condition, location, and options.

bmw_history = {

    "BMW M4 Competition xDrive": [
        {"year": 2023, "price": 84266},
        {"year": 2024, "price": 70704},
        {"year": 2025, "price": 71781},
        {"year": 2026, "price": 69700},
    ],

    "BMW M5 Competition xDrive": [
        # KBB publishes this historical series as BMW M5 Sedan.
        # Used here as an M5 market-value reference.
        {"year": 2023, "price": 90590},
        {"year": 2024, "price": 79399},
        {"year": 2025, "price": 75233},
        {"year": 2026, "price": 63000},
    ]
}
