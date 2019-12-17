#!/usr/bin/env python3

import argparse
import sys
import json
from parsers import report_parsers
from display import display_data


OUTPUT_DEFAULT = 'output_file.json'


def main():

    parser = argparse.ArgumentParser(description='Process input file and save to output file.')

    parser.add_argument('-i',
                        '--input',
                        help='File to process.',
                        action='store')

    parser.add_argument('-o',
                        '--output',
                        help='Output file.',
                        action='store')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if not args.input:
        print('Please specify input file.')
        sys.exit(1)

    if args.output:
        output_file = args.output
    else:
        output_file = OUTPUT_DEFAULT
        print(f'No output file specified. Using the default: {OUTPUT_DEFAULT}')

    trip_list = []  # the list of trips(dictionaries) to output to the data file
    trip_started = False
    day_started = False

    with open(args.input, 'r') as fh:

        while True:

            line = fh.readline()

            if line.isspace():
                continue

            if '________' in line:
                continue

            if line.startswith('TRIP'):     # detect start of a trip
                # print('Start trip' + line)

                trip = report_parsers.Parser.trip_parser(line)    # create a trip - dictionary
                trip['days'] = []   # adds a day list to the trip list

                trip_started = True     # sets trip started to true
                continue

            if trip_started:    # check if the trip has started
                if not day_started:     # check the trip has started and the new day has not started
                    if report_parsers.Parser.new_day(line):    # if new day has not started, create a new day
                        day = {}    # create a new day dictionary on each new day
                        day['sign_on'] = line[43:48]
                        day['day_sectors'] = []

                        day_started = True  # sets day started to true

            if trip_started and day_started:    # detect if a day has started within a trip

                if not report_parsers.Parser.end_day(line):   # make sure that day has not ended
                    # print('During day: ' + line)
                    day['day_number'] = line[24:26].strip()     # assign a day number to that day

                    if report_parsers.Parser.in_sector(line):     # check if a sector has started
                        day['day_sectors'].append(report_parsers.Parser.sector_parser(line))    # append sector to day

                else:   # if the day has ended, get the daily information
                    day['sign_off'] = line[53:58]
                    day['flight_duty_period'] = line[71:76].strip()
                    flight_duty_split = day['flight_duty_period'].split('h')
                    day['flight_duty_period_hours'] = int(flight_duty_split[0])
                    day['flight_duty_period_minutes'] = int(flight_duty_split[1])

                    day_started = False     # sets day started to false

                    # order the day using an OrderedDict, before adding it to the trip dict
                    day_ordered = report_parsers.Parser.order_day(day)
                    trip['days'].append(day_ordered)

            if not line[28:36].isspace() and line[27:35] == 'Sign_off':     # Detect end of a trip.
                trip_started = False

                trip_list.append(trip)

            if not line:
                break

    with open(output_file, 'w') as fh:  # Convert everything (including datetime object) to string.
        fh.write(json.dumps(trip_list, default=str, indent=4))

    display_data(output_file)

    # add mongodb functionality here


if __name__ == '__main__':
    main()
