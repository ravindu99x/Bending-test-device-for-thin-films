#Author: HD Ravindu Lakshan - Department of Physics - University of Colombo -
#Last Edited on 4th of September 2024

import tkinter as tk
import serial
from serial.tools.list_ports import comports
import csv
import time
import pyvisa as visa
from datetime import datetime

ser = None  # Global variable for serial connection

# Open the connection to the DMM
rm = visa.ResourceManager()
dmm = rm.open_resource('USB0::0x05E6::0x2100::1373334::INSTR')
dmm.timeout = 10000  # Set timeout to 10 seconds

# Open the CSV file for writing
file = open('conc_1.csv', mode='w', newline='')
writer = csv.writer(file)
writer.writerow(['Count', 'Time', 'Resistance'])

# Function to send values to Arduino
def send_values():
    global ser
    if ser is not None:
        speed_value = speed_entry.get()
        bend_value = bend_entry.get()
        dead_value = dead_var.get()

        # Format the values to send to Arduino
        command = "{:04d}{:03d}{}".format(int(speed_value), int(bend_value), int(dead_value))
        print("Sending command:", command)
        ser.write(command.encode())  # Send the command to Arduino
    else:
        print("Serial connection is not initialized.")

# Function to write DMM data to the CSV file
def write_dmm(count):
    reading = dmm.query_ascii_values('READ?')[0]  # Extract the value from the list
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Get the current timestamp with milliseconds
    data_row = [count, timestamp, reading]
    print(data_row)
    # Write the data to the CSV file
    writer.writerow(data_row)
    file.flush()  # Ensure data is written to file

# Function to update the count displayed on the GUI
def update_count(serial_connection):
    if serial_connection is not None and serial_connection.in_waiting > 0:
        count = serial_connection.readline().decode().strip()
        #if count != '0':  # Update and write only if count is not zero
        count_label.config(text=f"Count: {count}")
        write_dmm(count)  # Call the function to write DMM data to the CSV file

# Function to refresh the list of available COM ports
def refresh_ports():
    global ser
    # Get updated list of available COM ports
    ports = [port.device for port in comports()]
    port_menu['menu'].delete(0, 'end')  # Clear previous options
    for port in ports:
        port_menu['menu'].add_command(label=port, command=lambda p=port: select_port(p))

# Function to select a COM port
def select_port(port):
    global ser
    if ser is not None and ser.is_open:
        ser.close()
    ser = serial.Serial(port, 9600)
    print("Selected COM Port:", port)
    # Update count display function with the new serial connection
    window.after(100, update_count, ser)

# Create the Tkinter window
window = tk.Tk()
window.title("Arduino Control")
window.geometry("550x500")  # Set window size to 800x700

# Create a drop-down menu for selecting COM port
application = tk.Label(window, text="Flexible Electronic Laboratory - Department of Physics", font=("Arial", 8))
application.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
port_label = tk.Label(window, text="Select COM Port:", font=("Arial", 16))
port_label.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

# Create a StringVar to hold the selected COM port
selected_port = tk.StringVar()
selected_port.set("Select a port")  # Default text for the drop-down menu

port_menu = tk.OptionMenu(window, selected_port, "")
port_menu.config(font=("Arial", 14))
port_menu.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

# Create a button to refresh available ports
refresh_button = tk.Button(window, text="Refresh Ports", font=("Arial", 14), command=refresh_ports, width=15, height=2)
refresh_button.grid(row=2, columnspan=2, padx=10, pady=10, sticky='nsew')

# Initialize serial connection to default COM port
refresh_ports()  # Populate the initial list of ports

# Create labels and entry fields for speed and bend
speed_label = tk.Label(window, text="Speed (3000-1000):", font=("Arial", 14))
speed_label.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')
speed_entry = tk.Entry(window, font=("Arial", 14))
speed_entry.grid(row=3, column=1, padx=10, pady=10, sticky='nsew')

bend_label = tk.Label(window, text="Bend:", font=("Arial", 16))
bend_label.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')
bend_entry = tk.Entry(window, font=("Arial", 14))
bend_entry.grid(row=4, column=1, padx=10, pady=10, sticky='nsew')

# Create a checkbox for dead
dead_var = tk.IntVar()
dead_checkbox = tk.Checkbutton(window, text="Reset Count", variable=dead_var, font=("Arial", 16))
dead_checkbox.grid(row=5, columnspan=2, padx=10, pady=10, sticky='nsew')

# Create a button to send values
send_button = tk.Button(window, text="Send Values", font=("Arial", 16), command=send_values, width=15, height=2)
send_button.grid(row=6, columnspan=2, padx=10, pady=10, sticky='nsew')

# Create a label to display the count
count_label = tk.Label(window, text="Count: 0", font=("Arial", 16))
count_label.grid(row=7, columnspan=2, padx=10, pady=10, sticky='nsew')

csv_file = tk.Label(window, text="Please find the CSV file in the same folder where the software is executed.", font=("Arial", 9))
csv_file.grid(row=8, columnspan=9, padx=10, pady=10, sticky='nsew')

# owner_label = tk.Label(window, text="HDRLakshan", font=("Arial", 7))
# owner_label.grid(row=8, columnspan=9, padx=10, pady=10, sticky='nsew')

# Function to periodically update the count
def update():
    update_count(ser)
    window.after(100, update)  # Update every 100 milliseconds

update()

window.mainloop()

# Close the file when the program ends
file.close()
