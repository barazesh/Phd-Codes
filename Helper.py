from datetime import datetime
import numpy as np
from numba import njit


def Logistic(b, L, k, x0, input) -> float:
    return b + L / (1 + np.exp(-k * (input - x0)))


def ConvertYearly2MonthlyRate(yearly):
    return (1 + yearly) ** (1 / 12) - 1


def Logistic4RatioLimit(input) -> float:
    result = Logistic(b=1, L=-1, k=25, x0=0.7, input=input)
    return result


def _CalculateFirstHour(month) -> int:
    a = datetime(2017, 1, 1)
    b = datetime(2017, month, 1)
    diff = b - a
    return int(diff.total_seconds() / 3600)


def CalculateFirstHour(month: int) -> int:
    return _CalculateFirstHour(month)


def CalculateLastHour(month: int) -> int:
    if month == 12:
        return -1
    return _CalculateFirstHour(month + 1)


def SliceMonth(array: np.ndarray, month) -> np.ndarray:
    first = CalculateFirstHour(month)
    last = CalculateLastHour(month)
    if last == -1:
        return array[first:]
    else:
        return array[first:last]


def GetMonthofYear(month: int) -> int:
    if (month % 12) > 0:
        return int(month % 12)
    else:
        return 12


@njit
def cumsum_with_limits(
    input: np.ndarray, lowerLimit: float, upperLimit: float, initialValue: float
) -> tuple:
    sum_value = initialValue
    violation = 0
    for x in input:
        sum_value += x
        if sum_value < lowerLimit:
            sum_value = lowerLimit
            violation += 1
        elif sum_value > upperLimit:
            sum_value = upperLimit
            # violation +=1
    return (sum_value, violation)


def CalculateIRR(outflow: float, inflow: float, period: int) -> float:
    coefficients = inflow * np.ones((period + 1))
    coefficients[-1] = -outflow
    roots = np.roots(coefficients)
    mask = roots.imag == 0
    rates = 1 / roots[mask].real - 1
    if len(rates)>0:
        result = rates.item(np.argmin(np.abs(rates)))
    else:
        result=-1
    return result
