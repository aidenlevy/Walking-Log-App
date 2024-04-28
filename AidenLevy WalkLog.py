import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import csv


class WalkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Walk Log")

        # MOTD Banner message that sits at the top, contains my name
        self.welcome_label = tk.Label(root, text="Welcome to Walking Log\nYou can input walking data using the input fields and drop-down boxes.\nAt the bottom, there is a tool to scroll through previous entries.\nby Aiden Levy!", fg='Gold')
        self.welcome_label.pack(pady=10)

        # Frame for walking info (type, distance, date, time)
        self.walking_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
        self.walking_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.walking_label = tk.Label(self.walking_frame, text="Walking Info")
        self.walking_label.grid(row=0, column=0, columnspan=5, pady=5)

        self.walk_type_label = tk.Label(self.walking_frame, text="Select Activity Type:")
        self.walk_type_label.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)

        self.activity_options = ["Walk", "Run"]
        self.activity_combo = ttk.Combobox(self.walking_frame, values=self.activity_options)
        self.activity_combo.grid(row=1, column=1, padx=5, pady=5)

        self.distance_label = tk.Label(self.walking_frame, text="Distance:")
        self.distance_label.grid(row=1, column=2, sticky=tk.E, padx=5, pady=5)

        self.distance_entry = tk.Entry(self.walking_frame)
        self.distance_entry.grid(row=1, column=3, padx=5, pady=5)

        # Combobox for distance unit
        self.distance_unit_combo = ttk.Combobox(self.walking_frame, values=["MI", "KM"], width=3)
        self.distance_unit_combo.grid(row=1, column=4, padx=5, pady=5)
        self.distance_unit_combo.current(0)  # Set default unit to MI

        self.time_label = tk.Label(self.walking_frame, text="Time:")
        self.time_label.grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)

        self.time_entry = tk.Entry(self.walking_frame)
        self.time_entry.grid(row=2, column=1, padx=5, pady=5)

        self.date_label = tk.Label(self.walking_frame, text="Date:")
        self.date_label.grid(row=2, column=2, sticky=tk.E, padx=5, pady=5)

        self.date_entry = tk.Entry(self.walking_frame)
        self.date_entry.grid(row=2, column=3, padx=5, pady=5)

        # Frame for additional info (temp and weather)
        self.additional_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
        self.additional_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.additional_label = tk.Label(self.additional_frame, text="Additional Info")
        self.additional_label.grid(row=0, column=0, columnspan=5, pady=5)

        # Weather label
        self.weather_label = tk.Label(self.additional_frame, text="Weather:", anchor=tk.W)
        self.weather_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        # Weather Radiobuttons
        self.weather_options = ["Sunny", "Cloudy", "Rainy", "Windy"]
        self.weather_var = tk.StringVar()
        for i, option in enumerate(self.weather_options):
            rb = tk.Radiobutton(self.additional_frame, text=option, variable=self.weather_var, value=option)
            rb.grid(row=2 + i, column=0, sticky=tk.W, padx=5, pady=2)
            rb.invoke()  # Select one option by default

        # Temperature label and entry field
        self.temperature_label = tk.Label(self.additional_frame, text="Temperature (°F/°C):")
        self.temperature_label.grid(row=1, column=1, sticky=tk.E, padx=5, pady=5)

        self.temperature_entry = tk.Entry(self.additional_frame)
        self.temperature_entry.grid(row=1, column=2, padx=5, pady=5)

        self.temperature_unit_combo = ttk.Combobox(self.additional_frame, values=["Fahrenheit", "Celsius"], width=8)
        self.temperature_unit_combo.grid(row=1, column=3, padx=5, pady=5)
        self.temperature_unit_combo.current(0)  # Set default unit to Fahrenheit

        # Frame for bottom row
        self.bottom_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
        self.bottom_frame.pack(fill=tk.X, padx=10, pady=5)

        # Add a frame around the sample row
        self.sample_frame = tk.Frame(self.bottom_frame, bd=2)
        self.sample_frame.pack(side=tk.LEFT, padx=10)
        self.sample_label = tk.Label(self.sample_frame, text="SAMPLE ROW", font=("Arial", 12, "bold"))
        self.sample_label.pack()

        # View all data button
        self.vad_button = tk.Button(root, text="View All Data", command=self.display_all_data)
        self.vad_button.pack(side=tk.LEFT, padx=5)

        # Save data button
        self.save_button = tk.Button(root, text="Save Data", command=self.save_data, bg='blue', fg='blue')
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Delete all data button
        self.dad_button = tk.Button(root, text="Delete All Data", command=self.confirm_delete_data, fg='red')
        self.dad_button.pack(side=tk.LEFT, padx=5)

        # Close button
        self.clo_button = tk.Button(root, text="Close", command=root.destroy)
        self.clo_button.pack(side=tk.LEFT, padx=5)

        # Spinbox to select a row from the CSV file
        self.spinbox = tk.Spinbox(self.bottom_frame, from_=1, to=100, width=5, command=self.update_sample_row)
        self.spinbox.pack(side=tk.RIGHT)

        # Initialize the sample row
        self.update_sample_row()

    #this is my writing data function! aka Save_data()
    def save_data(self):
        # Activity
        selected_activity = self.activity_combo.get()

        # Distance and unit
        distance = self.distance_entry.get().strip()
        distance_unit = self.distance_unit_combo.get()

        # Temperature and unit
        temperature = self.temperature_entry.get().strip()
        temperature_unit = self.temperature_unit_combo.get()

        # Weather condition
        weather_condition = self.weather_var.get()

        # Date and time
        date = self.date_entry.get().strip()
        time = self.time_entry.get().strip()

        # Adding to CSV
        with open("walking_data.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([selected_activity, distance, distance_unit, temperature, temperature_unit, date, time, weather_condition])
        print("Data has been added to CSV.")

        # Clear the entry fields
        self.activity_combo.set("")  # Clear the combobox selection
        self.distance_entry.delete(0, tk.END)
        self.temperature_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.weather_var.set("")  # Clear the selected weather option

    def update_sample_row(self):
        index = int(self.spinbox.get()) - 1  # Subtract 1 to get the correct index
        data = self.read_data_from_csv(index)
        self.display_sample_row(data)

    #this is my first read data from csv function, it is used for the bottom reader row!  Get_data() #1
    def read_data_from_csv(self, index):
        try:
            with open("walking_data.csv", newline="") as file:
                reader = csv.reader(file)
                data = list(reader)
            if 0 <= index < len(data):
                return data[index]
            else:
                return None
        except FileNotFoundError:
            return None

    def display_sample_row(self, data):
        if data and len(data) >= 8:  # Ensure there's enough data to display
            for widget in self.sample_frame.winfo_children():
                widget.destroy()
            activity_type = data[0]
            distance = data[1]
            distance_unit = data[2]
            temperature = data[3]
            temperature_unit = data[4]
            date = data[5]
            time = data[6]
            weather_condition = data[7]
            sample_data_label = tk.Label(self.sample_frame, text="Activity Type: {} | Distance: {} {} | Temp: {} {} | Date: {} | Time: {} | Weather: {}".format(activity_type, distance, distance_unit, temperature, temperature_unit, date, time, weather_condition))
            sample_data_label.pack()
        else:
            for widget in self.sample_frame.winfo_children():
                widget.destroy()
            sample_data_label = tk.Label(self.sample_frame, text="There is no data for this row.")
            sample_data_label.pack()

    #this is my second read data function (it reads the csv and then adds it as text to a new window)  Get_data #2
    def display_all_data(self):
        all_data_window = tk.Toplevel(self.root)
        all_data_window.title("All Data")

        # Create a text widget to display CSV data
        text_widget = scrolledtext.ScrolledText(all_data_window, width=80, height=20)
        text_widget.pack(expand=True, fill="both")

        # Read data from CSV and insert it into the new window
        try:
            with open("walking_data.csv", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    text_widget.insert(tk.END, ' | '.join(row) + '\n')
        except FileNotFoundError:
            text_widget.insert(tk.END, "No data found.")

    def confirm_delete_data(self):
        confirm_window = tk.Toplevel(self.root)
        confirm_window.title("Are You Sure?")
        confirm_window.geometry("300x100")  # Adjust the size of the window

        confirm_label = tk.Label(confirm_window, text="Are you sure you want to delete all data?", padx=10, pady=10)  # Add padding to the label
        confirm_label.pack()

        # Buttons to confirm or cancel the delete operation
        yes_button = tk.Button(confirm_window, text="Yes, delete", command=lambda: [self.delete_all_data(), confirm_window.destroy()], fg='red')
        yes_button.pack(side=tk.LEFT, padx=5, pady=5)  # Add padding to the buttons

        no_button = tk.Button(confirm_window, text="No, go back", command=confirm_window.destroy)
        no_button.pack(side=tk.RIGHT, padx=5, pady=5)  # Add padding to the buttons

#second "writing" function. while it is deleting the entire csv, it is really replacing everything down to a single empty string, using pass.
    def delete_all_data(self):
        try:
            with open("walking_data.csv", "w", newline="") as file:
                pass  # Truncate the file to delete all data
            messagebox.showinfo("Success", "All data has been deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WalkingApp(root)
    root.geometry("800x600")
    root.configure(pady=20)
    root.mainloop()
