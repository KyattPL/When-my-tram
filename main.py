import datetime

trips = []


def open_file():
    lines = []
    with open("trips.txt", "r", encoding="utf8") as file:
        lines = file.readlines()
    for line in lines:
        row = line.split(",")
        trips.append(row)


def find_trips(trip_name, dest):
    your_vehicle = []
    dest = "\"" + dest.upper() + "\""
    for trip in trips:
        if trip[0] == trip_name and trip[3] == dest:
            your_vehicle.append(trip[2])
    return your_vehicle


def save_trip(trip_ids):
    with open("your_trip.txt", "w") as file:
        for trip_id in trip_ids:
            file.write(trip_id + "\n")


def save_stop_times(trip_ids, stop_id):
    stop_times = []
    with open("stop_times.txt", "r") as file:
        stop_times = file.readlines()

    stop_times_split = []
    for line in stop_times:
        stop_times_split.append(line.split(","))

    your_stop_times = []
    for trip_id in trip_ids:
        for stop_time in stop_times_split:
            if trip_id == stop_time[0] and stop_id == stop_time[3]:
                your_stop_times.append(stop_time)

    with open("your_stop_times.txt", "w") as file:
        for stop_time in your_stop_times:
            file.write(str(stop_time) + "\n")


def find_stop_id(stop_name):
    stops = []
    stop_name = "\"" + stop_name.upper() + "\""
    with open("stops.txt", "r", encoding="utf8") as file:
        stops = file.readlines()

    stops_splitted = []
    for stop in stops:
        stops_splitted.append(stop.split(","))

    for stop in stops_splitted:
        if stop_name == stop[2].upper():
            return stop[0]


def get_current_time():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second
    if hour < 10:
        hour = "0" + str(hour)
    else:
        hour = str(hour)
    if minute < 10:
        minute = "0" + str(minute)
    else:
        minute = str(minute)
    if second < 10:
        second = "0" + str(second)
    else:
        second = str(second)
    time = hour + ":" + minute + ":" + second
    return time


def is_sooner(stop_time, minimum, current):
    diff = difference(stop_time, current)
    return diff < minimum


def difference(stop_time, current):
    time = to_seconds(stop_time)
    current_time = to_seconds(current)
    diff = time - current_time
    if diff < 0:
        diff += 86_400
    return diff


def to_seconds(stop_time):
    split_time = stop_time.split(":")
    hour = int(split_time[0].replace("'", ""))
    minute = int(split_time[1].replace("'", ""))
    second = int(split_time[2].replace("'", ""))
    time = hour * 3600 + minute * 60 + second
    return time


def next_stop(time):
    stop_times = []
    with open("your_stop_times.txt", "r") as file:
        stop_times = file.readlines()

    stop_times_splitted = []
    for stop_time in stop_times:
        stop_times_splitted.append(stop_time.split(","))

    minimum = 86_400
    minimum_time = "25:25:25"
    for stop_time in stop_times_splitted:
        if is_sooner(stop_time[2], minimum, time):
            minimum = difference(stop_time[2], time)
            minimum_time = stop_time[2]

    return minimum_time


if __name__ == "__main__":
    open_file()
    while True:
        read = input("New/Existing (0/1): ")
        if read == "0":
            choice = input("Tram/Bus name: ")
            destination = input("Destination: ")
            stop = input("Stop name: ")
            trip_ids = find_trips(choice, destination)
            save_trip(trip_ids)
            stop_id = find_stop_id(stop)
            save_stop_times(trip_ids, stop_id)
            print("Next tram: ", end="")
            time = get_current_time()
            output = next_stop(time)
            print(output)
        else:
            print("Next tram: ", end="")
            time = get_current_time()
            output = next_stop(time)
            print(output)
