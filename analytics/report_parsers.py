"""
A class to manage parsing the trip reports.
"""
import re
import datetime
from collections import OrderedDict


class Parser:

    @staticmethod
    def trip_parser(line):  # function to obtain the basic information for each trip

        line_list = re.split(r'\s+', line)  # splits 'TRIP' line for individual component assignment
        # print(line_list)
        trip = {}
        trip['trip_number'] = int(line_list[2])
        trip['base'] = line_list[4]
        trip['number_of_days'] = int(line_list[6][0])
        # print(trip['number_of_days'])

        return trip

    @staticmethod
    def new_day(line):  # function to decide whether a new day has started or not
        # check that the departure port is empty and the sign-on time is not empty
        if line[40:43].isspace() and not line[43:48].isspace():
            # print('new day: ' + line)
            return True
        return False

    @staticmethod
    def end_day(line):  # function to decide whether a day has ended or not
        # test for blank space where day of the week is listed, and non-blank space for arrival time
        if line[22:26].isspace() and not line[53:58].isspace():
            # print('end day: ' + line)
            return True
        return False

    @staticmethod
    def in_sector(line):    # function to decide whether we are within a sector or not
        # check the flight number and departure port are both present
        return not line[30:35].isspace() and not line[40:43].isspace()

    @staticmethod
    def sector_parser(line):    # if we are within a sector, this function obtains the sector information
        sector = {
            'flight_number': line[30:35],
            'departure_port': line[39:42],
            'departure_time': line[43:48],
            'destination_port': line[49:52],
            'arrival_time': line[53:58],
            'scheduled_time': line[60:64],
        }


        if line[66:70].isspace():
            sector['turn_around_time'] = None
        else:
            turn_around_time_hour = int(line[66:67])
            turn_around_time_minute = int(line[68:70])

            sector['turn_around_time'] = datetime.time(hour=turn_around_time_hour,
                                                       minute=turn_around_time_minute)

        sector['is_position_flight'] = False if line[27:30].isspace() else True
        return sector

    @staticmethod
    def order_day(day):  # order the dictionary for writing to the output file

        day_ordered = OrderedDict(day.items())  # order the days information as follows:
        day_ordered['day_number'] = int(day_ordered.pop('day_number'))
        day_ordered['sign_on'] = day_ordered.pop('sign_on')
        day_ordered['day_sectors'] = day_ordered.pop('day_sectors')
        day_ordered['sign_off'] = day_ordered.pop('sign_off')
        day_ordered['flight_duty_period'] = day_ordered.pop('flight_duty_period')
        day_ordered['flight_duty_period_hours'] = day_ordered.pop('flight_duty_period_hours')
        day_ordered['flight_duty_period_minutes'] = day_ordered.pop('flight_duty_period_minutes')
        day_ordered['lay_over'] = day_ordered.pop('lay_over')
        day_ordered['lay_over_hours'] = day_ordered.pop('lay_over_hours')
        day_ordered['lay_over_minutes'] = day_ordered.pop('lay_over_minutes')

        return day_ordered

    @staticmethod
    def layover_split(layover):
        hours = layover.split('h')[0]
        minutes = layover.split('h')[1]
        return int(hours), int(minutes)
