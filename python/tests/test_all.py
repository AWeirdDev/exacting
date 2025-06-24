import pytest
import exacting


def test_sum_as_string():
    assert exacting.sum_as_string(1, 1) == "2"
