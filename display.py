import json
from parsers import analytics_parsers


class Display:

    @staticmethod
    def length_is_zero(method):
        if len(method) is 0:
            return True
        else:
            return False

    @staticmethod
    def zero_trips_found():
        print('Zero trips found')

    @staticmethod
    def display_data(data_file):
        """ Compile all the data from the analytics parsers and display information within the terminal window. """

        with open(data_file) as f:  # file type must be json
            analytics = json.load(f)

            # queenstown returns
            zqn = analytics_parsers.AnalyticsParser(analytics)
            zqn_returns = zqn.zqn_returns()
            print()
            print(f'*****  Trips of 5 or more days that include Queenstown returns  *****')
            if Display.length_is_zero(zqn_returns):
                Display.zero_trips_found()
            else:
                for key, value in zqn_returns.items():
                    print(f'Trip: {key}\tTotal: {value}')

########################################################################################################################
            # max flight duty periods
            fdp = analytics_parsers.AnalyticsParser(analytics)
            max_fdp = fdp.max_fdp()
            print()
            print('*****  Operating FDPs rostered within 30 minutes of max AND'
                  ' positioning sectors totalling between 12hrs and 16hrs *****')
            if Display.length_is_zero(max_fdp):
                Display.zero_trips_found()
            else:
                for key, value in max_fdp.items():
                    print(f'Trip: {key} \tDay: {value.day_number}\tDuty period: {value.fdp_hours}:{value.fdp_minutes}')

########################################################################################################################
            # more than one positioning sector in a day
            dual = analytics_parsers.AnalyticsParser(analytics)
            dual_paxing = dual.dual_paxing_days()
            print()
            print('***** Days that consist of more than one paxing sector where the FDP is equal to or exceeding'
                  ' 12hrs *****')
            if Display.length_is_zero(dual_paxing):
                Display.zero_trips_found()
            else:
                for key, value in dual_paxing.items():
                    print(f'Trip: {key}\tDay: {value}')

########################################################################################################################
            # positioning before or after a return
            pax = analytics_parsers.AnalyticsParser(analytics)
            three_sectors = pax.three_sector_days()
            print()
            print('***** Positioning before or after a return *****')
            if Display.length_is_zero(three_sectors):
                Display.zero_trips_found()
            else:
                for key, value in three_sectors:
                    print(f'Trip: {key}\tDay: {value}')

########################################################################################################################
            # start on early shift and finish on late shifts
            early = analytics_parsers.AnalyticsParser(analytics)
            early_late = early.early_late()
            print()
            print('*****  Early to late duties within a trip  *****')
            if Display.length_is_zero(early_late):
                Display.zero_trips_found()
            else:
                for duty in early_late:
                    print(f'Trip: {duty}')

########################################################################################################################
            # duties with excessive turn around times
            time = analytics_parsers.AnalyticsParser(analytics)
            time_on_ground = time.time_on_ground()
            print()
            print('***** Sectors with excessive turn around times *****')
            if Display.length_is_zero(time_on_ground):
                Display.zero_trips_found()
            else:
                for key, value in time_on_ground.items():
                    print(f'Trip: {key}\tDay: {value.day_number}\tTurn time: {value.turn_time}')

########################################################################################################################
            # layover compared with previous duty
            layover = analytics_parsers.AnalyticsParser(analytics)
            rest_period = layover.rest_period()
            print()
            print('***** Rest periods less than 2 hours greater than the previous duty *****')
            if Display.length_is_zero(rest_period):
                Display.zero_trips_found()
            else:
                for key, value in rest_period.items():
                    print(f'Trip: {key}\tDay: {value.day_number}\tHours: {value.hours}\tMinutes: {value.minutes}')

########################################################################################################################
            # apw-syd sectors
            apw = analytics_parsers.AnalyticsParser(analytics)
            apw_sectors = apw.apw_single_sector()
            print()
            print('***** Single sectors APW-SYD *****')
            if Display.length_is_zero(apw_sectors):
                Display.zero_trips_found()
            else:
                for key, value in apw_sectors:
                    print(f'Trip: {key}\tDay: {value}')

########################################################################################################################
            # trips with brisbane overnights
            overnights = analytics_parsers.AnalyticsParser(analytics)
            bne_overnights = overnights.overnights()
            print()
            print('***** Trips with 1 BNE overnight *****')
            if Display.length_is_zero(bne_overnights):
                Display.zero_trips_found()
            else:
                for key, value in bne_overnights.items():
                    if value == 1:
                        print(f'Trip Number: {key}')
                print()
                print('***** Trips with 2 BNE overnights *****')
                for key, value in bne_overnights.items():
                    if 1 < value < 3:
                        print(f'Trip Number: {key}')
                print()
                print('***** Trips with 3 BNE overnights *****')
                for key, value in bne_overnights.items():
                    if value == 2 and value < 3:
                        print(f'Trip Number: {key}')
                print()
                print('***** Trips with more than 3 BNE overnights *****')
                for key, value in bne_overnights.items():
                    if value > 3:
                        print(f'Trip Number: {key}')
########################################################################################################################

            print()
