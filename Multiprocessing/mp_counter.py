import re
import sys
import time
import multiprocessing as mp


def merge(a, b):
    for item in b:
        if item in a:
            a[item] += b[item]
        else:
            a[item] = b[item]
    return a


def proc(data, in_q, out_q):
    data = re.findall("[\w]+", data)  # noqa: W605
    data = [i.lower() for i in data]
    data = {i: data.count(i) for i in set(data)}
    out_q.put((data, mp.current_process().pid))

    order = in_q.get()
    if order:
        res = merge(order[0], order[1])
        out_q.put(res)


def main():
    init = time.perf_counter()
    if len(sys.argv) < 3:
        print('Pass the file to read and output file as parameters',
              '> python mp_counter.py sherlock.txt output.txt',
              sep='\n')
        return 1

    with open(sys.argv[1], 'r', encoding='utf8') as stream:
        file = stream.read()

    # Split file to distribute through four Processes
    in_q = mp.Queue()
    out_q = mp.Queue()
    previous = 0
    pace = 0
    for ind in range(0, len(file) + 1, len(file)//4):
        if ind == 0:
            pace += 1
            continue
        if pace != 4:
            ind = file.index(' ', ind)
        else:
            ind = len(file)
        mp.Process(
                target=proc,
                args=(file[previous:ind], in_q, out_q)
        ).start()
        previous = ind
        pace += 1

    # Get return and pids to choose the ones that can finish
    # I'll need just two of them for os.cpu_count() == 4
    result = []
    pids = []
    for _ in range(4):
        answer = out_q.get()
        result.append(answer[0])
        pids.append(answer[1])

    for pid in pids:
        if pid in pids[:2]:
            in_q.put((result.pop(), result.pop()))
        else:
            in_q.put(0)  # or any with bool() == False

    final = merge(out_q.get(), out_q.get())
    final = {i[0]: i[1]
             for i in sorted(
                 list(final.items()),
                 key=lambda x: x[1],
                 reverse=True)
             }
    with open(sys.argv[2], 'w') as stream:
        for k, v in final.items():
            print(f'{k}: {v}', file=stream)

    print(f'Multiprocessing took {time.perf_counter() - init:.2f}s')
    print('Starting "linear"')
    init = time.perf_counter()
    print('Equal?', final == linear())
    print(f'Linear took {time.perf_counter() - init:.2f}s')


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


if __name__ == "__main__":
    main()
