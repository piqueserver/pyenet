import os
import subprocess
import sys
import time
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestClientServer(unittest.TestCase):
    def test_client_server(self):
        """Run test_server.py and test_client.py as subprocesses."""
        server_proc = subprocess.Popen(
            [sys.executable, os.path.join(SCRIPT_DIR, "test_server.py")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            # Give server time to bind
            time.sleep(0.5)
            self.assertIsNone(server_proc.poll(), "Server failed to start")

            # Run client with fixed seed for determinism
            client_result = subprocess.run(
                [sys.executable, os.path.join(SCRIPT_DIR, "test_client.py"), "42"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if client_result.returncode != 0:
                print("Client stdout:", client_result.stdout)
                print("Client stderr:", client_result.stderr)
            self.assertEqual(client_result.returncode, 0, "Client failed")

            # Server should exit on its own after client disconnects
            server_stdout, server_stderr = server_proc.communicate(timeout=10)
            if server_proc.returncode != 0:
                print("Server stdout:", server_stdout.decode())
                print("Server stderr:", server_stderr.decode())
            self.assertEqual(server_proc.returncode, 0, "Server failed")

        finally:
            if server_proc.poll() is None:
                server_proc.terminate()
                server_proc.wait(timeout=5)


if __name__ == "__main__":
    unittest.main()
