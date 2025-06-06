#!/usr/bin/python3

# This is a data correlation analyzer for InfluxDB. It checks for correlation
# on one or more X-series with single Y-series column.
#
# usage: check-correlation.py [-h] -u USERNAME [-p PASSWORD] -d DATABASE 
#                             -t TABLE [-x [XFIELDS ...]] [-y YFIELD]
#                             [-s START] [-e END]

# Install all dependencies first:
# apt install python3-dateparser python3-pandas python3-influxdb python3-sklearn

host = '127.0.0.1'
port= 8086

import argparse
import dateparser
import pandas
from influxdb import InfluxDBClient
from sklearn.linear_model import LinearRegression
import sklearn.metrics
import math

parser = argparse.ArgumentParser(description='This is a data correlation analyzer for InfluxDB. It checks for correlation on one or more X-series with single Y-series column.')
parser.add_argument('-u', '--username', help='InfluxDB user name', required=True)
parser.add_argument('-p', '--password', help='InfluxDB password')
parser.add_argument('-d', '--database',help='Influx database name', required=True)
parser.add_argument('-t', '--table', help='Influx database table', required=True)
parser.add_argument('-x', '--xfields', nargs='*', help='Influx database field names which are expected to affect Y-field.')
parser.add_argument('-y', '--yfield', help='Influx database field name which is affected by X-fields.')
parser.add_argument('-s', '--start', help='Start of timeframe being analyzed in a loose format, e.g 2025-10-25 12:35:13', type=dateparser.parse)
parser.add_argument('-e', '--end', type=dateparser.parse, help='End of timeframe being analyzed')
args = parser.parse_args()


def prepare_query(args):
    field_selector = ', '.join([f'"{field}"' for field in args.xfields])
    field_selector += ', ' + args.yfield

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
    
    x = dataframe[args.xfields]
    y = dataframe[args.yfield]
    model = LinearRegression()
    model.fit(x, y)
    y_pred = model.predict(x)

    print("Linear correlation equation:")
    equation = f' {args.yfield} = '
    for coefficient, column_name in zip(model.coef_, x.columns):
        if coefficient > 0:
            equation += '+ '
        equation += f"{coefficient:.2f} * {column_name} "
    equation += f"+ {model.intercept_:.2f}"
    print(equation)
    print()

    r_squared = sklearn.metrics.r2_score(y, y_pred)
    print(f"R²   = {r_squared:.3f}")

    mean_sq_error = sklearn.metrics.mean_squared_error(y, y_pred)
    root_mean_sq_error = math.sqrt(mean_sq_error)
    print(f"MSE  = {mean_sq_error:.5f}")
    print(f"RMSE = {root_mean_sq_error:.5f}")
