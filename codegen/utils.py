from datetime import datetime


def utc_time():
    # Get the current date and time
    current_time = datetime.now()

    # Format the datetime in YYYY-MM-DD-HH-MIN-SS format
    formatted_time = current_time.strftime("%Y%m%d-%H%M%S")

    # Print the formatted datetime
    print("Formatted datetime:", formatted_time)
    return formatted_time

#extract filename from absolute path
def get_filename(path):
    return path.split("/")[-1]

#strip contents between ```java and ``` if string is nested between these tokens
def strip_java_code(contents):
    if "```java" in contents and "```" in contents:
        return contents.split("```java")[1].split("```")[0]
    else:
        return contents


#save contents to a file
def save_contents(contents, filename):
    target = "/Users/mani/tmp/" + get_filename(filename)
    with open(target, 'w') as f:
        f.write(strip_java_code(contents))


