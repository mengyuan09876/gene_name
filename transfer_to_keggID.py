import os
import argparse

# Create an argument parser to accept command-line arguments
parser = argparse.ArgumentParser(description='Process gene abundance files.')
parser.add_argument('-a', '--abundance_dir', required=True, help='Directory containing the gene abundance files')
parser.add_argument('-b', '--filename_prefix', required=True, help='Prefix for identifying gene abundance files')
parser.add_argument('-c', '--file_extension', required=True, help='File extension for gene abundance files')
args = parser.parse_args()

# Read the gene names and numbers into a dictionary
gene_dict = {}
with open('gene_names.txt', 'r') as gene_names_file:
    for line in gene_names_file:
        gene, number = line.strip().split()
        gene_dict[gene] = number

# Directory containing the gene abundance files
abundance_files_dir = args.abundance_dir  # Use the provided directory path
filename_prefix = args.filename_prefix  # Use the provided filename prefix
file_extension = args.file_extension  # Use the provided file extension

# Loop through each gene abundance file in the directory
for filename in os.listdir(abundance_files_dir):
    if filename.startswith(filename_prefix) and filename.endswith(file_extension):
        print("Processing:", filename)  # Debugging line
        # Read the gene abundance file and replace gene names with numbers
        output_lines = []
        with open(os.path.join(abundance_files_dir, filename), 'r') as gene_abundance_file:
            header = next(gene_abundance_file)  # Read the header row (sample names)
            output_lines.append(header)  # Preserve the header row
            for line in gene_abundance_file:
                gene, *abundance_values = line.strip().split()
                if gene in gene_dict:
                    gene_number = gene_dict[gene]
                    output_line = [gene_number] + abundance_values
                    output_lines.append(' '.join(output_line))

        # Write the updated data to a new file
        output_filename = os.path.splitext(filename)[0] + '_updated.txt'
        with open(os.path.join(abundance_files_dir, output_filename), 'w') as output_file:
            output_file.write('\n'.join(output_lines))
