import threading
import subprocess
import time
import os
import signal

def runServer(pyScript):
    subprocess.run(["python", pyScript])

def runTests(pyScript):
    subprocess.run(["pytest", pyScript])
    

if __name__ == "__main__":
    serverThread = threading.Thread(target=runServer, args=("server.py",))
    testThread = threading.Thread(target=runTests, args=("serverTest.py",))
    
    serverThread.start()
    time.sleep(1)
    testThread.start()

    testThread.join()
    os.kill(os.getpid(), signal.SIGTERM)