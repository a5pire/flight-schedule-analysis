#!/usr/bin/env python3
import os
import json
from collections import namedtuple
from parsers.analytics_parsers import AnalyticsParser

"""
Run these commands from within /pairings directory
1. Test the greater code base (tests that run against the main code): python -m pytest -vv

2. Find the percentage of the code base the tests cover
    : coverage run -m pytest -vv (does the same as number one above but stores the data for a coverage report)
    : coverage report -m
"""
directory = os.path.dirname(__file__)
data = os.path.join(directory, 'test_data.json')


class TestAnalyticsParsers:

    with open(data) as f:
        test_data = json.load(f)

        def test_zqn_returns(self):
            zqn_trip = AnalyticsParser(TestAnalyticsParsers.test_data)
            zqn = zqn_trip.zqn_returns()
            assert zqn == {10: 2, 17: 3, 23: 3, 35: 3, 37: 2, 40: 2, 44: 2, 49: 2, 51: 3, 52: 2, 57: 3, 63: 2, 64: 3,
                           99: 2, 103: 3, 114: 2, 118: 2, 127: 1, 132: 3, 134: 1, 138: 2, 147: 3}

        def test_max_fdp(self):
            fdp = AnalyticsParser(TestAnalyticsParsers.test_data)
            test_max_fdp = fdp.max_fdp()

            max_fdp = namedtuple('max_fdp', 'day_number fdp_hours fdp_minutes')
            trips = {2: max_fdp(day_number=2, fdp_hours=11, fdp_minutes=35),
                     64: max_fdp(day_number=3, fdp_hours=11, fdp_minutes=40),
                     124: max_fdp(day_number=2, fdp_hours=11, fdp_minutes=35)}

            assert test_max_fdp == trips

        def test_dual_paxing_days(self):
            days = AnalyticsParser(TestAnalyticsParsers.test_data)
            dual_paxing = days.dual_paxing_days()
            assert dual_paxing == [(2, 1)]

        def test_three_sector_days(self):
            three = AnalyticsParser(TestAnalyticsParsers.test_data)
            three_sectors = three.three_sector_days()
            assert three_sectors == [(64, 3), (72, 4), (93, 4), (142, 3)]

        def test_early_to_late(self):
            early = AnalyticsParser(TestAnalyticsParsers.test_data)
            early_to_late = early.early_late()
            assert early_to_late == [28, 75, 81, 104, 109]

        def test_time_on_ground(self):
            time_on_ground = AnalyticsParser(TestAnalyticsParsers.test_data)
            test_total_tog = time_on_ground.time_on_ground()

            tog = namedtuple('tog', 'day_number turn_time')
            trips = {117: tog(day_number=1, turn_time='03:05:00'), 126: tog(day_number=1, turn_time='03:05:00')}

            assert test_total_tog == trips

        def test_bne_overnights(self):
            overnights = AnalyticsParser(TestAnalyticsParsers.test_data)
            bne_overnights = overnights.overnights()
            assert bne_overnights == {103: 4, 104: 1, 105: 3, 109: 1, 110: 1, 112: 1, 115: 2, 118: 3, 119: 1, 120: 1,
                                      121: 2, 122: 1, 124: 1, 127: 1, 128: 1, 129: 2, 132: 4, 133: 2, 134: 2, 139: 1,
                                      142: 2, 145: 1, 147: 4, 151: 2}

        def test_single_sector_apw(self):
            sector = AnalyticsParser(TestAnalyticsParsers.test_data)
            apw_sector = sector.apw_single_sector()
            assert apw_sector == [(68, 5)]
