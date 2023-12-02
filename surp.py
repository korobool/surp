#!/usr/bin/env python3
import sys
import subprocess

def call_gecko_news(topic):
    # Replace spaces with '+' for URL encoding
    formatted_topic = topic.strip().replace(' ', '+')
    # Define the output file name
    output_file = f"{formatted_topic}_result.txt"

    # Call the gecko_news.py script with the topic and redirect output to the file
    with open(output_file, 'w') as outfile:
        subprocess.run(['python3', 'gecko-news1.py', formatted_topic], stdout=outfile, text=True)

if __name__ == '__main__':
    # Read from standard input
    for line in sys.stdin:
        if line.strip():
            call_gecko_news(line)

