import tkinter as tk
from tkinter import font
from datetime import datetime
import requests



# Mock data for now - replace with your actual API
bus_stop_codes = ['67129', '67121']
service_numbers = ['50', '119', '136']
bus_stop_names = {
    '67129': "Blk 137",
    '67121': "Blk 142A"
}

url = "https://datamall2.mytransport.sg/ltaodataservice/v3/BusArrival"
headers = {
    'AccountKey': 'ezz9eDAQTiyOVO4Un4PmjQ==',
    'accept': 'application/json'
}

# Function to convert API time to minutes from now
def time_to_minutes(arrival_time_str):
    if arrival_time_str:
        arrival_time = datetime.strptime(arrival_time_str[:-6], '%Y-%m-%dT%H:%M:%S')
        current_time = datetime.now()
        time_difference = arrival_time - current_time
        minutes = divmod(time_difference.total_seconds(), 60)[0]
        if minutes <= 0:
            return "Arriving"
        return max(0, int(minutes))
    return "-"

# Function to check if the bus is a double-decker
def check_double_decker(bus_type):
    return "DD" if bus_type == "DD" else ""

# Function to update the GUI with new bus timings
def update_timings():
    for bus_stop_code in bus_stop_codes:
        params = {'BusStopCode': bus_stop_code}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        services = data.get("Services", [])
        services_sorted = sorted(services, key=lambda x: service_numbers.index(x["ServiceNo"]) if x["ServiceNo"] in service_numbers else len(service_numbers))
        
        for i, service in enumerate(services_sorted):
            bus_number = service.get("ServiceNo")
            if bus_number in service_numbers:
                next_bus = service.get("NextBus", {})
                next_bus2 = service.get("NextBus2", {})
                next_bus3 = service.get("NextBus3", {})

                # Calculate arrival times in minutes
                minutes_to_arrival_1 = time_to_minutes(next_bus.get("EstimatedArrival"))
                minutes_to_arrival_2 = time_to_minutes(next_bus2.get("EstimatedArrival"))
                minutes_to_arrival_3 = time_to_minutes(next_bus3.get("EstimatedArrival"))

                # Check if buses are double-decker
                double_decker_1 = check_double_decker(next_bus.get("Type"))
                double_decker_2 = check_double_decker(next_bus2.get("Type"))
                double_decker_3 = check_double_decker(next_bus3.get("Type"))

                # Update labels
                bus_stop_labels[bus_stop_code]['services'][i]['next_1'].config(text=f"{minutes_to_arrival_1} mins {double_decker_1}")
                bus_stop_labels[bus_stop_code]['services'][i]['next_2'].config(text=f"{minutes_to_arrival_2} mins {double_decker_2}")
                bus_stop_labels[bus_stop_code]['services'][i]['next_3'].config(text=f"{minutes_to_arrival_3} mins {double_decker_3}")

    # Optional: You can provide feedback when the timings have been updated.
    refresh_status_label.config(text="Last updated: " + datetime.now().strftime("%H:%M:%S"))

# Initialize the GUI
root = tk.Tk()
root.title("Bus Timing Display")
root.geometry("500x500")  # Adjust size based on your screen

# Set font for labels
label_font = font.Font(family="Arial", size=12)

# A dictionary to store label references
bus_stop_labels = {}

# Create UI for each bus stop and services
for bus_stop_code in bus_stop_codes:
    bus_stop_frame = tk.Frame(root)
    bus_stop_frame.pack(pady=10)

    # Bus stop title
    title_label = tk.Label(bus_stop_frame, text=f"{bus_stop_names[bus_stop_code]} ({bus_stop_code})", font=label_font)
    title_label.pack()

    bus_stop_labels[bus_stop_code] = {'frame': bus_stop_frame, 'services': []}

    for service_no in service_numbers:
        service_frame = tk.Frame(bus_stop_frame)
        service_frame.pack(pady=5)

        # Labels for bus service number and next 3 arrival times
        service_label = tk.Label(service_frame, text=f"Service {service_no}", font=label_font)
        service_label.pack(side=tk.LEFT, padx=5)

        next_1 = tk.Label(service_frame, text="Fetching...", font=label_font)
        next_1.pack(side=tk.LEFT, padx=5)

        next_2 = tk.Label(service_frame, text="Fetching...", font=label_font)
        next_2.pack(side=tk.LEFT, padx=5)

        next_3 = tk.Label(service_frame, text="Fetching...", font=label_font)
        next_3.pack(side=tk.LEFT, padx=5)

        # Store the references to the labels
        bus_stop_labels[bus_stop_code]['services'].append({
            'next_1': next_1,
            'next_2': next_2,
            'next_3': next_3
        })

# Add refresh button with a refresh icon
def refresh_icon_button():
    update_timings()
    print("Refreshing Bus Timings...")

# Create a refresh button
refresh_image = tk.PhotoImage(file="refresh_icon.png")  # Replace with path to your refresh icon image
refresh_button = tk.Button(root, image=refresh_image, command=refresh_icon_button)
refresh_button.pack(pady=0)

resized_refresh_image = refresh_image.subsample(5, 5)  # This resizes the image



# Status label to show when the data was last updated
refresh_status_label = tk.Label(root, text="", font=label_font)
refresh_status_label.pack()

# Initial call to fetch and display bus timings
update_timings()

# Start the GUI main loop
root.mainloop()
