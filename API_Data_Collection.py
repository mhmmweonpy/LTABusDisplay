import requests
from datetime import datetime

bus_stop_codes = ['67129', '67121']
service_numbers =['50','119','136']
bus_stop_names = {
    '67129' : "Blk 137",
    '67121' : "Blk 142A"
}

url="https://datamall2.mytransport.sg/ltaodataservice/v3/BusArrival"
headers={
    'AccountKey': 'ezz9eDAQTiyOVO4Un4PmjQ==',
    'accept': 'application/json'
}

def time_to_minutes(arrival_time_str):
    # Convert the estimated arrival time to minutes from now
    if arrival_time_str:
        # Parse the API time format 'YYYY-MM-DDTHH:MM:SS+08:00'
        arrival_time = datetime.strptime(arrival_time_str[:-6], '%Y-%m-%dT%H:%M:%S')
        # Get the current time
        current_time = datetime.now()
        # Calculate the difference in minutes
        time_difference = arrival_time - current_time
        minutes = divmod(time_difference.total_seconds(), 60)[0]  # Get only the minutes
        
        if minutes <= 0:
            return "Arriving"
        return max(0, int(minutes))  # Return the difference, ensuring it's not negative
    return None

def check_double_decker(bus_type):
    # Check if the bus type is 'DD' for double-decker
    return "Double" if bus_type == "DD" else ""

for bus_stop in bus_stop_codes:
    params = {'BusStopCode': bus_stop}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # Get the bus stop name from the dictionary
    bus_stop_name = bus_stop_names.get(bus_stop, "Unknown Bus Stop")
    
    # Extract relevant information from the data
    services = data.get("Services", [])

    # Sort services based on your preferred order (50, 119, 136)
    services_sorted = sorted(services, key=lambda x: service_numbers.index(x["ServiceNo"]) if x["ServiceNo"] in service_numbers else len(service_numbers))

    for service in services_sorted:
        bus_number = service.get("ServiceNo")
        if bus_number in service_numbers:  # Only print the buses you're interested in
            # Extract timings for next three buses
            next_bus = service.get("NextBus", {})
            next_bus2 = service.get("NextBus2", {})
            next_bus3 = service.get("NextBus3", {})
            
            # Convert arrival times to minutes from now
            minutes_to_arrival_1 = time_to_minutes(next_bus.get("EstimatedArrival"))
            minutes_to_arrival_2 = time_to_minutes(next_bus2.get("EstimatedArrival"))
            minutes_to_arrival_3 = time_to_minutes(next_bus3.get("EstimatedArrival"))
            
            # Check if the bus is a double-decker
            double_decker_1 = check_double_decker(next_bus.get("Type"))
            double_decker_2 = check_double_decker(next_bus2.get("Type"))
            double_decker_3 = check_double_decker(next_bus3.get("Type"))
            
            bus_load_1 = next_bus.get("Load")  # Bus capacity for the next 3 buses
            bus_load_2 = next_bus2.get("Load")
            bus_load_3 = next_bus3.get("Load")

            # Print the bus stop name alongside the extracted data
            print(f"Bus Stop: {bus_stop_name} ({bus_stop})")
            print(f"Bus Number: {bus_number}")
            print(f"Next 3 Arrivals (in minutes): ")
            if minutes_to_arrival_1 is not None:
                print(f"1st Bus: {minutes_to_arrival_1} mins | Load: {bus_load_1} {double_decker_1}")
            if minutes_to_arrival_2 is not None:
                print(f"2nd Bus: {minutes_to_arrival_2} mins | Load: {bus_load_2} {double_decker_2}")
            if minutes_to_arrival_3 is not None:
                print(f"3rd Bus: {minutes_to_arrival_3} mins | Load: {bus_load_3} {double_decker_3}")
            print("-" * 20)