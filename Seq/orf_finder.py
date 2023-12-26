import os
import sys

class ORFFinder:
    def __init__(self, sequence):
        self.sequence = sequence

    def read_fasta(self, file_path, encoding="utf-8"):
        try:
            with open(file_path, "r", encoding=encoding) as fasta:
                lines = fasta.readlines()
                sequence = ""
                for line in lines:
                    if line[0] != ">":
                        sequence += line.strip()
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            sys.exit(1)
        except UnicodeDecodeError:
            print(f"Unable to decode the file {encoding}")
            sys.exit(1)
        return sequence

    def find_longest_orf(self, sequence):
        start = 0
        stop = 0
        longest = 0
        for i in range(0, len(sequence), 3):
            if sequence[i:i + 3] == "ATG":
                start = i
                for j in range(i, len(sequence), 3):
                    if sequence[j:j + 3] in ["TAA", "TAG", "TGA"]:
                        stop = j
                        if stop - start > longest:
                            longest = stop - start
                            longest_start = start
                            longest_stop = stop
                        break
        return longest_start, longest_stop

    def process_sequences(self, file_path):
        sequence = self.read_fasta(file_path)
        longest_start, longest_stop = self.find_longest_orf(sequence)
        longest_orf = sequence[longest_start:longest_stop + 3]
        return longest_orf, len(longest_orf)

def main():
    if len(sys.argv) != 2 and "--print_length" not in sys.argv:
        print("Usage: python orf_finder.py <file_path> [--print_length]")
        sys.exit(1)

    file_path = sys.argv[1]
    print("File path:", file_path)  # Add this line for debugging

    orf_finder = ORFFinder("")
    orf_finder.sequence = orf_finder.read_fasta(file_path, encoding="utf-8")
    longest_orf, orf_length = orf_finder.process_sequences(file_path)

    print("The longest ORF:", longest_orf)

    if "--print_length" in sys.argv:
        print("Printed ORF length:", orf_length)


if __name__ == "__main__":
    main()
