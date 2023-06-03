# Esse é o arquivo main
import platesDatabase
import sys
import plates
import time


#==========================================================================#
if __name__ == '__main__':

# aqui começamos a contar o tempo de execução do nosso programa
	
	begin = time.time()
	
#===========================================================================#
# aqui criamos um objeto da classe c.Vector para armazenar as placas FIZ COM QUE ESSE TIPO DE VETOR SÓ ACEITE OBJETOS DO TIPO "PLATE" (QUE SÃO AS PLACAS)
	database = platesDatabase.cVector()


#===========================================================================#
# ABORDAGEM ANTIGA: fiz uma pequena adaptação para não precisar editar o código para colocar o nome do arquivo toda hora, basta apenas inserir o nome do arquivo, exemplo: "PIVs-1000000.piv"

	#nome_do_arquivo = input("Insira o nome do arquivo:")
	
# ABORDAGEM NOVA: o arquivo vem da linha de comando

	nome_do_arquivo = sys.argv[1]

#===========================================================================#
#aqui abrimos o arquivo que foi passado como referência na linha de comando, criamos o objeto placa e inserimos as placas em database, que é um objeto do tipo cVector(só recebe placas).

	with open(f'{nome_do_arquivo}', 'r') as file:
		for license_plate in file:
			car_plate = plates.plate(license_plate)
			database.__insert__(car_plate)

#===========================================================================#
#chamamos a função de ordenação da classe cVector para ordenar as placas usando o Radix Sort adaptado

	database.__sort__()

#===========================================================================#
#criamos um novo arquivo do tipo .txt com o nome "sorted_plates" onde serão armazenadas as placas em ordem lexicográfica

	with open('sorted_plates.txt', 'w') as file:
		for plate in database.__database__:
			file.write(str(plate.getplate()))
#==========================================================================#
# paramos de contar o tempo de execução e logo em seguida imprimimos ele
	end = time.time()
	print(end - begin)
#==========================================================================#
