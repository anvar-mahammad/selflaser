import datetime
from datetime import timedelta
import json

spots = {"Dodaqüstü": 5,"Bakenbard": 5,"Çənə": 5,"Üz": 10,"Boğaz": 10,"Üz+Boğaz":15,"Boyun": 10,"Boyun Forma ilə": 15,"Qolaltı": 10,
         "Barmaqlar": 5,"Qollar": 20,"Qollar Dirsəkə qədər": 15,"Sinə": 10,"Qarın (Göbəkdən aşağı)": 10,
         "Qarın": 15, "Kürək": 10, "Bel": 10, "Bikini (Üstü)": 10, "Dərin Bikini (Bikini + Popo içi)": 20,
         "Ayaqlar (dizə qədər)": 15, "Ayaqlar Tam": 20, "Popo": 10,
         "Standard- ayaqlar, qollar, qolaltı, dərin bikini, üz, boğaz": 50,
         "Full Paket - bədənin hər bir hissəsi, üz": 60, "Korreksiya - 1 nahiyyə": 10,
         "Korreksiya - 2 və ya daha çox nahiyyə": 30, "Tükün qısaldılması (bikini keçirilmir)": 5}

class Employee:
    def __init__(self, name, schedule=None):
        self.name = name
        self.schedule_increment = 10  # Assuming this is a class attribute for schedule increments
        # Attempt to load existing schedule; if not found, generate a new one
        loaded_schedule, loaded_old_schedule, loaded_procedure_times = self.load_employee_data()
        if loaded_schedule is not None:
            self.schedule = loaded_schedule
            self.old_schedule = loaded_old_schedule
            self.procedure_times = loaded_procedure_times  # Load procedure times if available
        else:
            self.schedule = self.generate_schedule()
            self.old_schedule = {}
            self.procedure_times = {}  # Initialize if not loaded

    def load_employee_data(self):
        """Attempt to load an employee's schedule, old schedule, and procedure times from employees.json."""
        try:
            with open('employee_schedules.json', 'r') as file:
                employees_data = json.load(file)
                if self.name in employees_data:
                    employee_data = employees_data[self.name]
                    return employee_data.get('schedule', {}), employee_data.get('old_schedule',
                                                                                {}), employee_data.get(
                        'procedure_times', {})
        except FileNotFoundError:
            print("The employees.json file was not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON from the file.")
        return None, None, None  # Return None if the employee data could not be loaded

    def record_procedure_times(self, procedures_dict):
        """Record new procedures and their durations."""
        self.procedure_times.update(procedures_dict)

    def get_procedure_time(self, procedure_name):
        """Retrieve the time for a specific procedure."""
        return self.procedure_times.get(procedure_name, "Procedure not found")

    def generate_schedule(self):
        """Generate a schedule with 5-minute increments for the next 2 weeks."""
        schedule = {}
        start_date = datetime.datetime.now()
        for day in range(28):  # For the next 2 weeks
            date = start_date + timedelta(days=day)
            date_str = date.strftime("%Y-%m-%d")  # Format date as YYYY-MM-DD
            schedule[date_str] = {}
            for hour in range(8,22):  # Assuming a workday from 09:00 to 17:00
                for minute in range(0, 60, self.schedule_increment):  # 5-minute increments
                    start_time = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=hour, minute=minute)
                    end_time = start_time + timedelta(minutes=self.schedule_increment)
                    time_slot = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
                    schedule[date_str][time_slot] = []
        return schedule

    def save_to_json(self):
        """Save the employee's details, schedule, old schedule, and procedure times to a JSON file."""
        employee_data = {
            self.name: {
                "schedule": self.schedule,
                "old_schedule": self.old_schedule,
                "procedure_times": self.procedure_times  # Include procedure times
            }
        }

        filename = 'employee_schedules.json'
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data.update(employee_data)

        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def book(self, date_str, start_time_str, elapsed_minutes, client_name, procedure_name):
        """
        Update the schedule with the client name and procedure for a given time period.

        :param date_str: The date for the booking in 'YYYY-MM-DD' format.
        :param start_time_str: Start time in 'HH:MM' format.
        :param elapsed_minutes: Duration of the appointment in minutes.
        :param client_name: Name of the client.
        :param procedure_name: Name of the procedure.
        """
        # Combine date and time to create a datetime object for the start time
        start_datetime_str = f"{date_str} {start_time_str}"
        start_time = datetime.datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M')
        end_time = start_time + timedelta(minutes=elapsed_minutes)
        current_time = start_time

        # The date_str is now directly used as it is provided as a parameter
        if date_str not in self.schedule:
            self.schedule[date_str] = {}

        while current_time < end_time:
            # Constructing time slot string
            next_time = current_time + timedelta(minutes=self.schedule_increment)
            time_slot_str = f"{current_time.strftime('%H:%M')} - {next_time.strftime('%H:%M')}"

            # Update the schedule for the time slot with client and procedure
            self.schedule[date_str][time_slot_str] = [client_name, procedure_name]

            # Move to the next time slot
            current_time = next_time

    def find_empty_slots(self, date_str, duration_minutes):
        """
        Find start times where the specified duration is free in the schedule.

        :param date_str: The date for which to find empty slots, in 'YYYY-MM-DD' format.
        :param duration_minutes: The total duration of free time required, in minutes.
        :param increment: The increment in minutes for checking the schedule (default is 5 minutes).
        :return: A list of start times (as strings) where the specified duration is free.
        """
        if date_str not in self.schedule:
            print(f"No schedule found for {date_str}. The entire day is available.")
            return []

        available_slots = []
        # Define the work hours
        work_start = datetime.datetime.strptime(f"{date_str} 09:00", '%Y-%m-%d %H:%M')
        work_end = datetime.datetime.strptime(f"{date_str} 22:00", '%Y-%m-%d %H:%M')
        current_time = work_start

        while current_time + timedelta(minutes=duration_minutes) <= work_end:
            # Assume the slot is free until proven otherwise
            slot_free = True

            # Check each increment within the slot for availability
            for i in range(0, duration_minutes, self.schedule_increment):
                check_time = current_time + timedelta(minutes=i)
                check_end = check_time + timedelta(minutes=self.schedule_increment)
                time_slot_str = f"{check_time.strftime('%H:%M')} - {check_end.strftime('%H:%M')}"

                # If any part of the slot is booked, mark slot as not free
                if time_slot_str in self.schedule[date_str] and self.schedule[date_str][time_slot_str] != True and \
                        self.schedule[date_str][time_slot_str] != []:
                    slot_free = False
                    break

            if slot_free:
                available_slots.append(current_time.strftime('%H:%M'))

            # Move to the next potential start time based on increment
            current_time += timedelta(minutes=self.schedule_increment)

        return available_slots

