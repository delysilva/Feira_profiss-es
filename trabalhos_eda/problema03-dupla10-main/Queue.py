class Node:
    def __init__(self, val):
        self._val = val
        self._next = None
        self._prev = None

    def get_val(self):
        return self._val
    
    def set_val(self, new_val):
        self._val = new_val

    def get_next(self) -> 'Node':
        return self._next

    def set_next(self, new_next: 'Node'):
        self._next = new_next
    
    def get_prev(self) -> 'Node':
        return self._prev

    def set_prev(self, new_prev: 'Node'):
        self._prev = new_prev

    def __str__(self):
        return str(self.get_val())

class Queue:
    def __init__(self):
        self._front = None
        self._back = None
        self._size = 0

    def get_front(self) -> Node:
        return self._front

    def get_back(self) -> Node:
        return self._back

    def set_front(self, new_front: Node):
        self._front = new_front

    def set_back(self, new_back: Node):
        self._back = new_back
    
    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return len(self) == 0

    def queue(self, val):
        new_back = Node(val)
        if (self.get_back() is not None):
            # conectar novo nó
            self.get_back().set_prev(new_back) # conexão back -> new_back
            new_back.set_next(self.get_back()) # conexão back <- new_back
            # atualizar fundo da fila
            self.set_back(new_back)
        else:
            # fila antes vazia
            self.set_front(new_back)
            self.set_back(new_back)
        self._size += 1

    def dequeue(self):
        if len(self) == 0:
            raise IndexError("Fila vazia")
        else:
            to_remove = self.get_front()
            if len(self) == 1:
                self.set_front(None)
                self.set_back(None)
            else:
                new_front = self.get_front().get_prev()
                new_front.set_next(None) # remove conexão front -> new_front
                self.set_front(new_front) # atualiza front
            del to_remove
            self._size -= 1

    def __str__(self) -> str:
        """
        Representa uma fila de n elementos como string da forma 
        a(n-1) -> a(n-2) -> ... -> a(1) -> a(0)
        onde a(n-1) = back e a(0) = front
        """
        outStr = ""
        currNode = self.get_front()
        while currNode is not None:
            outStr = str(currNode) + " " + outStr
            if currNode.get_prev() is not None:
                outStr = "-> " + outStr
            currNode = currNode.get_prev()
        return outStr.strip() # remove espaços em branco ao redor da string
    
    def __repr__(self) -> str:
        return str(self)

    def remove_key(self, key, throw_error:bool = False):
        # remove a primeira ocorrência (a partir da frente da fila) de um determinado valor
        # Complexidade: O(n)
        # Se throw_error está ativado, retorna RuntimeError ao tentar remover chave ausente da fila
        # Se throw_error está desativado, não faz nada nesse caso.
        temp_queue = Queue()
        while (not self.is_empty() and self.get_front().get_val() != key):
            v = self.get_front().get_val()
            self.dequeue()
            temp_queue.queue(v)    
        try:
            # chave encontrada (primeira ocorrência)
            self.dequeue() # chave removida
        except IndexError:
            # chave não encontrada
            if (throw_error):
                raise RuntimeError("Tentativa de remoção de chave inexistente em fila")
            
        while (not self.is_empty()): # esvazia self
            v = self.get_front().get_val()
            self.dequeue()
            temp_queue.queue(v)
        while (not temp_queue.is_empty()): # retorna os valores à fila de self
            v = temp_queue.get_front().get_val()
            temp_queue.dequeue()
            self.queue(v)

    def __getitem__(self, index: int):
        try:
            if (index < 0 or index >= len(self)):
                raise IndexError
            cnt = 0
            temp = Queue()
            while cnt < index:
                v = self.get_front().get_val()
                self.dequeue()
                temp.queue(v)
                cnt += 1
            item = self.get_front().get_val()

            while (not self.is_empty()): # esvazia self
                v = self.get_front().get_val()
                self.dequeue()
                temp.queue(v)
            while (not temp.is_empty()): # retorna os valores à fila de self
                v = temp.get_front().get_val()
                temp.dequeue()
                self.queue(v)
            return item
        except AttributeError: #TODO REMOVE
            print(self)