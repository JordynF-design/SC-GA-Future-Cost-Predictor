import pandas as pd


def get_state_growth_rate(state):
    # Load FHFA housing data
    data = pd.read_csv("hpi_master.csv", low_memory=False)

    # Find the selected state and quarterly data
    state_data = data[
        (data["place_id"].astype(str) == state) &
        (data["frequency"].astype(str).str.lower() == "quarterly")
    ].copy()

    if state_data.empty:
        print(f"No quarterly data found for {state}.")
        return None

    # Make sure the HPI values are numbers
    state_data["index_nsa"] = pd.to_numeric(
        state_data["index_nsa"],
        errors="coerce"
    )

    # Remove rows without a valid HPI value
    state_data = state_data.dropna(subset=["index_nsa"])

    # Calculate average HPI for each year
    yearly_hpi = (
        state_data
        .groupby("yr")["index_nsa"]
        .mean()
        .sort_index()
    )

    if len(yearly_hpi) < 2:
        print(f"Not enough historical data for {state}.")
        return None

    # Use the most recent 10 years of available data
    latest_year = yearly_hpi.index[-1]
    start_year = latest_year - 10

    recent_hpi = yearly_hpi[yearly_hpi.index >= start_year]

    if len(recent_hpi) < 2:
        print(f"Not enough recent data for {state}.")
        return None

    # Get HPI values from the recent period
    first_hpi = recent_hpi.iloc[0]
    latest_hpi = recent_hpi.iloc[-1]

    first_year = recent_hpi.index[0]
    latest_year = recent_hpi.index[-1]

    # Calculate annualized historical growth
    years = latest_year - first_year

    if years <= 0:
        return None

    growth_rate = (latest_hpi / first_hpi) ** (1 / years) - 1

    return growth_rate