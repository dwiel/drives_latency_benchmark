import os
import time
import random
import string
import numpy as np
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def count_files_and_subdirectories(directory):
    file_count = 0
    subdirectory_count = 0

    for root, dirs, files in os.walk(directory):
        file_count += len(files)
        subdirectory_count += len(dirs)

    return file_count, subdirectory_count


class SyncLatencyHandler(FileSystemEventHandler):
    def __init__(self):
        self.latencies = []
        self.file_times = {}

    def on_created(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            if filename in self.file_times:
                write_time = self.file_times[filename]
                latency = time.time() - write_time
                self.latencies.append(latency)
                del self.file_times[filename]

def generate_random_filename(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def write_file(directory, event_handler):
    filename = generate_random_filename(10)
    file_path = os.path.join(directory, filename)
    with open(file_path, 'w') as file:
        file.write('This is a test file.')
    event_handler.file_times[filename] = time.time()

def measure_latency(src_dir, dest_dir, num_samples):
    event_handler = SyncLatencyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=dest_dir, recursive=False)
    observer.start()

    for _ in range(num_samples):
        write_file(src_dir, event_handler)
        while True:
            if len(event_handler.latencies) == _ + 1:
                break
            time.sleep(0.01)

    observer.stop()
    observer.join()

    latencies = np.array(event_handler.latencies)
    percentiles = np.percentile(latencies, [25, 50, 75, 90, 95, 99])
    mean = np.mean(latencies)
    std = np.std(latencies)

    # print("Latency Distribution:")
    # print(f"25th Percentile: {percentiles[0]:.4f} seconds")
    # print(f"50th Percentile (Median): {percentiles[1]:.4f} seconds")
    # print(f"75th Percentile: {percentiles[2]:.4f} seconds")
    # print(f"90th Percentile: {percentiles[3]:.4f} seconds")
    # print(f"95th Percentile: {percentiles[4]:.4f} seconds")
    # print(f"99th Percentile: {percentiles[5]:.4f} seconds")
    # print(f"Mean: {mean:.4f} seconds")
    # print(f"Standard Deviation: {std:.4f} seconds")

    return mean

if __name__ == '__main__':
    src_dir = '/tmp/test'
    dest_dir = '/tmp/test2'
    num_samples = 1
    for step in range(1000):
        os.system("bash /Users/zdwiel/src/drives_latency_benchmark/gen_files.sh 10")
        time.sleep(0.1)
        files, directories = count_files_and_subdirectories(src_dir)
        latency = measure_latency(src_dir, dest_dir, num_samples)
        print(f"{files}, {directories}, {latency}")
