
import pytest

from amusement_park_ride_access import (
    process_ride_admissions,
    inspect_safety_restraints
)


# 1. Input validation branches
def test_valid_input():
    result = process_ride_admissions([], 5.0)
    assert result["status"] == "ZERO_ADMISSIONS"


def test_invalid_groups_type():
    with pytest.raises(ValueError):
        process_ride_admissions("invalid", 5.0)


def test_negative_fee():
    with pytest.raises(ValueError):
        process_ride_admissions([], -1.0)


# 2. Ride open / closed branches
def test_open_ride():
    groups = [{
        "is_open": True,
        "ride_type": "family",
        "patrons": [{"height_cm": 150}]
    }]
    result = process_ride_admissions(groups, 5.0)
    assert result["status"] == "COMPLETED"


def test_closed_ride():
    groups = [{
        "is_open": False,
        "ride_type": "family",
        "patrons": [{"height_cm": 150}]
    }]
    result = process_ride_admissions(groups, 5.0)
    assert result["status"] == "ZERO_ADMISSIONS"


# 3. All ride types
def test_roller_coaster_branch():
    groups = [{
        "is_open": True,
        "ride_type": "roller_coaster",
        "patrons": [{"height_cm": 150}]
    }]
    assert process_ride_admissions(groups, 5.0)["total_revenue"] == 25.0


def test_water_ride_branch():
    groups = [{
        "is_open": True,
        "ride_type": "water_ride",
        "patrons": [{"height_cm": 150}]
    }]
    assert process_ride_admissions(groups, 5.0)["total_revenue"] == 18.0


def test_family_ride_branch():
    groups = [{
        "is_open": True,
        "ride_type": "family",
        "patrons": [{"height_cm": 150}]
    }]
    assert process_ride_admissions(groups, 5.0)["total_revenue"] == 10.0


def test_unknown_ride_branch():
    groups = [{
        "is_open": True,
        "ride_type": "unknown",
        "patrons": []
    }]
    assert process_ride_admissions(groups, 5.0)["status"] == "ZERO_ADMISSIONS"


# 4. Patron height branches
def test_zero_height():
    groups = [{
        "is_open": True,
        "ride_type": "family",
        "patrons": [{"height_cm": 0}]
    }]
    assert process_ride_admissions(groups, 5.0)["total_revenue"] == 0.0


def test_height_below_limit():
    groups = [{
        "is_open": True,
        "ride_type": "family",
        "patrons": [{"height_cm": 119}]
    }]
    assert process_ride_admissions(groups, 5.0)["total_revenue"] == 0.0


def test_height_at_limit():
    groups = [{
        "is_open": True,
        "ride_type": "family",
        "patrons": [{"height_cm": 120}]
    }]
    assert process_ride_admissions(groups, 5.0)["total_revenue"] == 10.0


# 5. Health warning branches
def test_health_warning_true():
    groups = [{
        "is_open": True,
        "ride_type": "family",
        "patrons": [{"height_cm": 150, "health_warning": True}]
    }]
    assert process_ride_admissions(groups, 5.0)["total_revenue"] == 0.0


def test_health_warning_false():
    groups = [{
        "is_open": True,
        "ride_type": "family",
        "patrons": [{"height_cm": 150, "health_warning": False}]
    }]
    assert process_ride_admissions(groups, 5.0)["total_revenue"] == 10.0


def test_roller_coaster_health_warning():
    groups = [{
        "is_open": True,
        "ride_type": "roller_coaster",
        "patrons": [
            {"height_cm": 150},
            {"height_cm": 160, "health_warning": True}
        ]
    }]
    assert process_ride_admissions(groups, 5.0)["total_revenue"] == 0.0


# 6. Child / adult branches
def test_child_patron():
    groups = [{
        "is_open": True,
        "ride_type": "family",
        "patrons": [{"height_cm": 150, "is_child": True}]
    }]
    assert process_ride_admissions(groups, 5.0)["total_revenue"] == 6.0


def test_adult_patron():
    groups = [{
        "is_open": True,
        "ride_type": "family",
        "patrons": [{"height_cm": 150, "is_child": False}]
    }]
    assert process_ride_admissions(groups, 5.0)["total_revenue"] == 10.0


# 7. Fast lane branches
def test_fast_lane_enabled():
    groups = [{
        "is_open": True,
        "ride_type": "family",
        "has_fast_lane": True,
        "patrons": [{"height_cm": 150}]
    }]
    assert process_ride_admissions(groups, 5.0)["total_revenue"] == 15.0


def test_fast_lane_disabled():
    groups = [{
        "is_open": True,
        "ride_type": "family",
        "has_fast_lane": False,
        "patrons": [{"height_cm": 150}]
    }]
    assert process_ride_admissions(groups, 5.0)["total_revenue"] == 10.0


# 8. Rejected patron count branches
def test_four_rejected_patrons():
    groups = [{
        "is_open": True,
        "ride_type": "unknown",
        "patrons": []
    } for _ in range(4)]
    assert process_ride_admissions(groups, 5.0)["status"] == "ZERO_ADMISSIONS"


def test_more_than_four_rejected_patrons():
    groups = [{
        "is_open": True,
        "ride_type": "unknown",
        "patrons": []
    } for _ in range(5)]
    assert process_ride_admissions(groups, 5.0)["status"] == "SAFETY_AUDIT"


# 9. Safety restraint branches
def test_empty_restraint_streams():
    assert inspect_safety_restraints([]) == "NO_DATA"


def test_two_consecutive_unlatched_readings():
    assert inspect_safety_restraints([[0, 0]]) == "EMERGENCY_LOCK"


def test_single_unlatched_reading():
    assert inspect_safety_restraints([[0]]) == "SAFE"


def test_latched_reading_resets_streak():
    assert inspect_safety_restraints([[0, 1, 0]]) == "SAFE"


def test_safe_sensor_readings():
    assert inspect_safety_restraints([[1, 1, 1]]) == "SAFE"
