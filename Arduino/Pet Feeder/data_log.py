import serial
from datetime import datetime
import csv
import os
import time

# Define the path to the CSV file
csv_file_path = '/home/pawprint/Documents/csv_output/data_log.csv'

# Check if the file already exists and has content
file_exists = os.path.isfile(csv_file_path) and os.path.getsize(csv_file_path) > 0

#Open a csv file and set it up to receive comma delimited input
logging = open('/home/pawprint/Documents/csv_output/data_log.csv',mode='a')
writer = csv.writer(logging, delimiter=",", escapechar="\\", quoting=csv.QUOTE_NONE)

# Update the header row to include separate columns for Date and Time
if not file_exists:
    writer.writerow(["Date", "Time (EST)", "Dispense Count (#)", "Food Eaten (g)", "Water Drank (mL)"])

# Modify the section where the current time is retrieved to format date and time separately
c = datetime.now()
current_date = c.strftime('%Y-%m-%d')  # Format for the date
current_time = c.strftime('%H:%M:%S')  # Format for the time
print(current_date, current_time)

#Open a serial port that is connected to an Arduino (below is Linux, Windows and Mac would be "COM4" or similar)
#No timeout specified; program will wait until all serial data is received from Arduino
#Port description will vary according to operating system. Linux will be in the form /dev/ttyXXXX
#Windows and MAC will be COMX
ser = serial.Serial('/dev/ttyACM0')
ser.flushInput()

#Write out a single character encoded in utf-8; this is defalt encoding for Arduino serial comms
#This character tells the Arduino to start sending data
ser.write(bytes('x', 'utf-8'))

# Wait for 5 seconds to skip initial unwanted output
time.sleep(5)

# Define your thresholds
significant_difference_threshold_food = 5  # Assuming grams for Food Eaten
significant_difference_threshold_water = 10  # Assuming mL for Water Drank

# Initialize variables to store the last logged values. Initially set them to None.
last_logged_food = None
last_logged_water = None

while True:
    #Read in data from Serial until \n (new line) received
    ser_bytes = ser.readline()
    print(ser_bytes)
    
    #Convert received bytes to text format
    decoded_bytes = (ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    print(decoded_bytes)
    
    #Retreive current time
    c = datetime.now()
    current_time = c.strftime('%H:%M:%S')
    print(current_time)

    # Split decoded_bytes into a list
    data_parts = decoded_bytes.split(',')
    
    # Convert the food and water values to float for comparison
    # Note the adjustment in indices according to your CSV structure
    current_food = float(data_parts[1])  # Adjusted index for Food Eaten
    current_water = float(data_parts[2])  # Adjusted index for Water Drank
    
    # Determine if the changes are significant
    is_significant_change = False
    if last_logged_food is None or abs(current_food - last_logged_food) >= significant_difference_threshold_food:
        is_significant_change = True
    if last_logged_water is None or abs(current_water - last_logged_water) >= significant_difference_threshold_water:
        is_significant_change = True

    #If Arduino has sent a string "stop", exit loop
    if (decoded_bytes == "stop"):
         break
    
    #Write received data to CSV file

    # If there's a significant change in either value, log the data
    if is_significant_change:
        # Adjust the order of row_data according to your structure: Date, Time, data_parts
        row_data = [current_date, current_time] + data_parts
        writer.writerow(row_data)
        logging.flush()  # Ensure data is written immediately
        
        # Update the last logged values for food and water
        last_logged_food = current_food
        last_logged_water = current_water
            
# Close port and CSV file to exit
ser.close()
logging.close()
