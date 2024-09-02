#!/usr/bin/env python3

"""
Random generator for log and lookup files.
This script generates sample data for testing the Data Flow Log Analyzer.
Inputs are number of lines for flow log and lookup table respectively.
"""

__author__ = "Marten Sova"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import csv
import random
import time
import uuid
from analyze import get_protocol_name

ports = [25, 68, 23, 31, 443, 22, 3389, 0, 110, 993, 143, 49153, 49154, 1024]
protocols = ['tcp', 'udp', 'icmp']
protocol_nums = [6, 17, 1]
tags = ['sv_P1', 'sv_P2', 'SV_P3', 'sv_P4', 'sv_P5', 'email']


def generate_random_ip():
    """Generate a random IP address."""
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

def generate_random_enis():
    """Generate a random ENI ID."""
    return f"eni-{''.join(random.choices('0123456789abcdef', k=8))}"

def generate_random_port():
    """Generate a random port number between 1 and 1000."""
    return random.randint(1, 1000)

def generate_random_tag():
    """Return a random preset tag or a random hex string."""
    heads = random.randint(0,1)
    if heads == 1:
        return random.choice(tags)
    return uuid.uuid4().hex[:6]

def generate_random_protocol_name():
    """Return a common protocol or an unusual protocol (50/50)"""
    heads = random.randint(0,10)
    if heads > 0:
        return random.choice(protocols)
    return get_protocol_name(random.randint(0, 145))

def generate_random_protocol_number():
    """Return a common protocol number or an unusual protocol number"""
    heads = random.randint(0,10)
    if heads > 0:
        return random.choice(protocol_nums)
    return random.randint(0, 145)

def generate_random_action():
    """Randomly choose between ACCEPT and REJECT."""
    return random.choice(["ACCEPT", "REJECT"])

def generate_random_status():
    """Randomly choose between OK and NODATA."""
    return random.choice(["OK", "NODATA"])

def generate_flow_log_entry():
    """Generate a single flow log entry with randomized values."""
    version = 2
    account_id = 123456789012
    eni = generate_random_enis()
    src_addr = generate_random_ip()
    dst_addr = generate_random_ip()
    src_port = generate_random_port()
    dst_port = generate_random_port()
    protocol = generate_random_protocol_number()
    packets = random.randint(1, 100)
    bytes_ = packets * random.randint(400, 1500)  # Average packet size between 400-1500 bytes
    start_time = int(time.time()) - random.randint(0, 10000)  # Some time in the past
    end_time = start_time + random.randint(1, 60)  # End time shortly after start time
    action = generate_random_action()
    status = generate_random_status()
    return f"{version} {account_id} {eni} {src_addr} {dst_addr} {src_port} {dst_port} {protocol} {packets} {bytes_} {start_time} {end_time} {action} {status}"

def generate_flow_log_file(file_path, num_lines):
    """Generate a file with a specified number of randomized flow log entries."""
    with open(file_path, mode='w', encoding='ascii') as file:
        for _ in range(num_lines):
            line = generate_flow_log_entry()
            file.write(line + "\n")
    print(f"Generated {num_lines} lines of flow log data in {file_path}")

def generate_random_lookup_entry():
    """Generate a single lookup table entry with randomized values."""
    dstport = generate_random_port()
    protocol = generate_random_protocol_name()
    tag = generate_random_tag()
    return [dstport, protocol, tag]

def generate_lookup_table_csv(file_path, num_entries):
    """Generate a CSV file with a specified number of randomized lookup table entries."""
    with open(file_path, mode='w', newline='', encoding='ascii') as file:
        writer = csv.writer(file)
        writer.writerow(['dstport', 'protocol', 'tag'])  # Write the header
        for _ in range(num_entries):
            entry = generate_random_lookup_entry()
            writer.writerow(entry)
    print(f"Generated {num_entries} entries in the lookup table CSV: {file_path}")

def main(args):
    """Main entry point of the app."""
    print("Sample data generator\n")
    print("Generating sample flow log file...")
    generate_flow_log_file("flow_log_generated.txt", int(args.flow_log_line_count))
    print("Generating sample lookup table CSV...")
    generate_lookup_table_csv("lookup_table_generated.csv", int(args.lookup_table_line_count))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "flow_log_line_count",
        help="Required positional argument: Number of lines to generate for flow log."
    )
    parser.add_argument(
        "lookup_table_line_count",
        help="Required positional argument: Number of lines to generate for lookup table."
    )
    arguments = parser.parse_args()
    main(arguments)
