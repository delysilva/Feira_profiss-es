# classe responsável por armazenar as placas em uma espécie de lista, seus únicos métodos são construção, imprimir (não era necessário para o problema, mas usei para certificar que os elementos eram inseridos corretamente), inserção e o de ordenação, que faz uso de um Radix Sort adaptado para o caso específico das placas.
import radixSort
import plates

class cVector:

#função de criação
	def __init__(self):
		self.__database__ = []
		self.__numPlates__ = 0

#função de impressão
	def __str__(self):
		outStr = ''
		for i in range(self.__numPlates__):
			outStr += f' | {self.__database__[i].getplate()} | '
		return outStr

#função de inserção
	def __insert__(self, plate):
		if type(plate) is plates.plate: 
			self.__database__.append(plate)
			self.__numPlates__ += 1
			return True
		else:
			return False

#função de ordenação
	def __sort__(self):
		self.__database__ = radixSort.radixSort(self.__database__, self.__numPlates__)
		return

		
		

