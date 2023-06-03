# counting sort pra números, com 10 buckets
def countingSort(array, currentIndex, size):
  buckets = 10*[0]
  ans = size*[0]

  for index in range(size):
    digit = int(array[index].getplate()[currentIndex])
    buckets[digit] += 1

  for index in range(1, 10):
    buckets[index] += buckets[index - 1]

  i = size - 1
  while i >= 0:
    aux = int(array[i].getplate()[currentIndex])
    ans[buckets[aux] - 1] = array[i]
    buckets[aux] -= 1
    i -= 1
  
  return ans


# counting sort para letras com 26 buckets
def countingSortLetters(array, currentIndex, size):
  buckets = 26*[0]
  ans = size*[0]

  for index in range(size):
    digit = ord(array[index].getplate()[currentIndex]) - 65
    buckets[digit] += 1

  for index in range(1, 26):
    buckets[index] += buckets[index - 1]

  i = size - 1
  while i >= 0:
    aux = ord(array[i].getplate()[currentIndex]) - 65
    ans[buckets[aux] - 1] = array[i]
    buckets[aux] -= 1
    i -= 1
  
  return ans





def radixSort(array, size):
  # size = len(array) ---->> excluí essa parte pois a estrutura de dados que criei possui a informação do tamanho do vetor que é inserido, ela entra como parâmetro na variável size

# como as placas têm tamanho fixo sempre vamos analisar 7 dígitos, de trás pra frente
  for i in range(6, -1, -1):

# por conta do formato da placa ABC1D23, já sabemos que os índices 0, 1, 2 e 4 são letras e os índices 3 e 5 são números, então no primeiro caso do if, sabemos que vamos tratar de números, e fazemos um counting sort pra esse "dígito" específico sabendo da sua natureza (um efeito disso é a criação dos "buckets" na função counting sort, pra letras criamos 26 buckets, pra número apenas 10)
    if i > 2 and i != 4:
      array = countingSort(array, i, size)

# counting sort pra quando o índice se referir a uma letra
    else:
      array = countingSortLetters(array, i, size)

  return array

