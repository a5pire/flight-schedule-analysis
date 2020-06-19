from analytics.report_parsers import Parser

# Run this to make it work: python -m pytest tests/


class TestParsers:

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
