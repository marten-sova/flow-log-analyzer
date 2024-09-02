# V2 Flow Log Analyzer

Parses a flow log file and maps each row to a tag based on a lookup table.
Outputs summary of tag frequency and unique port/protocol combinations.

The lookup table is defined as a csv file, and it has 3 columns, `dstport,protocol,tag`.
The dstport and protocol combination decide what tag can be applied.

## How to run locally

### Download source code

1. `git clone https://github.com/marten-sova/flow-log-analyzer.git`
2. `cd flow-log-analyzer`

### Optional: run in virtual env

3. `python3 -m venv venv`
4. `source venv/bin/activate`. _if you get permission denied, fix with:_ `chmod a+x ./venv/bin/activate`

### Run the program

`python3 analyze.py sample-flow-logs.txt sample-lookup-table.csv`

### Run unit tests

`python3 test.py`

### Generate random logs for testing

This script is used to generate randomized logs and lookup tables for stress testing the program. Entries are randomized valid records/mappings with a bias toward a subset of tag names and common protocols.

`python3 generate_sample_data.py <flow_log_line_count> <lookup_table_line_count>`

## Assumptions

- Supports default v2 log format only. Reference https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html
- Tags can map to multiple (port, protocol) combinations. **However, each (port, protocol) combination can have only one tag.**
- The requirements state "The matches should be case insensitive". I assume this refers to the protocol strings in the lookup table. Tag names remain case sensitive.
- No tags are named "Untagged" (if they are, they will be counted as untagged!)

## Testing done so far

- Works with provided sample data in exercise description.
- Used `generate_sample_data.py` script to test logs with 10,000,000 entries (>1GB) and lookup tables with 10,000 entries, appears to work successfully.
