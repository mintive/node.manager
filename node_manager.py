import argparse
import os
import signal
import subprocess
import json
import logging
from pathlib import Path

class NodeManager:
    def __init__(self, config_path):
        self.process = None
        self.config_path = config_path
        self.port = self.load_config().get("port", 8000)
        self.setup_logging()

    def load_config(self):
        """Load server configuration from JSON file."""
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        return config

    def setup_logging(self):
        """Set up logging to a file."""
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)  # Create logs directory if it doesn't exist

        logging.basicConfig(
            filename=log_dir / 'server.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def start_node(self):
        """Start the server node."""
        if self.process is not None:
            print("Node is already running.")
            return

        try:
            print(f"Starting the server node on port {self.port}...")
            self.process = subprocess.Popen(
                ['python3', '-m', 'http.server', str(self.port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            logging.info(f"Node started with PID: {self.process.pid}")
            print(f"Node started with PID: {self.process.pid}")
        except Exception as e:
            logging.error(f"Failed to start the node: {e}")
            print("Failed to start the node.")

    def stop_node(self):
        """Stop the server node."""
        if self.process is None:
            print("No node is currently running.")
            return

        print(f"Stopping the server node with PID: {self.process.pid}...")
        os.kill(self.process.pid, signal.SIGTERM)
        self.process = None
        logging.info("Node stopped.")
        print("Node stopped.")

    def status_node(self):
        """Check the status of the server node."""
        if self.process is None:
            print("Node is not running.")
        else:
            print(f"Node is running with PID: {self.process.pid}")

    def view_logs(self):
        """View the latest logs."""
        log_file = Path('logs/server.log')
        if log_file.exists():
            with log_file.open('r') as f:
                logs = f.readlines()
                print("".join(logs[-10:]))  # Print the last 10 lines of logs
        else:
            print("Log file does not exist.")

def main():
    parser = argparse.ArgumentParser(description="Manage a server node.")
    parser.add_argument('action', choices=['start', 'stop', 'status', 'logs'], help='Action to perform on the node')
    args = parser.parse_args()
    
    manager = NodeManager(config_path='config.json')

    if args.action == 'start':
        manager.start_node()
    elif args.action == 'stop':
        manager.stop_node()
    elif args.action == 'status':
        manager.status_node()
    elif args.action == 'logs':
        manager.view_logs()

if __name__ == "__main__":
    main()
