"""Main tests for the log analyzer functions."""
import unittest
import tempfile
from analyze import read_lookup_table, read_flow_log, count_tag_matches, output_to_file

class TestLogAnalyzer(unittest.TestCase):
    """Test cases for the log analyzer functions."""

    def test_read_lookup_table(self):
        """Test reading a lookup table with valid data."""
        csv_data = "dstport,protocol,tag\n80,tcp,web\n443,tcp,secure-web\n"
        expected = {('80', 'tcp'): 'web', ('443', 'tcp'): 'secure-web'}
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(csv_data.encode('ascii'))

        result = read_lookup_table(temp_file_path)
        self.assertEqual(result, expected)

    def test_read_flow_log(self):
        """Test reading a flow log with valid data."""
        expected = {
            ('80', 'tcp'): 1,
            ('49154', 'udp'): 2
        }
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(
                "2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 "
                "80 6 25 20000 1620140761 1620140821 ACCEPT OK\n"
                "2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 "
                "23 49154 17 15 12000 1620140761 1620140821 REJECT OK\n"
                "2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 "
                "23 49154 17 15 12000 1620140761 1620140821 ACCEPT OK"
                .encode('ascii')
              )
        result = read_flow_log(temp_file_path)
        self.assertEqual(result, expected)

    def test_count_tag_matches(self):
        """Test counting tag matches based on lookup table."""
        flow_log = {
            ('80', 'tcp'): 1,
            ('443', 'tcp'): 1,
            ('22', 'tcp'): 1
        }
        lookup_table = {
            ('80', 'tcp'): 'web',
            ('443', 'tcp'): 'secure-web'
        }
        expected = {
            'web': 1, 'secure-web': 1,
            'Untagged': 1
        }
        result = count_tag_matches(flow_log, lookup_table)
        self.assertEqual(result, expected)

    def test_output_to_file(self):
        """Test outputting to a file."""
        pair_counts = {
            ('80', 'tcp'): 1,
            ('443', 'tcp'): 2
        }
        tag_counts = {
            'web': 1, 'secure-web': 2
        }
        expected_output = (
            "Tag Counts:\nTag,Count\n"
            "web,1\nsecure-web,2\n"
            "Port/Protocol Combination Counts:\nPort,Protocol,Count\n"
            "80,tcp,1\n443,tcp,2"
        )
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name

        # Call the function with the temporary file path
        output_to_file(temp_file_path, pair_counts, tag_counts)

        # Read from the temporary file and check contents
        with open(temp_file_path, 'r', encoding='ascii') as file:
            output_content = file.read()

        self.assertEqual(output_content, expected_output)

if __name__ == '__main__':
    unittest.main()
