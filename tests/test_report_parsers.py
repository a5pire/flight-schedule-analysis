import datetime
from analytics.report_parsers import Parser


"""
Run these commands from within /pairings directory
1. Test the greater code base (tests that run against the main code): python -m pytest -vv

2. Find the percentage of the code base the tests cover
    : coverage run -m pytest -vv (does the same as number one above but stores the data for a coverage report)
    : coverage report -m
"""


class TestReportParsers:

    def test_trip_parser_dictionary(self):
        line = 'TRIP #174  174 [1CPT,1FO] CHC  Type: 4: _____6_ effective JUN 01-JUN 01 no exceptions.'
        trip = Parser.trip_parser(line)
        assert trip == {'trip_number': 174, 'base': 'CHC', 'number_of_days': 4}

    def test_new_day_true(self):
        day = Parser()
        result = day.new_day('M04 -- -- -- -- -- --      Sign_on         17:00'
                             '                  1h00                   0h00')
        assert result is True

    def test_new_day_false(self):
        day = Parser()
        result = day.new_day('                      We 2    00163    SYD 10:40 ZQN 15:40  3h00  0h45'
                             '                         _73C       [1,1,0,1,3,0,0]')
        assert result is False

    def test_end_day_true(self):
        day = Parser()
        result = day.end_day(' -- -- -- -- -- -- --                                15:25  7h20  0h30  9h55          ')
        assert result is True

    def test_end_day_false(self):
        day = Parser()
        result = day.end_day('P16 17 18 19 20 21 --    1    00113    OOL 12:15 AKL 17:15  3h00'
                             '                               _73C       [1,1,0,1,3,0,0]')
        assert result is False

    def test_in_sector_true(self):
        sector = Parser()
        result = sector.in_sector('                      We 2    00059    BNE 10:15 VLI 14:00  2h45  0h50'
                                  '                         _73C       [1,1,0,1,3,0,0]')
        assert result is True

    def test_in_sector_false(self):
        sector = Parser()
        result = sector.in_sector('                                                     00:55  3h30  0h30  5h00'
                                  '          ')
        assert result is False

    def test_sector_parser(self):
        sector_one = Parser()
        result_sector_one = sector_one.sector_parser('                      Tu 2    00094    TBU 07:00 SYD 09:45'
                                                     '  5h45  2h15                         _73C       '
                                                     '[1,1,0,1,3,0,0]')
        sector_two = Parser()
        result_sector_two = sector_two.sector_parser('                      We 3 VA_00331    MEL 14:00 BNE 16:10'
                                                     '  2h10  2h00                         _73H                ')

        sector_three = Parser()
        result_sector_three = sector_three.sector_parser('U-- -- -- -- -- -- -- Mo 1    00156'
                                                         '    AKL 18:00 BNE 19:50  3h50'
                                                         '                               _73C'
                                                         '       [1,1,0,1,3,0,0]')

        sector_four = Parser()
        result_sector_four = sector_four.sector_parser('O-- -- -- -- -- -- -- Tu 1 NZ_00296'
                                                       '    AKL 08:45 APW 13:30  3h45'
                                                       '                               _772                ')

        assert result_sector_one == {'flight_number': '00094',
                                     'departure_port': 'TBU',
                                     'departure_time': '07:00',
                                     'destination_port': 'SYD',
                                     'arrival_time': '09:45',
                                     'scheduled_time': '5h45',
                                     'turn_around_time': datetime.time(2, 15),
                                     'is_position_flight': False
                                     }

        assert result_sector_two == {'flight_number': '00331',
                                     'departure_port': 'MEL',
                                     'departure_time': '14:00',
                                     'destination_port': 'BNE',
                                     'arrival_time': '16:10',
                                     'scheduled_time': '2h10',
                                     'turn_around_time': datetime.time(2, 0),
                                     'is_position_flight': True
                                     }

        assert result_sector_three == {'flight_number': '00156',
                                       'departure_port': 'AKL',
                                       'departure_time': '18:00',
                                       'destination_port': 'BNE',
                                       'arrival_time': '19:50',
                                       'scheduled_time': '3h50',
                                       'turn_around_time': None,
                                       'is_position_flight': False
                                       }

        assert result_sector_four == {'flight_number': '00296',
                                      'departure_port': 'AKL',
                                      'departure_time': '08:45',
                                      'destination_port': 'APW',
                                      'arrival_time': '13:30',
                                      'scheduled_time': '3h45',
                                      'turn_around_time': None,
                                      'is_position_flight': True
                                      }

    def test_ordered_day(self):
        day_one = Parser()
        result = day_one.order_day({
                "flight_duty_period_minutes": 0,
                "day_number": 2,
                "sign_on": "05:15",
                "lay_over": "18h50",
                "day_sectors": [
                    {
                        "flight_number": "00094",
                        "departure_port": "TBU",
                        "departure_time": "06:15",
                        "destination_port": "SYD",
                        "arrival_time": "09:45",
                        "scheduled_time": "5h30",
                        "turn_around_time": None,
                        "is_position_flight": False
                    }
                ],
                "lay_over_minutes": 50,
                "sign_off": "10:15",
                "flight_duty_period_hours": 7,
                "flight_duty_period": "7h00",
                "lay_over_hours": 18
        }
        )

        assert result == {
                    "day_number": 2,
                    "sign_on": "05:15",
                    "day_sectors": [
                        {
                            "flight_number": "00094",
                            "departure_port": "TBU",
                            "departure_time": "06:15",
                            "destination_port": "SYD",
                            "arrival_time": "09:45",
                            "scheduled_time": "5h30",
                            "turn_around_time": None,
                            "is_position_flight": False
                        }
                    ],
                    "sign_off": "10:15",
                    "flight_duty_period": "7h00",
                    "flight_duty_period_hours": 7,
                    "flight_duty_period_minutes": 0,
                    "lay_over": "18h50",
                    "lay_over_hours": 18,
                    "lay_over_minutes": 50
        }

    def test_layover_split(self):
        zero_layover = Parser()
        layover_time = '0h00'
        zero_result_hours = zero_layover.layover_split(layover_time)[0]
        zero_result_minutes = zero_layover.layover_split(layover_time)[1]

        layover = Parser()
        layover_time = '23h50'
        result_hours = layover.layover_split(layover_time)[0]
        result_minutes = layover.layover_split(layover_time)[1]

        assert zero_result_hours == 0
        assert zero_result_minutes == 0

        assert result_hours == 23
        assert result_minutes == 50
