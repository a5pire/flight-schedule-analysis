#!/usr/bin/env python3

from analytics.analytics_parsers import AnalyticsParser
import sys
import json


with open(sys.argv[1]) as f:  # file type must be json
    analytics = json.load(f)

    def main():

        zqn = AnalyticsParser(analytics)
        zqn_returns = zqn.zqn_returns()
        print()
        print(f'*****  Trips of 5 or more days that include Queenstown returns  *****')
        print(zqn_returns)

        fdp = AnalyticsParser(analytics)
        max_fdp = fdp.max_fdp()
        print()
        print('*****  Operating FDPs rostered within 30 minutes of max & paxing sectors between 12hrs and 16hrs *****')
        for fdp in max_fdp:
            print(fdp)

        dual = AnalyticsParser(analytics)
        dual_paxing = dual.dual_paxing_days()
        print()
        print('***** Days that consist of more than one paxing sector where the FDP is equal to or exceeding'
              ' 12hrs *****')
        for day in dual_paxing:
            print(day)

        pax = AnalyticsParser(analytics)
        three_sectors = pax.three_sector_days()
        print()
        print('***** Paxing before or after a return *****')
        if three_sectors is None:
            print('Zero three sector days.')
        else:
            for p in three_sectors:
                print(p)

        early = AnalyticsParser(analytics)
        early_late = early.early_late()
        print()
        print('*****  Early to late duties within a trip  *****')
        print(early_late)

        time = AnalyticsParser(analytics)
        time_on_ground = time.time_on_ground()
        print()
        print('***** Sectors with excessive turn around times *****')
        for trip in time_on_ground:
            print(trip)

        overnights = AnalyticsParser(analytics)
        bne_overnights = overnights.overnights()
        print()


if __name__ == '__main__':
    main()
