import random

def get_list() -> list:
    x = list(range(1001))
    random.shuffle(x)
    return x

def mine(x: list):
    for i in range(len(x)-1):
        for j in range(len(x)-1, i, -1):
            if x[i] > x[j]:
                x[i], x[j] = x[j], x[i]

def bubble(x: list):
    for i in range(len(x)-1):
        for j in range(len(x)-1, i, -1):
            if x[j] < x[j-1]:
                x[j], x[j-1] = x[j-1], x[j]

def insertion(x: list):
    for j in range(1, len(x)):
        key = x[j]
        i = j-1
        while i >= 0 and x[i] > key:
            x[i+1] = x[i]
            i -= 1
        x[i+1] = key

def selection(x: list):
    for i in range(len(x)-2):
        min = i
        for j in range(i+1, len(x)):
            if x[j] < x[min]:
                min = j
        if x[i] != x[min]:
            x[i], x[min] = x[min], x[i]

def fatorial(x: int): # math.factorial()
    if x == 0:
        return 1
    return x * fatorial(x-1)

def fibo(x: int):
    assert x >= 0
    if x in [1,0]:
        return 1
    return fibo(x-1) + fibo(x-2)

def it_fibo(x: int):
    a = b = c = 1
    for i in range(x+2):
        if i <= 2:
            continue
        c = a + b
        a = b
        b = c
    return c

def quicksort(arr):
    _quicksort(arr, 0, len(arr)-1)

def _partition(arr, low, high):
    i = (low-1)         # índice do menor elemento
    pivot = arr[high]     
 
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
 
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return (i+1)

 
def _quicksort(arr, low, high):
    if len(arr) == 1:
        return arr

    if low < high:
        pi = _partition(arr, low, high)
        _quicksort(arr, low, pi-1)
        _quicksort(arr, pi+1, high)

def mergeSort(arr):
    if len(arr) > 1:
        mid = len(arr)//2

        L = arr[:mid]
        R = arr[mid:]
  
        mergeSort(L)
        mergeSort(R)
  
        i = j = k = 0
  
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
  
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
  
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def buscabin(x, arr):
    p, c, r = 0, 0, len(arr)
    return _buscabin(x, arr, p, r, c)

def _buscabin(x, v, p, r, c):
    c += 1
    if p > r:
        return -1
    else:
        q = (p + r)//2
        if v[q] == x:
            return v[q], c
        else:
            if v[q] < x:
                return _buscabin(x, v, q+1, r, c)
            else:
                return _buscabin(x, v, p, q-1, c)