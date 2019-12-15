#!/usr/bin/env python3

import re
import datetime
from collections import OrderedDict


class Parser:

    @staticmethod
    def trip_parser(line):
        """
        :param line: A line string from the input file, that starts with 'TRIP'
        :return: A dictionary containing trip number, base, and number of days, that have been read from the line.
        """

        line_list = re.split(r'\s+', line)
        # print(line_list)
        trip = {}
        trip['trip_number'] = int(line_list[2])
        trip['base'] = line_list[4]
        trip['number_of_days'] = int(line_list[6][0])
        # print(trip['number_of_days'])

        return trip

    @staticmethod
    def new_day(line):
        # Check the departure port is empty and sign-on time is not empty.
        if line[40:43].isspace() and not line[43:48].isspace():
            # print('new day: ' + line)
            return True
        return False

    @staticmethod
    def end_day(line):
        # Test for blank space where day is listed, and non-blank space for arrival time.
        if line[22:26].isspace() and not line[53:58].isspace():
            # print('end day: ' + line)
            return True
        return False

    @staticmethod
    def in_sector(line):
        # Flight number and departure port are both present.
        if not line[30:35].isspace() and not line[40:43].isspace():
            return True
        return False

    @staticmethod
    def sector_parser(line):
        sector = {}

        sector['flight_number'] = line[30:35]
        sector['departure_port'] = line[39:42]
        sector['departure_time'] = line[43:48]
        sector['destination_port'] = line[49:52]
        sector['arrival_time'] = line[53:58]
        sector['scheduled_time'] = line[60:64]

        if line[66:70].isspace():
            sector['turn_around_time'] = None
        else:
            turn_around_time_hour = int(line[66:67])
            turn_around_time_minute = int(line[68:70])

            sector['turn_around_time'] = datetime.time(hour=turn_around_time_hour,
                                                       minute=turn_around_time_minute)

        if line[27:30].isspace():
            sector['is_position_flight'] = False
        else:
            sector['is_position_flight'] = True

        return sector

    @staticmethod
    def order_day(day):

        day_ordered = OrderedDict(day.items())  # Re-order the dictionary in the following item order
        day_ordered['day_number'] = int(day_ordered.pop('day_number'))
        day_ordered['sign_on'] = day_ordered.pop('sign_on')
        day_ordered['day_sectors'] = day_ordered.pop('day_sectors')
        day_ordered['sign_off'] = day_ordered.pop('sign_off')
        day_ordered['flight_duty_period'] = day_ordered.pop('flight_duty_period')
        day_ordered['flight_duty_period_hours'] = day_ordered.pop('flight_duty_period_hours')
        day_ordered['flight_duty_period_minutes'] = day_ordered.pop('flight_duty_period_minutes')
        # day_ordered['lay_over'] = day_ordered.pop('lay_over')

        return day_ordered
