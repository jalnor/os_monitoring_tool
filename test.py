import subprocess

import psutil



if __name__ == "__main__":

    procs = {p for p in psutil.process_iter()}
    print(procs)

    print(f'_______________________________________________\n'
          '| pid | name | status | start time | username |\n'
          '_______________________________________________\n')
    for p in procs:
        print(f'| {p} |')


