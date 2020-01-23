from datetime import datetime
from collections import namedtuple, defaultdict


class AnalyticsParser:

    def __init__(self, file):
        self.file = file

    def zqn_returns(self):
        """ Looks for days that include Queenstown returns on trips of 5 days or more. It creates a dictionary called
        zqn_trips with key:value set to trip_number:number of Queenstown returns in trip. """

        zqn_trips = []
        zqn_trip_tally = {}

        for trip in self.file:
            if trip['number_of_days'] >= 5:  # trips with number of days greater than or equal to 5
                for day in trip['days']:
                    for sector in day['day_sectors']:
                        if sector['destination_port'] == 'ZQN':  # looking for Queenstown as a destination port
                            zqn_trips.append(trip['trip_number'])  # trips with zqn added to list

        for trip_number in zqn_trips:  # loop through list of trips with Queenstown as destination
            if trip_number not in zqn_trip_tally:
                zqn_trip_tally[trip_number] = 1  # if the trip number not in zqn_trip_tally - then add it
            else:
                zqn_trip_tally[trip_number] += 1  # if the trip number is in zqn_trip_tally - add 1 'return flight'
        return zqn_trip_tally

    def max_fdp(self):
        """ Makes sure the flight duty period is not rostered in excess of max flight duty period (fdp)
        minus 30 minutes (11 hours, 30 minutes). It also looks for paxing sectors to make sure they are below 16hrs
        duty. """

        max_fdp = namedtuple('max_fdp', 'day_number fdp_hours fdp_minutes')
        trips = defaultdict(max_fdp)

        for trip in self.file:
            for day in trip['days']:
                if (day['flight_duty_period_hours'] == 11 and day['flight_duty_period_minutes'] > 29) or \
                        (12 <= day['flight_duty_period_hours'] <= 16):
                    # fdp > 11:30 or positioning duties between 12 and 16 hours
                    trip_number = trip['trip_number']
                    template = max_fdp(day_number=day['day_number'], fdp_hours=day['flight_duty_period_hours'],
                                       fdp_minutes=day['flight_duty_period_minutes'])
                    trips[trip_number] = template

        return trips

    def dual_paxing_days(self):
        """ Looks for flight duty periods that are in excess of 12 hours. This indicates ONLY multiple positioning
        sectors possible for this duty as we cannot plan to operate/fly for a duty in excess of than 12 hours. """

        dual_paxing = set()

        for trip in self.file:
            for day in trip['days']:
                if day['flight_duty_period_hours'] >= 12:  # if flight duty period hours is greater than or equal to 12
                    dual_paxing.add((trip['trip_number'], day['day_number']))

        return sorted(dual_paxing)

    def three_sector_days(self):
        """ Looks for days that have 3 sectors of flying. This function will find one positioning sector and two
        operating sectors. The result could be positioning one and operate two or operate two then position one. """

        three_sectors = set()

        for trip in self.file:
            for day in trip['days']:
                for sector in day['day_sectors']:
                    if len(day['day_sectors']) > 2:     # make sure there is more than 2 sectors for the day
                        if day['day_sectors'][0]['is_position_flight'] is True or \
                                day['day_sectors'][2]['is_position_flight'] is True:
                            # check if first or last sector for the day is positioning
                            three_sectors.add((trip['trip_number'], day['day_number']))

        return sorted(three_sectors)

    def early_late(self):
        """ Checks trips for days that start flight duty periods early in the morning on day one, then finish late in
        the afternoon or late at night on the last day of the trip. """

        early_start_late_finish = []

        for trip in self.file:
            for day in trip['days']:
                sign_on = datetime.strptime(day['sign_on'], '%H:%M')  # convert sign on time to datetime object
                if (day['day_number'] == 1) and (sign_on.hour < 6):  # day 1 of a trip sign on before 6am
                    sign_off = datetime.strptime(trip['days'][-1]['sign_off'], '%H:%M')
                    # convert sign off time to datetime object
                    if sign_off.hour > 18:
                        early_start_late_finish.append(trip['trip_number'])  # add trip number to list

        return early_start_late_finish

    def time_on_ground(self):
        """ Looks for sectors with excessive turn around times contributing to fatigue. This generally points to
        positioning sectors where a transit from international to domestic (or vise versa) is required. """

        tog = namedtuple('tog', 'day_number turn_time')
        trips = defaultdict(tog)

        for trip in self.file:
            for day in trip['days']:
                for sector in day['day_sectors']:
                    if sector['turn_around_time'] is None:
                        pass
                    else:
                        time = sector['turn_around_time']
                        time_split_hour = int(time.split(':')[0])
                        time_split_minute = int(time.split(':')[1])
                        if time_split_hour > 2 and time_split_minute > 0:
                            trip_number = trip['trip_number']
                            template = tog(day_number=day['day_number'],
                                           turn_time=sector['turn_around_time'])
                            trips[trip_number] = template

        return trips

    def rest_period(self):
        """ Compares the flight duty period with the following rest period for that day and analyses the adequacy
        of that rest period. i.e. How close to minimum rest was it? """

        rest_periods = namedtuple('rest_periods', 'day_number hours minutes')
        trips = defaultdict(rest_periods)

        for trip in self.file:
            for day in trip['days']:
                if day['lay_over_hours'] > 0 and day['lay_over_minutes'] > 0:
                    if day['lay_over_hours'] - day['flight_duty_period_hours'] < 2:
                        trip_number = trip['trip_number']
                        difference_hours = day['lay_over_hours'] - day['flight_duty_period_hours']
                        difference_minutes = day['lay_over_minutes'] - day['flight_duty_period_minutes']
                        template = rest_periods(day_number=day['day_number'], hours=difference_hours,
                                                minutes=difference_minutes)
                        trips[trip_number] = template

        return trips

    def apw_single_sector(self):
        """ Looks for pairings where crews operate APW-SYD (Apia - Sydney) and arrive mid morning which is NOT followed
        by a positioning sector. Generally, the first sector of the following day will be a positioning sector. If this
        sector is SYD-BNE (Sydney - Brisbane) the preference is to move that sector to follow the APW-SYD operating
        sector from the day before. This increases the rest for the next day and potentially avoids a 3 sector day. """

        apw_sectors = set()
        apw_syd = False
        day_number = 0

        for trip in self.file:
            for day in trip['days']:
                for sector in day['day_sectors']:
                    if sector['departure_port'] == 'APW' and sector['destination_port'] == 'SYD':
                        # look for departure from apia and arrival into sydney sector
                        apw_syd = True
                        day_number = day['day_number']
                    elif apw_syd is True and sector['departure_port'] == 'SYD' and sector['destination_port'] == 'BNE':
                        # look for apia-sydney flights that have the positioning flight afterwards
                        apw_syd = False
                        if day['day_number'] > day_number:
                            apw_sectors.add((trip['trip_number'], day['day_number']))
                    else:
                        apw_syd = False

        return sorted(apw_sectors)

    def overnights(self):
        """ Looks for the last sector of each day. If the destination_port is Brisbane, the trip_number is added to a
        dictionary that tallies total Brisbane overnights. Essentially looks for the most Brisbane overnights
        within a given trip. """

        count = {}

        for trip in self.file:
            for day in trip['days']:
                if trip['base'] == 'CHC':
                    if trip['number_of_days'] > 1:  # more than one day in the trip
                        if len(day['day_sectors']) >= 1:  # more than one sector in the day
                            if day['day_sectors'][-1]['destination_port'] == 'BNE':
                                # check destination for the last sector of each day is Brisbane
                                if trip['trip_number'] not in count:  # check if trip number not in count dictionary
                                    count[trip['trip_number']] = 1  # if it's not, initialise it with one
                                else:
                                    count[trip['trip_number']] += 1  # if it is, add one to the count

        return count

