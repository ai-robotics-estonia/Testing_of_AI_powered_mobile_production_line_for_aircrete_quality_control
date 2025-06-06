#!/usr/bin/python3

# This is a data fetcher for InfluxDB.
# It makes a statistical summary for a given timeframe.
#
# usage: statistical-summary.py [-h] -d DATABASE -t TABLE [-f [FIELD ...]] 
#                               [--tags [TAGS ...]] -u USERNAME [-p PASSWORD]
#                               [-s START] [-e END] [-o OUTPUT] [-m SUMMARY]

# Install all dependencies first:
# apt install python3-dateparser python3-pandas python3-influxdb

host = '127.0.0.1'
port= 8086

import argparse
import dateparser
import pandas
from influxdb import InfluxDBClient

parser = argparse.ArgumentParser(description='This is a data fetcher for InfluxDB. It makes a statistical summary for a given timeframe.')
parser.add_argument('-d', '--database',help='Influx database name', required=True)
parser.add_argument('-t', '--table', help='Influx database table', required=True)
parser.add_argument('-f', '--field', nargs='*', help='Influx database field name, accepts multiple values separated by spaces, e.g: -f temperature power. All fields are returned, if none is given.')
parser.add_argument('--tags', nargs='*', help='Influx database tag name, accepts multiple values separated by spaces, e.g: --tags device serial. Results will be grouped by all values of chosen tags.')
parser.add_argument('-u', '--username', help='InfluxDB user name', required=True)
parser.add_argument('-p', '--password', help='InfluxDB password')
parser.add_argument('-s', '--start', help='Start of timeframe being analyzed in a loose format, e.g 2025-10-25 12:35:13', type=dateparser.parse)
parser.add_argument('-e', '--end', type=dateparser.parse, help='End of timeframe being analyzed')
parser.add_argument('-o', '--output', help='Output file name for full data')
parser.add_argument('-m', '--summary', help='Output file name for statistical summary of data')
args = parser.parse_args()


def prepare_query(args):
    if args.field:
        field_selector = ', '.join([f'"{field}"' for field in args.field])
        field_selector += ', ' + ', '.join([f'"{tag}"' for tag in args.tags])
    else:
        field_selector = '*'

    time_condition = ''
    elements = 0
    if args.start:
        timestring = args.start.strftime('%Y-%m-%dT%H:%M:%SZ')
        time_condition += f" WHERE time >= '{timestring}'"
        elements += 1
    if args.end:
        timestring = args.end.strftime('%Y-%m-%dT%H:%M:%SZ')
        if elements < 1:
            time_condition += f" WHERE time <= '{timestring}'"
        else:
            time_condition += f" AND time <= '{timestring}'"

    return f'SELECT {field_selector} FROM "{args.table}" {time_condition};'


client = InfluxDBClient(host=host, port=port, username=args.username, password=args.password, database=args.database)
query = prepare_query(args)
result = client.query(query, epoch='ms')


for row in result:
    dataframe = pandas.DataFrame.from_dict(row)
    dataframe.set_index('time', inplace = True)
    dataframe.index = pandas.to_datetime(dataframe.index, unit='ms')
    print('Data start: ', dataframe.index.min())
    print('Data end:   ', dataframe.index.max())
    print('Data points count by field:')
    print(dataframe.count())
    print()
    
    if args.summary:
        summary = dataframe.groupby(args.tags).describe()
        filename = args.summary
        if not filename.lower().endswith('.xslx'):
            filename = f"{filename}.xlsx"
        summary.to_excel(filename)
        print("Exported data summary to", filename)

    # Exporting all data
    if args.output:
        index = dataframe.index
        other = []
        for tag in args.tags:
            other.append(dataframe[tag])
        other.append(index)
        mi = pandas.MultiIndex.from_arrays(other)
        dataframe.index = mi
        dataframe.sort_index(inplace=True)

        filename = args.output
        if not filename.lower().endswith('.xslx'):
            filename = f"{filename}.xlsx"
        dataframe.to_excel(filename)
        print("Exported all data to", filename)
