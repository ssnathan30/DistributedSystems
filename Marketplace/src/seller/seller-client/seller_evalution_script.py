from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import os
import pathlib
import sys
import seller_client_execution

# path to src directory
parent_dir = pathlib.Path(__file__).parent.resolve()

def f1():
    #os.system("python3 {0}/execution_script.py |  python3 {1}/buyer-client.py".format(parent_dir,parent_dir))
    seller_client_execution.execute()

def main():
    if len(sys.argv) > 1:
        workers = int(sys.argv[1])
    else:
        workers = 1

    with ProcessPoolExecutor(max_workers=workers) as executor:
        future_to_url = {executor.submit(f1): i for i in range(workers)}
        for future in as_completed(future_to_url):
            print("future: {}, result {} ".format(future, future.result()))

if __name__ == '__main__':
    main()