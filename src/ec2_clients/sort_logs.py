from datetime import datetime

with open('all_client_logs.txt', 'r') as file:
    lines = file.readlines()

# Parse lines and extract log times
parsed_lines = []
for line in lines:
    timestamp_str = line.split(' - ')[1][:19].strip()  # Extract the entire timestamp
    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

    # Append the timestamp along with the original line
    parsed_lines.append((timestamp, line))

sorted_lines = sorted(parsed_lines, key=lambda x: x[0])

with open('sorted_logs.txt', 'w') as file:
    for _, line in sorted_lines:
        file.write(line)

