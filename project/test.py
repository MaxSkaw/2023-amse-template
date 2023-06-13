import os

def check_file(file_path):
    return os.path.exists(file_path)

# Testing for speed

print("Checking for speed dataset.")
file_path="../speed.sqlite"
if check_file(file_path):
    print("Success! The file was found here: " + file_path)
else:
    print("Failure! The file was not found.")

# Testing for weather

print("Checking for weather dataset.")
file_path="../weather.sqlite"
if check_file(file_path):
    print("Success! The file was found here: " + file_path)
else:
    print("Failure! The file was not found.")