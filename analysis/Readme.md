# How to use statistical tools

## Statistical summary

statistical-summary.py is a data fetcher for InfluxDB. It makes a statistical summary for given
timeframe.

```
usage: statistical-summary.py [-h] -d DATABASE -t TABLE [-f [FIELD ...]]
                              [--tags [TAGS ...]] -u USERNAME [-p PASSWORD] [-s START]
                              [-e END] [-o OUTPUT] [-m SUMMARY]

options:
  -h, --help            show this help message and exit
  -d DATABASE, --database DATABASE
                        Influx database name
  -t TABLE, --table TABLE
                        Influx database table
  -f [FIELD ...], --field [FIELD ...]
                        Influx database field name, accepts multiple values separated
                        by spaces, e.g: -f temperature power. All fields are returned,
                        if none is given.
  --tags [TAGS ...]     Influx database tag name, accepts multiple values separated by
                        spaces, e.g: --tags device serial. Results will be grouped by
                        all values of chosen tags.
  -u USERNAME, --username USERNAME
                        InfluxDB user name
  -p PASSWORD, --password PASSWORD
                        InfluxDB password
  -s START, --start START
                        Start of timeframe being analyzed in a loose format, e.g
                        2025-10-25 12:35:13
  -e END, --end END     End of timeframe being analyzed
  -o OUTPUT, --output OUTPUT
                        Output file name for full data
  -m SUMMARY, --summary SUMMARY
                        Output file name for statistical summary of data
```

### Example
```bash
python3 statistical-summary.py -d testdb -t dbtable --start "2020.01.1 12:00:00" -f setpoint present_value power --tags serial device --summary summary.xslx --output full.xslx
```

## Linear correlation

check-correlation.py is a data correlation analyzer for InfluxDB. It checks for correlation on one or more X-series with single Y-series column.

```
usage: check-correlation.py [-h] -u USERNAME [-p PASSWORD] -d DATABASE -t TABLE
                            [-x [XFIELDS ...]] [-y YFIELD] [-s START] [-e END]

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        InfluxDB user name
  -p PASSWORD, --password PASSWORD
                        InfluxDB password
  -d DATABASE, --database DATABASE
                        Influx database name
  -t TABLE, --table TABLE
                        Influx database table
  -x [XFIELDS ...], --xfields [XFIELDS ...]
                        Influx database field names which are expected to affect
                        Y-field.
  -y YFIELD, --yfield YFIELD
                        Influx database field name which is affected by X-fields.
  -s START, --start START
                        Start of timeframe being analyzed in a loose format, e.g
                        2025-10-25 12:35:13
  -e END, --end END     End of timeframe being analyzed
```

### Example
```bash
python3 check-correlation.py -d testdb -t dbtable -s "2025.01.1 12:00:00" -xfields setpoint1 setpoint2 -yfield present_value
```
# Installing dependencies

To install all the dependencies, run the following command in the terminal:
```bash
apt update
apt install python3-dateparser python3-pandas python3-influxdb python3-sklearn
```

or

```bash
pip3 install dateparser pandas influxdb-client scikit-learn
```
