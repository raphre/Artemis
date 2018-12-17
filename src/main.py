from Artemis import Artemis
import time

if __name__ == "__main__":
    artemis = Artemis('foo')
    while True:
        artemis.run()
        time.sleep(5)
