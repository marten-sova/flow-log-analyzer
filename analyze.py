#!/usr/bin/env python3

"""
Data Flow Log Analyzer.
This script reads a flow log file and outputs occurences of pairs (dstport, protocol).
It also counts matches for tags defined in a lookup table.
"""

__author__ = "Marten Sova"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import csv
from iana import iana_map

DSTPORT_IDX = 6 # 7th column in v2 flow log format
IANA_IDX = 7 # 8th column in v2 flow log format

def get_protocol_name(protocol_number):
    """Return protocol name based on IANA protocol number."""
    try:
        protocol_name = iana_map.get(protocol_number, "unknown")
        if len(protocol_name) > 0:
            return protocol_name
        return "unknown"
    except ValueError:
        print(f"ERROR: Invalid protocol number: {protocol_number}")
        return "unknown"

def read_lookup_table(lookup_table_file):
    """
    Read lookup table file and return dictionary with tags.
    Expected format of the file is CSV with columns dstport,protocol,tag.
    Returned dictionary has key (dstport, protocol) and value tag name.
    """
    tags = {}
    try:
        with open(lookup_table_file, mode='r', encoding='ascii') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                dstport = row['dstport']
                protocol = row['protocol'].lower()
                tag = row['tag']
                if (dstport, protocol) in tags:
                    print(f"Ignoring tag {tag} in lookup table. ({dstport},{protocol}) is already mapped to {tags[(dstport, protocol)]}.")
                else:
                    tags[(dstport, protocol)] = tag
    except FileNotFoundError:
        print(f"ERROR: Lookup table file '{lookup_table_file}' not found.")
    except csv.Error as e:
        print(f"ERROR: An error occurred while reading the lookup table: {e}")
    return tags

def read_flow_log(flow_log_file):
    """
    Read flow log file and return dictionary with pair occurences.
    Expected format of the file is ASCII encoded flow log v2, see
    https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html
    Returned dictionary has key (dstport, protocol) and value occurences."""
    freq = {}
    min_row_length = max(DSTPORT_IDX, IANA_IDX) + 1
    try:
        with open(flow_log_file, mode='r', encoding='ascii') as file:
            for line in file:
                values = line.split()
                if len(values) >= min_row_length:
                    dstport = values[DSTPORT_IDX]
                    try:
                        iana = get_protocol_name(int(values[IANA_IDX]))
                        freq[(dstport, iana)] = freq.get((dstport, iana), 0) + 1
                    except ValueError:
                        print(f"ERROR: Invalid IANA code: {values[IANA_IDX]} is not an integer.")
    except FileNotFoundError:
        print(f"ERROR: Flow log file '{flow_log_file}' not found.")
    return freq

def count_tag_matches(flow_log, lookup_table):
    """
    Counts tag matches from (dstport, protocol) pairs in flow log.
    Expects flow_log as dictionary mapping pairs to occurences.
    Returns dictionary with tag names and occurences."""
    freq = {}
    for pair, count in flow_log.items():
        tag = lookup_table.get(pair)
        if tag:
            freq[tag] = freq.get(tag, 0) + count
        else:
            freq["Untagged"] = freq.get("Untagged", 0) + count
    return freq

def output_to_file(output_file, pair_counts, tag_counts):
    """Output pair and tag counts to a file."""
    try:
        with open(output_file, mode='w', encoding='ascii') as file:
            file.write("Tag Counts:\nTag,Count")
            for tag, count in tag_counts.items():
                file.write(f"\n{tag},{count}")
            file.write("\nPort/Protocol Combination Counts:\nPort,Protocol,Count")
            for pair, count in pair_counts.items():
                file.write(f"\n{pair[0]},{pair[1]},{count}")
    except FileNotFoundError:
        print(f"ERROR: Could not write to output file '{output_file}'.")

def main(args):
    """Main entry point of the app."""
    print("Data Flow Log Analyzer")
    print("Reading lookup table...")
    lookup_table = read_lookup_table(args.lookup_table)
    print(f"Found {len(lookup_table)} tag mappings from lookup table.")
    print("Reading flow log...")
    pair_counts = read_flow_log(args.flow_log)
    print(f"Found {len(pair_counts)} unique port/protocol combinations.")
    tag_counts = count_tag_matches(pair_counts, lookup_table)
    output_to_file("output.txt", pair_counts, tag_counts)
    print("Output written to output.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "flow_log",
        help="Required positional argument: Ascii flow log v2 file."
        "See https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html"
    )
    parser.add_argument(
        "lookup_table",
        help="Required positional argument: Ascii CSV lookup table. "
        "dstport,protocol,tag columns are required."
    )
    arguments = parser.parse_args()
    main(arguments)
