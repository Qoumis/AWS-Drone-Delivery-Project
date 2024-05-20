mport os
import sys
import signal
import subprocess

NUMBER_OF_CLIENTS = 20
LOG_FOLDER_NAME   = 'client_logs'
CLIENT_FILE_NAME  = 'client.py'

def run_client_process(port, log_file):
    log_folder = LOG_FOLDER_NAME
    os.makedirs(log_folder, exist_ok=True)

    log_path = os.path.join(log_folder, log_file)

    #replace 'client.py' with your client script
    process = subprocess.Popen(['python3', CLIENT_FILE_NAME, str(port)],preexec_fn=os.setsid)
    return process

def main():
    processes = []

    for i in range(NUMBER_OF_CLIENTS):
        client_id = i
        log_file = f'client_{i}.txt'

        process = run_client_process(client_id, log_file)
        processes.append((i, process))
        print(f"Client with id {i} is starting...")
    print()
    try:
        while True:
            pass

    except KeyboardInterrupt:
        print("Terminating clients...")
        for i, process in processes:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)

if __name__ == '__main__':
    main()
