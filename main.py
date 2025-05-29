import os
import uuid
import argparse
import logging
from agents.classifier import classify_input

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def process_file(filepath, conversation_id, dry_run=False):
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except Exception as e:
        logging.error(f"Error reading file {filepath}: {e}")
        return

    try:
        logging.info(f"Processing file {filepath}")
        if dry_run:
            logging.info("Dry run mode enabled. Skipping actual processing.")
            logging.info(f"Processed file {filepath} | Intent: NA | Format: NA")
        else:
            result = classify_input(filepath, conversation_id, content)
            logging.info(f"Processed file {filepath} | Intent: {result['intent']} | Format: {result['format']}")
    except Exception as e:
        logging.error(f"Error processing file {filepath}: {e}")
    
def main():
    parser = argparse.ArgumentParser(description='Process files')
    parser.add_argument('files', nargs='+', help='Files to process')
    parser.add_argument('--conversation_id', default=str(uuid.uuid4()), help='Conversation ID')
    parser.add_argument('--dry_run', action='store_true', help='Dry run mode')
    args = parser.parse_args()
    
    conversation_id = args.conversation_id

    for filepath_arg in args.files:
        if os.path.isfile(filepath_arg):
            process_file(filepath_arg, conversation_id, args.dry_run)

        elif os.path.isdir(filepath_arg):
            for filename in os.listdir(filepath_arg):
                fullpath = os.path.join(filepath_arg, filename)
                if os.path.isfile(fullpath):
                    process_file(fullpath, conversation_id, args.dry_run)
                else:
                    logging.info(f"Skipping non-file item in directory {filepath_arg}: {filename}")
        else:
            logging.error(f"Invalid file or directory: {filepath_arg}")
            

if __name__ == '__main__':
    main()