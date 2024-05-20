import os

log_folder = "client_logs"
output_file = "all_client_logs.txt"

def merge_logs():
    log_entries = []

    for filename in os.listdir(log_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(log_folder, filename)
            with open(file_path, "r") as log_file:
                lines = log_file.readlines()
                log_entries.extend(lines)

    #sort log entries based on client id
    log_entries.sort(key=lambda entry: int(entry.split(" - ")[0].split("Client ")[1]))

    with open(output_file, "w") as output_log:
        output_log.writelines(log_entries)

if __name__ == "__main__":
    merge_logs()
    print(f"Merged log entries saved to {output_file}")
