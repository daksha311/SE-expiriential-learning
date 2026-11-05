
import pytest

from amusement_park_ride_access import (
    process_ride_admissions,
    inspect_safety_restraints
)


# 1. Invalid input
def test_invalid_groups():
    with pytest.raises(ValueError):
        process_ride_admissions("invalid", 5.0)


def test_negative_express_fee():
    with pytest.raises(ValueError):
        process_ride_admissions([], -5.0)


# 2. Closed ride
def test_closed_ride():
    groups = [
        {
            "is_open": False,
            "ride_type": "family",
            "patrons": [{"height_cm": 150}]
        }
    ]
    result = process_ride_admissions(groups, 5.0)
    assert result["status"] == "ZERO_ADMISSIONS"


# 3. Different ride types
def test_roller_coaster():
    groups = [{
        "is_open": True,
        "ride_type": "roller_coaster",
        "patrons": [{"height_cm": 150}]
    }]
    result = process_ride_admissions(groups, 5.0)
    assert result["total_revenue"] == 25.0


def test_water_ride():
    groups = [{
        "is_open": True,
        "ride_type": "water_ride",
        "patrons": [{"height_cm": 150}]
    }]
    result = process_ride_admissions(groups, 5.0)
    assert result["total_revenue"] == 18.0


def test_family_ride_child():
    groups = [{
        "is_open": True,
        "ride_type": "family",
        "patrons": [{"height_cm": 130, "is_child": True}]
    }]
    result = process_ride_admissions(groups, 5.0)
    assert result["total_revenue"] == 6.0


def test_unknown_ride():
    groups = [{
        "is_open": True,
        "ride_type": "haunted_ride",
        "patrons": [{"height_cm": 150}]
    }]
    result = process_ride_admissions(groups, 5.0)
    assert result["status"] == "ZERO_ADMISSIONS"


# 4. Patron validation
def test_invalid_height():
    groups = [{
        "is_open": True,
        "ride_type": "family",
        "patrons": [{"height_cm": 0}]
    }]
    result = process_ride_admissions(groups, 5.0)
    assert result["total_revenue"] == 0.0


def test_height_below_120():
    groups = [{
        "is_open": True,
        "ride_type": "family",
        "patrons": [{"height_cm": 100}]
    }]
    result = process_ride_admissions(groups, 5.0)
    assert result["total_revenue"] == 0.0


def test_health_warning_family_ride():
    groups = [{
        "is_open": True,
        "ride_type": "family",
        "patrons": [{"height_cm": 150, "health_warning": True}]
    }]
    result = process_ride_admissions(groups, 5.0)
    assert result["total_revenue"] == 0.0


def test_health_warning_roller_coaster():
    groups = [{
        "is_open": True,
        "ride_type": "roller_coaster",
        "patrons": [
            {"height_cm": 150},
            {"height_cm": 160, "health_warning": True},
            {"height_cm": 170}
        ]
    }]
    result = process_ride_admissions(groups, 5.0)
    assert result["total_revenue"] == 0.0


# 5. Fast lane
def test_fast_lane():
    groups = [{
        "is_open": True,
        "ride_type": "family",
        "has_fast_lane": True,
        "patrons": [{"height_cm": 150}]
    }]
    result = process_ride_admissions(groups, 5.0)
    assert result["total_revenue"] == 15.0


# 6. Safety audit
def test_safety_audit():
    groups = [
        {
            "is_open": True,
            "ride_type": "unknown",
            "patrons": []
        }
        for _ in range(5)
    ]
    result = process_ride_admissions(groups, 5.0)
    assert result["status"] == "SAFETY_AUDIT"


# 7. Safety restraint inspection
def test_no_sensor_data():
    assert inspect_safety_restraints([]) == "NO_DATA"


def test_emergency_lock():
    readings = [[1, 0, 0, 1]]
    assert inspect_safety_restraints(readings) == "EMERGENCY_LOCK"


def test_safe_restraints():
    readings = [[1, 0, 1, 0, 1]]
    assert inspect_safety_restraints(readings) == "SAFE"


def test_unlatched_streak_resets():
    readings = [[0, 1, 0, 1]]
    assert inspect_safety_restraints(readings) == "SAFE"
