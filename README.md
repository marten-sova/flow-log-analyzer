# flow-log-analyzer

## How to run locally

### Download source code

1. `git clone https://github.com/marten-sova/flow-log-analyzer.git`
2. `cd flow-log-analyzer`

### Activate virtual env

3. `python3 -m venv venv`
4. `source venv/bin/activate`. _if you get permission denied, fix with:_ `chmod a+x ./venv/bin/activate`

### Run the program

`python3 analyze.py sample-flow-logs.txt sample-lookup-table.csv`

### Run tests

`python3 test.py`

## Assumptions

- Supports default v2 log format only. Reference https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html
- Tags can map to multiple (port, protocol) combinations. \_However, each (port, protocol) combination can have only one tag.
- The requirements state "The matches should be case insensitive". I assume this refers to the protocol strings in the lookup table. Tag names remain case sensitive.
- No tags are named "Untagged" (if they are, they will be counted as untagged!)

## Pseudocode

0. Load preset dict mapping protocol numbers to keywords.
1. Read in lookup table
2. create dict1 for recognizing tags. map (dst_port, protocol_keyword) to tag_name
3. create dict2 for counting tag occurences. map tag name to count.
4. create dict3 for counting pair occurences. map (dst_port, protocol_keyword) to int.
5. go through log file and add each line to dict3
6. for pairs in dict3, add that count to dict2.
