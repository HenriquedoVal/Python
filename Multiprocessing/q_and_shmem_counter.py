import re
import sys
import time
import multiprocessing as mp
from multiprocessing.shared_memory import SharedMemory


def linear():
    with open(sys.argv[1], 'r', encoding='utf8') as stream:
        file = stream.read()
    file = re.findall("[\w]+", file)  # noqa: W605
    file = [i.lower() for i in file]
    file = {i: file.count(i) for i in set(file)}
    file = {i[0]: i[1]
            for i in sorted(
                 list(file.items()),
                 key=lambda x: x[1],
                 reverse=True)
            }
    with open(sys.argv[2], 'w') as stream:
        for k, v in file.items():
            print(f'{k}: {v}', file=stream)

    return file


def merge(a, b):
    for item in b:
        if item in a:
            a[item] += b[item]
        else:
            a[item] = b[item]
    return a


def proc(start, stop, in_q, out_q):
    sh_file = SharedMemory(name='shared file')
    data = sh_file.buf[start:stop].tobytes().decode()
    data = re.findall("[\w]+", data)  # noqa: W605
    data = [i.lower() for i in data]
    data = {i: data.count(i) for i in set(data)}
    out_q.put(data)
    sh_file.close()

    while (order := in_q.get()):
        res = merge(order[0], order[1])
        out_q.put(res)


def main():
    init = time.perf_counter()
    if len(sys.argv) < 3:
        print('Pass the file to read and output file as parameters',
              '> python mp_counter.py sherlock.txt output.txt',
              sep='\n')
        return 1

    cpu_count = mp.cpu_count()
    if cpu_count == 1:
        print('Just one process can be run at a time')
        linear()
        return 0

    with open(sys.argv[1], 'rb') as stream:
        file = stream.read()

    # Put only the largest thing that would be serialized in shared memory
    sh_file = SharedMemory(create=True,
                           name='shared file',
                           size=len(file))  # Same as sys.getsizeof
    sh_file.buf[:] = file

    in_q = mp.Queue()
    out_q = mp.Queue()
    previous = 0
    pace = 0
    for ind in range(0, len(file) + 1, len(file)//cpu_count):
        if ind == 0:
            pace += 1
            continue
        if pace != cpu_count:
            ind = file.index(b' ', ind)
        else:
            ind = len(file)
        mp.Process(
                target=proc,
                args=(previous, ind, in_q, out_q)
        ).start()
        previous = ind
        pace += 1

    # Keeps sending to queue while it can be done in parallel
    cpu_needed = cpu_count / 2
    halves_left = 0
    while cpu_needed >= 2:
        for _ in range(int(cpu_needed)):
            in_q.put((out_q.get(), out_q.get()))
        if cpu_needed != int(cpu_needed):
            cpu_needed -= .5
            halves_left += .5
        cpu_needed /= 2
        if cpu_needed + halves_left == int(cpu_needed + halves_left):
            cpu_needed += halves_left
            halves_left = 0

    # Sends signal for processes to end
    for _ in range(cpu_count):
        in_q.put(0)

    final = merge(out_q.get(), out_q.get())

    # Deals with odd number of processes
    if cpu_needed != int(cpu_needed) or halves_left:
        final = merge(final, out_q.get())

    final = {i[0]: i[1]
             for i in sorted(
                 list(final.items()),
                 key=lambda x: x[1],
                 reverse=True)
             }
    with open(sys.argv[2], 'w') as stream:
        for k, v in final.items():
            print(f'{k}: {v}', file=stream)

    sh_file.close()
    sh_file.unlink()

    print(f'Multiprocessing took {time.perf_counter() - init:.2f}s')
    print('Starting "linear"')
    init = time.perf_counter()
    print('Equal?', final == linear())
    print(f'Linear took {time.perf_counter() - init:.2f}s')
    return 0


if __name__ == "__main__":
    quit(main())
