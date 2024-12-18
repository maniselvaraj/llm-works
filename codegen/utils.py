from datetime import datetime


def utc_time():
    # Get the current date and time
    current_time = datetime.now()

    # Format the datetime in YYYY-MM-DD-HH-MIN-SS format
    formatted_time = current_time.strftime("%Y%m%d-%H%M%S")

    # Print the formatted datetime
    print("Formatted datetime:", formatted_time)
    return formatted_time

