import numpy as np
import pandas as pd


def get_heating_dataset():
    n = 365
    outdoor_temp = 14 + 2 * \
        np.sin(np.linspace(0, 2 * np.pi, n)) + \
        np.random.normal(0, 1, size=n)
    heating = 100 - 3 * outdoor_temp + np.random.normal(0, 1.5, size=n)
    indoor_temp, energy = set_heating(
        heating, outdoor_temp, noise=True)

    outdoor_temp = np.round(outdoor_temp, 2)
    indoor_temp = np.round(indoor_temp, 2)
    energy = np.round(energy, 0)
    heating = np.round(heating, 0)

    data = pd.DataFrame({
        'day': np.arange(n),
        'outdoor_temp': outdoor_temp,
        'heating': heating,
        'indoor_temp': indoor_temp,
        'energy': energy
    })
    return data


def set_heating(heating, outdoor_temp, noise=False):
    indoor_temp = 3 + 0.15 * outdoor_temp + 0.25 * heating
    if noise:
        indoor_temp += np.random.randn(len(outdoor_temp)) * 0.5
    energy = 200 + 2 * indoor_temp + 8 * heating
    if noise:
        energy += np.random.randn(len(outdoor_temp)) * 10
    return indoor_temp, energy


def calculate_wasted_heating_cost(indoor_temp, target_temp, volume=50000, insulation_coefficient=2):
    # 50,000 cubic meters is the size of an average medium commercial warehouse
    # Insulation coefficient of 2 is quite good for a commercial warehouse
    # How far off are we from the target temperature?
    delta_temp = np.abs(indoor_temp - target_temp)
    # kW of heating wasted. 4/3412 is the conversion factor to kWh
    heating_power = volume * delta_temp * insulation_coefficient * (4/3412)
    # Heating power can't be negative
    heating_power = np.maximum(0, heating_power)

    # Daily heating cost
    heating_cost_daily = heating_power * 24 * 0.20  # 20p per kWh (cheap)
    heating_cost_total = np.mean(heating_cost_daily) * 365
    return heating_cost_total, heating_cost_daily, heating_power
