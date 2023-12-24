import argparse
import time
import sys
from generator.data_generator import generate_data
from utils.file_handler import clear_directory
from utils.config_reader import read_defaults
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    parser = argparse.ArgumentParser(description="MagicGenerator: A utility for generating test data.")
    parser.add_argument('path_to_save_files', type=str, help='Directory path to save generated files.')
    parser.add_argument('--file_count', type=int, default=1, help='Number of JSON files to generate.')
    parser.add_argument('--file_name', type=str, default='data', help='Base file name for generated files.')
    parser.add_argument('--prefix', type=str, choices=['count', 'random', 'uuid'], help='Prefix for file names.')
    parser.add_argument('--data_schema', type=str, required=True,
                        help='JSON schema for data generation or path to schema file.')
    parser.add_argument('--data_lines', type=int, default=1000, help='Number of lines of data for each file.')
    parser.add_argument('--clear_path', action='store_true', help='Clear the directory before generating new files.')
    parser.add_argument('--multiprocessing', type=int, default=1,
                        help='Number of processes to use for file generation.')

    args = parser.parse_args()

    config = read_defaults('default.ini')

    if args.clear_path:
        clear_directory(args.path_to_save_files, args.file_name)

    logging.info("Starting data generation.")
    start_time = time.time()
    try:
        generate_data(args.data_schema, args.file_count, args.data_lines, args.path_to_save_files, args.file_name,
                      args.prefix, args.multiprocessing)
        logging.info("Data generation completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

    duration = time.time() - start_time
    print(duration)


if __name__ == "__main__":
    main()








