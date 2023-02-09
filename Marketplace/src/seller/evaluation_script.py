from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import pathlib

# path to src directory
parent_dir = pathlib.Path(__file__).parent.resolve()

def f1():
    os.system("python3 {0}/execution_script.py |  python3 {1}/seller-client.py".format(parent_dir,parent_dir)) 

executors_list = []
to_do = []
with ThreadPoolExecutor(max_workers=2) as executor:
    for i in range(1):
        to_do.append(executor.submit(f1))

    for future in as_completed(to_do):
        print("future: {}, result {} ".format(future, future.result()))