class Node:
    def __init__(self, data) -> None:
        self.data = data
        self.next = None
    
    def __repr__(self):
        return str(self.data)

class LinkedList:
    def __init__(self, *args) -> None:
        self.llist = []
        self.head = None
        self.__counter = -1
        for i in args:
            self.append(i)

    def __repr__(self):
        if not self.llist:
            return 'None'
        return ' -> '.join(str(i.data) for i in self.llist) + ' -> None'

    def __iter__(self):
        return self

    def __next__(self):
        self.__counter += 1
        if self.__counter == len(self.llist):
            self.__counter = -1
            raise StopIteration
        return self.llist[self.__counter]

    def append(self, x: Node):
        self.llist.append(x)
        self.head = x
        if len(self.llist) > 1:
            self.llist[-2].next = x.data
    
    def pop(self):
        if self.llist:    
            aux = self.llist.pop()
            if self.llist:
                self.llist[-1].next = None
                self.head = self.llist[-1].data
            else:
                self.head = None
            return aux
        else:
            raise Exception('List is empty')
    
    def remove(self, x):
        if not self.llist:
            raise Exception('List is empty')
        for i in self.llist:
            if i.data == x:
                aux = self.llist.index(i)
                self.llist.remove(i)
                if aux > 0:
                    self.llist[aux-1].next = self.llist[aux].data
                return
        else:
            print("List doesn't contain this value")
    
    def reverse(self):
        if len(self.llist) > 1:
            self.llist = self.llist[::-1]
            for i in range(len(self.llist)-1):
                self.llist[i].next = self.llist[i+1].data
            self.llist[-1].next = None

    def explain(self):
        print('Node - Data - Next')
        for i in self.llist:
            print(str(self.llist.index(i)).center(4), str(i.data).center(8), str(i.next).center(4))
    
    