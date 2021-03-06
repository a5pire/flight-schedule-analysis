#!/usr/bin/env python3
""" Parses the pairings list and outputs a trip list as a json file.
    Args:
        -i <input_file_location>: The input file is the issued pairings report file in text file format (txt).
        -o <output_file_location>: The output file is the json formatted trip list (parsed pairings report). This
           file must be user defined. If no output file is specified, the default 'output_file.json' is used
           automatically. Json extension must be used.
    Usage:
        python main.py -i <trip_report_file_location> -o <output_file_location>
"""
import argparse
import sys
import json
from analytics.timer import Timer
from analytics.report_parsers import Parser
from display import Display
from mongo import database_insertion


OUTPUT_DEFAULT = 'output_file.json'


@Timer()
def main():
    """ See 'main.py' docstring description. """
    parser = argparse.ArgumentParser(description='Process input file and save to output file.')

    parser.add_argument('-i',
                        '--input',
                        help='Trip report file (txt file) to process.',
                        action='store')

    parser.add_argument('-o',
                        '--output',
                        help='Output file (json).',
                        action='store')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if not args.input:
        print('Please specify the trip report input text file.')
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

            if not line:
                break

            if line.isspace():
                continue

            if '________' in line:
                continue

            if line.startswith('TRIP'):     # detect start of a trip (anywhere from 1-5 days long)
                # print('Start trip' + line)

                trip = Parser.trip_parser(line)    # create a trip(dictionary)
                trip['days'] = []   # adds a day list (a list of sectors(dictionaries)) to the trip list

                trip_started = True     # sets trip started to true
                continue

            # if new day has not started, create a new day
            if trip_started and not day_started and Parser.new_day(line):
                day = {'sign_on': line[43:48], 'day_sectors': []}
                day_started = True  # sets day started to true

            if trip_started and day_started:
                if not Parser.end_day(line):
                    # print('During day: ' + line)
                    day['day_number'] = line[24:26].strip()     # assign a day number to that day

                    if Parser.in_sector(line):     # check if a sector has started
                        day['day_sectors'].append(Parser.sector_parser(line))    # append sector to day

                else:
                    day['sign_off'] = line[53:58].strip()   # get sign off time from line
                    day['flight_duty_period'] = line[71:76].strip()     # get flight duty period
                    flight_duty_split = day['flight_duty_period'].split('h')    # split flight duty period on 'h'
                    day['flight_duty_period_hours'] = int(flight_duty_split[0])     # convert to hours
                    day['flight_duty_period_minutes'] = int(flight_duty_split[1])   # convert to minutes

                    day_started = False     # sets day started to false

            if not day_started:
                if 'Sign_off' in line:  # indicated the day is finished and its only a single day trip
                    day['lay_over'] = '0h00'    # hard coded 0h00 layover as this is return flight from home base
                    day['lay_over_hours'] = 0   # hard coded 0 hours
                    day['lay_over_minutes'] = 0     # hard coded 0 minutes

                    # order the day using an OrderedDict, before adding it to the trip dict
                    day_ordered = Parser.order_day(day)
                    trip['days'].append(day_ordered)

                elif '--------------------------------' in line:    # the day is over and now layover
                    lay_over = line[88:93].strip()  # get layover from line
                    day['lay_over'] = lay_over  # add to day dictionary
                    day['lay_over_hours'] = Parser.layover_split(lay_over)[0]    # split and convert to int
                    day['lay_over_minutes'] = Parser.layover_split(lay_over)[1]  # split and convert to int

                    # order the day using an OrderedDict, before adding it to the trip dict
                    day_ordered = Parser.order_day(day)
                    trip['days'].append(day_ordered)

            if not line[28:36].isspace() and line[27:35] == 'Sign_off':     # detect end of a trip
                trip_started = False    # set trip started to False

                trip_list.append(trip)  # append the trip(dictionary) to the trip list

    with open(output_file, 'w') as fh:  # Convert everything (including datetime object) to string
        fh.write(json.dumps(trip_list, default=str, indent=4))  # write to json file for output

    Display.display_data(output_file)   # display analytics data within the terminal

    return output_file


if __name__ == '__main__':
    data = main()
    print()
    database_insertion(data)
