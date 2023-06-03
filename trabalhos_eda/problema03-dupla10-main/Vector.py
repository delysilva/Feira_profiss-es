class StaticVector:
    def __init__(self,
                maxsize: int):
        self.__allocated = maxsize
        self.__size = 0
        self.v = [0]*maxsize

    def __len__(self) -> int:
        return self.__size

    def __getitem__(self,
                    index: int):
        """
        Retorna o elemento naquele posição, se dentro dos limites do vetor. 
        Do contrário, gera IndexError.
        Complexidade: O(1)
        """
        if (0 <= index and index < self.__size):
            return self.v[index]
        else:
            raise IndexError("Fora dos limites do vetor")
        
    def __setitem__(self,
                    index: int,
                    new_value):
        """
        Atribui um novo valor ao elemento naquele índice (se dentro dos limites do vetor).
        Do contrário, gera IndexError.
        Complexidade: O(1)
        """
        if (0 <= index and index < self.__size):
            self.v[index] = new_value
        else:
            raise IndexError("Fora dos limites do vetor")

    def __repr__(self) -> str:
        outStr = "["    
        for i in range(self.__allocated):
            outStr += str(self.v[i])
            if (i < self.__allocated - 1):
                outStr += ", "
        outStr += "]"
        return outStr
        

    def __str__(self) -> str:
        outStr = "["
        for i in range(len(self)):
            outStr += str(self[i])
            if (i < len(self) - 1):
                outStr += ", "
        outStr += "]"
        return outStr

    def __eq__(self, other: 'StaticVector') -> bool:
        for i in range(len(self)):
            if (self.v[i] != other.v[i]):
                return False
        return True
        

    def append(self, 
                item):
        """
        Se o vetor não está cheio, adiciona aquele elemento no final
        Do contrário, gera IndexError.
        Complexidade: O(1)
        """
        if (self.__size < self.__allocated):
            self.v[self.__size] = item
            self.__size += 1
        else:
            raise IndexError("Limite de elementos do vetor alcançado")
        
    def pop(self, 
            index = None):
        """
        Remove o elemento naquela posição (se dentro dos limites do vetor)
        e retorna o elemento.
        Do contrário, gera IndexError.
        Complexidade: O(n)
        """
        if (index is None):
            index = self.__size - 1
        if (0 <= index and index < self.__size):
            key = self.v[index]
            self.v[index] = 0 # clear value
            for i in range(index, self.__size - 1):
                self.v[i] = self.v[i + 1] # left shift elements
            self.v[self.__size - 1] = 0 # clear last element
            self.__size -= 1
            return key
        else:
            raise IndexError("Fora dos limites do vetor")
    
    def prefixsum(self):
        """
        Substitui v[i] pela soma parcial v[0] + ... + v[i].
        Assume que o operator + está implementado para aquele tipo.
        Complexidade: O(n)
        """
        for i in range(1, self.__size):
            self.v[i] += self.v[i-1]

    def remove(self, 
                key) -> int:
        """
        Remove todos os elementos que comparam iguais a 'key'.
        Retorna a quantidade de elementos removidos.
        Complexidade: O(n)
        """
        bitmask = StaticVector(self.__size)
        prefix_sum_bitmask = StaticVector(self.__size)
        for i in range(self.__size):
            if (self.v[i] == key):
                bitmask.append(1)
                prefix_sum_bitmask.append(1)
            else:
                bitmask.append(0)
                prefix_sum_bitmask.append(0)
        prefix_sum_bitmask.prefixsum()
        removed = prefix_sum_bitmask.v[prefix_sum_bitmask.__size - 1]
        # remoção e deslocamento dos elementos
        for i in range(self.__size):
            if (bitmask.v[i] == 0 and prefix_sum_bitmask.v[i] != 0):
                # não será removido nem fixado
                self.v[i - prefix_sum_bitmask.v[i]] = self.v[i]
                self.v[i] = 0
            elif (bitmask.v[i] == 1):
                # deve ser removido
                self.v[i] = 0
        # atualizando tamanho
        self.__size -= removed
        return removed
        


class DynamicVector(StaticVector):
    def __init__(self,
                initial_size = 1):
        StaticVector.__init__(self, initial_size)

    # override append
    def append(self, 
                item):
        """
        Realiza append normal se há espaços sobrando, do contrário realiza realocação.
        Complexidade:
            O(1) se não houver realocação
            O(n) se houver realocação de memória
        Em média, adicionar K elementos é O(K) independente do tamanho inicial.
        """

        # for the explanation on the prefix "_StaticVector", note the inheritance from the StaticVector class and see
        # see https://stackoverflow.com/questions/1301346/what-is-the-meaning-of-single-and-double-underscore-before-an-object-name for more details
        if (self._StaticVector__size < self._StaticVector__allocated):
            StaticVector.append(self, item)
        else:
            # nova alocação do dobro de espaço
            # O(n) cópia para temporário
            temp = StaticVector(self._StaticVector__size)
            for i in range(self._StaticVector__size):
                temp.append(self.v[i])
            # nova alocação
            self.v = [0]*(2*self._StaticVector__allocated)
            self._StaticVector__allocated = 2*self._StaticVector__allocated
            for i in range(self._StaticVector__size):
                self.v[i] = temp.v[i]
            del temp
            self.v[self._StaticVector__size] = item
            self._StaticVector__size += 1

class Point(StaticVector):
    def __init__(self, *args):
        StaticVector.__init__(self, len(args))
        for x in args:
            self.append(x)
        self.dimension = StaticVector.__len__(self)

    def __add__(self, other: 'Point') -> 'Point':
        assert self.dimension == other.dimension
        res = Point(*([0]*self.dimension))
        for i in range(self.dimension):
            res[i] = self[i] + other[i]
        return res

    def __mul__(self, scalar: float) -> 'Point':
        res = Point(*([0]*self.dimension))
        for i in range(self.dimension):
            res[i] = scalar*self[i]
        return res

    def __sub__(self, other: 'Point') -> 'Point':
        return self + (-1)*other
        
