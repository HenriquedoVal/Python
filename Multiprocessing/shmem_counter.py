import re
import sys
import time
import multiprocessing as mp
from multiprocessing.shared_memory import ShareableList


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


def proc():
    shl_words = ShareableList(name='shared words')
    shl_set = ShareableList(name='shared set')
    shl_counter = ShareableList(name='shared counter')
    shl_args = ShareableList(name='shared args')

    name = mp.current_process().name
    ind = int(name[name.rindex('-')+1:]) - 1

    # Not making copies will make it EXTREMELY slow
    words_copy = [i for i in shl_words]  # shl_words[:] doesn't work
    set_copy = [i for i in shl_set]

    for i in range(shl_args[ind], shl_args[ind+1]):
        shl_counter[i] = words_copy.count(set_copy[i])

    for obj in (shl_words, shl_set, shl_counter, shl_args):
        obj.shm.close()


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

    with open(sys.argv[1], 'r', encoding='utf8') as stream:
        file = stream.read()

    list_words = re.findall("[\w]+", file)  # noqa: W605
    list_words = [i.lower() for i in list_words]
    set_words = set(list_words)

    args = [0]
    pace = 0
    for ind in range(0, len(set_words) + 1, len(set_words)//cpu_count):
        if ind == 0:  # if it is the first pace
            pace += 1
            continue
        if pace == cpu_count:  # if it is the last pace
            ind = len(set_words)
        args.append(ind)
        pace += 1

    shl_words = ShareableList(list_words, name='shared words')
    shl_set = ShareableList(set_words, name='shared set')
    shl_counter = ShareableList([0] * len(set_words), name='shared counter')
    shl_args = ShareableList(args, name='shared args')

    parallel_time = time.perf_counter()
    for _ in range(cpu_count):  # mp.Pool().map must receive arg
        mp.Process(target=proc).start()

    for process in mp.active_children():
        process.join()
    print('Strict parallel time took '
          f'{time.perf_counter() - parallel_time:.2f}s')

    final = {shl_set[i]: shl_counter[i] for i in range(len(shl_set))}

    final = {i[0]: i[1]
             for i in sorted(
                 list(final.items()),
                 key=lambda x: x[1],
                 reverse=True)
             }

    with open(sys.argv[2], 'w') as stream:
        for k, v in final.items():
            print(f'{k}: {v}', file=stream)

    for obj in (shl_words, shl_set, shl_counter, shl_args):
        obj.shm.close()
        obj.shm.unlink()

    print(f'Multiprocessing took {time.perf_counter() - init:.2f}s')
    print(f'{"pickle" in sys.modules = }')  # Maybe it's imported but unused
    print('Starting "linear"')
    init = time.perf_counter()
    print('Equal?', final == linear())
    print(f'Linear took {time.perf_counter() - init:.2f}s')
    return 0


if __name__ == "__main__":
    quit(main())
