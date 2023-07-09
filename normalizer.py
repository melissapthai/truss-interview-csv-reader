import codecs
import csv
import pytz
import re
import sys

from datetime import datetime, timedelta


ZIP_CODE_LENGTH = 5


def convert_to_seconds(duration: str) -> float:
    """
    Takes a duration in HH:MM:SS.MS format and converts it to seconds.
    :param duration string
    :return: total seconds
    """
    hh, mm, ss, ms = tuple(map(int, re.split(r'[:.]', duration)))
    return timedelta(
        hours=hh,
        minutes=mm,
        seconds=ss,
        milliseconds=ms
    ).total_seconds()


def main():
    # Set input/output encoding to utf-8
    sys.stdin = codecs.getreader('utf-8')(sys.stdin.detach(), errors='replace')
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach(), errors='replace')

    # Create CSV reader and writer
    reader = csv.DictReader(sys.stdin)
    writer = csv.DictWriter(sys.stdout, fieldnames=reader.fieldnames)

    for row in reader:
        try:
            # Timestamp
            # Make timestamp timezone-aware (PST), convert to EST, and format as RFC3339
            ds = row['Timestamp']
            pacific_tz = pytz.timezone('US/Pacific')
            eastern_tz = pytz.timezone('US/Eastern')
            dt_pacific = datetime.strptime(ds, '%m/%d/%y %H:%M:%S %p').replace(tzinfo=pacific_tz)
            dt_eastern = dt_pacific.astimezone(eastern_tz)
            row['Timestamp'] = dt_eastern.isoformat()

            # ZIP
            # Format as 5 digits, prepend with 0's if necessary
            row['ZIP'] = '0'*(ZIP_CODE_LENGTH - len(row['ZIP'])) + row['ZIP']

            # FullName
            # Convert to uppercase
            row['FullName'] = row['FullName'].upper()

            # Address
            # Pass as is, but replace invalid characters with Unicode Replacement Character.
            row['Address'] = row['Address'].encode('utf-8').decode('utf-8', 'replace')

            # FooDuration / BarDuration
            # Convert HH:MM:SS.MS format to total number of seconds
            # TODO: should total seconds be float or int?
            foo_duration = convert_to_seconds(row['FooDuration'])
            bar_duration = convert_to_seconds(row['BarDuration'])

            row['FooDuration'] = foo_duration
            row['BarDuration'] = bar_duration

            # TotalDuration
            # Sum of FooDuration and BarDuration
            row['TotalDuration'] = foo_duration + bar_duration

            # Notes
            # Pass as is, but replace invalid characters with Unicode Replacement Character.
            row['Notes'] = row['Notes'].encode('utf-8').decode('utf-8', 'replace')

            writer.writerow(row)
        except Exception as e:
            sys.stderr.write(f'Unable to process row! {str(e)}\n')


if __name__ == '__main__':
    main()
