from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import os
import pathlib
import sys

# path to src directory
parent_dir = pathlib.Path(__file__).parent.resolve()

def f1():
    os.system("python3 {0}/execution_script.py |  python3 {1}/buyer-client.py".format(parent_dir,parent_dir)) 

def main():
    workers = int(sys.argv[1])
    if not workers:
        workers = 1

    with ProcessPoolExecutor(max_workers=workers) as executor:
        #work_list = [i for i in range(workers)]
        future_to_url = {executor.submit(f1): i for i in range(workers)}
        for future in as_completed(future_to_url):
            print("future: {}, result {} ".format(future, future.result()))

if __name__ == '__main__':
    main()