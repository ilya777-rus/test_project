import multiprocessing
import datetime

from news.utils.supermagapi import SuperMAGGetInventory, SuperMAGGetData


def get_data(stations):
    logon = 'qwert123'
    start = [2012, 1, 1, 0, 0, 0]
    flagstring = "all"
    dc = {'FORMAT': 'list'}
    points = []
    for station in stations:
        status, data = SuperMAGGetData(logon, start, 60, flagstring, station, **dc)
        try:
            points.append([data[0]['glon'], data[0]['glat']])
            print(data[0]['iaga'], [data[0]['glon'], data[0]['glat']])
        except:
            print('errrr')
    return points


def main():
    logon = 'qwert123'
    start = [2012, 1, 1, 0, 0, 0]
    (status, stations) = SuperMAGGetInventory(logon, start, 60)
    print(stations)
    print(len(stations))

    # Get the current date and time
    start_time = datetime.datetime.now()

    # Split the list of stations between processes
    num_processes =6
    station_chunks = [stations[i::num_processes] for i in range(num_processes)]

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(get_data, station_chunks)

    # Combine the results
    points_api = [point for result in results for point in result]

    # Now the list points_api contains the coordinates of all stations
    print(len(points_api))

    end_time = datetime.datetime.now()

    # Calculate the difference between the two times
    time_diff = end_time - start_time

    print(f"Processing time: {time_diff}")
    return points_api


if __name__ == '__main__':
    multiprocessing.freeze_support()
    points_api1 = main()