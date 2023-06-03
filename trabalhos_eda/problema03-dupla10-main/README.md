# Problema 3: visualização de superfícies implícitas

## Atalhos de teclado/uso do programa
Foram implementados os modos de visualização 1 e 3. O programa dispõe dos seguintes recursos interativos, realizados através de atalhos no teclado:
1. 'C': realiza o primeiro desenho da superfície, conforme os parâmetros iniciais passados na inicialização da árvore e da instância da classe ```App``` 
criada. 
2. 'D': aumenta em 1 (uma unidade) a profundidade atual (não confundir com profundidade máxima da árvore). 
  Se essa profundidade atual ```<myApp>.program_depth``` ultrapassa a profundidade máxima da árvore, ```<myTree>.max_depth```, essa profundidade
  máxima é atualizada. Isso exige chamar ```QuadTree.build_tree``` para construir as camadas faltantes da árvore.
3. 'F': diminui em 1 (uma unidade) a profundidade atual (não confundir com profundidade máxima da árvore), se ela for maior que 0. 
Do contrário, não faz nada.
4. 'U' (update geral): constrói a árvore novamente e cria o batch associado.
5. 'B' (update do batch): apenas recria o batch novamente.

Após a aplicação de 'D' ou 'F', o update geral 'U' é necessário.

6. 'N': muda para a próxima função, de forma cíclica.
7. 'M': muda para o próximo modo de visualização, de forma cíclica.

## Arquivos auxiliares Vector.py e Queue.py
O código no arquivo ```Vector.py``` implementa a classe ```StaticVector```, um vetor de tamanho fixo, e ```DynamicVector```, vetor de tamanho variável, que são utilizadas ao longo da aplicação. Também apresenta a classe ```Point```, subclasse de ```StaticVector``` com alguns operadores adicionais.

O código no arquivo ```Queue.py``` implementa a classe ```Queue```, isto é, uma fila simples, utilizada sobretudo na construção da árvore/QuadTree e nos métodos de desenho em ```implicit.py```.

## Representação dos retângulos: classe RectNode
Cada retângulo é um objeto da classe ```RectNode```. Ele possui os seguintes atributos:
* ```bottom_left``` e ```top_right``` (```Vector.Point```): são pontos de dimensão 2 que representam respectivamente o canto inferior esquerdo e superior direito do retângulo. Juntos, definem completamente o retângulo.
* ```depth``` (```int```): é a profundidade daquele retângulo na árvore na qual se insere.
* ```subrects``` (```Vector.StaticVector```): é um vetor com 4 elementos, os subretângulos (nós-filhos) do retângulo em questão. São construídos na chamada do método ```RectNode.make_subrects```.

A classe possui alguns métodos auxiliares, como ```RectNode.width``` e ```RectNode.height``` que retorna, respectivamente, a largura e altura do retângulo, evitam repetição de cálculos semelhantes em outros pontos do código e, assim, contribuindo para legibilidade. Ela também possui um ```__repr__```, que permite a representação do objeto e sua transformação para string. O resultado final é sempre da forma "Rect(x, y, z, w)" onde (x, y) é o ponto inferior esquerdo (```self.bottom_left```) e (z, w) é o ponto superior direito (```self.top_right```).

### ```RectNode.make_subrects```
O critério para definição dos subretângulos é a divisão em 4 partes (aproximadamente) iguais. Isto é, dado um retângulo "Rect(x, y, z, w)" temos os seguintes subretângulos como filhos após a chamada do método:
* "Rect(x, y, (x+z)//2, (y+w)//2)" (inferior esquerdo)
* "Rect((x+z)//2, y, z, (y+w)//2)" (inferior direito)
* "Rect(x, (y+w)//2, (x+z)//2, w)" (superior esquerdo)
* "Rect((x+z)//2, (y+w)//2, z, w)" (superior direito)

É claro, sem nenhuma condição de parada a chamada sucessiva de ```RectNode.make_subrects``` sobre os subretângulos gerados pela chamada anterior do mesmo método criaria uma árvore de profundidade ilimitada (excedendo os limites de memória) e com várias camadas repetidas, uma vez que retângulos que representem pixels individuais, ou regiões de 1x2 pixels ou similares não podem ser divididas em novos subretângulos (assumindo, evidentemente, que cada subretângulos deve ser definido por pontos com coordenadas inteiras, isto é, suas dimensões devem ser um número inteiro positivo de pixels). 
Dessa forma, introduzimos a restrição de que ambas as dimensões (largura e altura) do retângulo atual sejam estritamente maiores que 1 pixel, a qual se revela condição necessária e suficiente para que as subdivisões aconteçam sem problemas. 

## O algoritmo: classe QuadTree
### Construção da árvore: classe QuadTree
A árvore de busca utilizada é uma Quad-Tree, isto é, uma árvore em cada nó possui exatamente 4 filhos. Cada árvore possui os seguintes atributos:
* ```max_depth``` (```int```): profundidade máxima construída da árvore.
* ```root``` (```RectNode```): nó raiz, representa o retângulo formado por toda a tela.
* ```rect_queue```(```Queue.Queue```): fila contendo os nós folha atual, isto é, aqueles na profundidade máxima da árvore. Essa fila será útil na construção de novas camadas da árvore.

O construtor da classe (```QuadTree.__init__```) recebe a largura e altura da janela e profundidade máxima da árvore. Ele cria o nó raiz e já coloca-o na fila ```rect_queue```. **A raiz é sempre considerada como um nó de profundidade 0**. 

Para a construção da árvore em si, chama-se o método (```QuadTree.build_tree```). Ele constrói todas as camadas da árvore, da seguinte maneira: se queremos construir o nível $n+1$, temos
* No início da chamada do método, ```self.rect_queue``` contém os nós folha, isto é, os nós na profundidade $n$. Está é nossa invariante ao longo de todo o programa: apenas durante a execução desse método que essa condição é quebrada.
* Enquanto a fila não está vazia, tomamos o primeiro nó $r$:  se sua profundidade é maior ou igual à nova profundidade máxima da árvore (na prática, ele nunca será estritamente maior, no máximo igual) segue que já construímos o nível $n+1$, e finalizamos a execução.
* Do contrário, removemos esse nó da fila e chamamos ```r.make_subrects()``` para criar seus subretângulos. Um a um, adicionamos esse subretângulos à fila, se não forem ```None```. 

Dessa forma, nota-se que a construção é feita de forma análoga a uma "Breadth-First-Search"/BFS/Busca em largura em uma árvore. 
#### Teorema: esse algoritmo de construção da árvore é $\Theta(4^d)$ onde $d$ é a profundidade até a qual se quer construir.
Prova: temos que cada nó de profundidade $d' \leq d$ é visitado exatamente uma vez no algoritmo acima, pois logo após ser visitado ou a execução do método termina ou o nó é retirado da fila. Como existem $1 + 4 + ... + 4^d = \dfrac{4^{d+1} - 1}{3} \in \Theta(4^d)$ nós de profundidade menor ou igual a $d$, considerando a profundidade da raiz como $0$, e notando que as operações feitas com cada nó (criar seus subretângulos/nós filhos com ```RectNode.make_subrects```, retirá-lo da fila, etc) são todas $O(1)$, concluímos que o algoritmo é $\Theta(4^d)$.

#### Corolário: se a tela é quadrada de tamanho $n$ pixels, então o algoritmo de construção de toda a árvore, até a profundidade máxima (onde cada nó folha representa um único pixel) é $O(n^2)$
Prova: as dimensões de cada retângulos diminuem pela metade a cada profundidade descida. Como devemos ter que as medidas dos subretângulos representados pelos nós folhas são de pelo menos 1 pixel em cada direção, $d \leq log_2(n)$. Portanto são visitados no máximo
$1 + 4 + ... + 4^{\lfloor log_2(n) \rfloor} \leq \dfrac{4n^2 - 1}{3} \in O(n^2)$
o que mostra que o algoritmo é $O(n^2)$ no pior caso (de máxima profundidade).

### O algoritmo: montando o batch e desenhando a curva.
Três métodos são responsáveis por modos diferentes de visualização de uma determinada função. Esses métodos não retornam nada, mas possuem como efeito a (re)criação do atributo ```self.batch``` (do tipo ```pyglet.graphics.Batch```) que contém/referencia todos os retângulos a serem desenhados (objetos da classe ```pyglet.shapes.Rectangle``` ou, no caso do modo 3 de visualização, ```pyglet.shapes.BorderedRectangle```).

De fato, a parte de desenho e atualização da tela é toda gerenciada pela classe ```App``` em ```app.py``` para propósitos de modularização e conforme o princípio de responsabilidade única. Enfim, temos os seguintes 3 métodos para criação do batch:
* ```QuadTree.make_batch_curve``` (responsável pelo modo de visualização 1): possui como parâmetros a função ```f```, a cor que deve ser utilizada para pintar o traçado da curva de nível $f(x,y)=0$, ```root_color``` (passada como tupla de 3 inteiros no formato RGB) e ```depth```, um inteiro que indica a profundidade a ser utilizada na criação do batch;
* ```QuadTree.make_batch_colored``` (responsável pelo modo de visualização 2): possui como parâmetros a função ```f```, a cor da região onde $f(x,y)>0$ (```positive_color```), a cor da região onde $f(x,y)<0$ (```negative_color```), a cor do traçado da curva de nível $f(x,y)=0$ (```border_color```), e a profundidade de referência para a criação do batch. Novamente, todas as cores são passadas como triplas de 3 inteiros entre 0 e 255, no formato RGB.
* ```QuadTree.make_batch_border``` (responsável pelo modo de visualização 3): esse modo de visualização gera retângulos com borda, e por isso o método, além de receber a função ```f```, recebe mais 4 argumentos: ```border_width``` (a largura da borda em pixels), ```inside_color``` (a cor da parte interna do retângulo), ```border_color``` (a cor da borda) e ```depth```, a profundidade de referência para a criação do batch. 

O algoritmo é análogo para os 3 casos e, com isso, explicamos apenas a implementação observada no primeiro método, ```QuadTree.make_batch_curve```.
0. Assumimos que ```2 <= depth <= self.max_depth```, isto é, que a profundidade é pelo menos 2 e é menor que a profundidade máxima construída da árvore, que também deve ser de pelo menos 2.  
1. Primeiramente, inicializamos o batch e a lista de formas a serem desenhadas, ```self.shapeList```. Como a quantidade de formas a serem desenhadas é desconhecida antes da execução, ```self.shapeList``` é um vetor dinâmico, objeto da classe ```Vector.DynamicVector```.
2. Depois, utilizamos o método ```QuadTree.get_nodes_at_depth``` para recuperar uma fila com os retângulos de profundidade 2 na árvore: é neles que começamos o algoritmo, para evitar que a análise de sinais a seguir falhe muito cedo. Essa fila é a fila de nós a serem analisados (```waiting_nodes```), em seu estado inicial.
3. Enquanto há nós a serem analisados (```not waiting_nodes.is_empty()```), tomamos o nó da frente da fila e removemos ele (dequeue).
	* Caso 1: se o valor da função tem o mesmo sinal nos 4 vértices do retângulo representado por aquele nó, pulamos para a próxima iteração sem fazer nada. Isso garante que nenhum nó de sua subárvore será analisado, pois ele já foi removido da fila de processamento.
	* Caso 2: o valor da função nos 4 vértices apresenta sinais distintos e a profundidade desse nó é maior ou igual a ```depth```: adicionamos esse retângulo ao batch com a cor apropriada, para ser desenhado no futuro.
	* Caso 3: o valor da função nos 4 vértices apresenta sinais distintos e a profundidade desse nós é estritamente menor que ```depth```: adicionamos seus sub-retângulos/nós-filhos à fila.

## Gerenciamento da interface da aplicação: classe App em app.py
Cada objeto da classe ```App``` representa uma instância da aplicação com diferentes parâmetros/configurações. De fato, no construtor ```App.__init__``` são passados os seguintes argumentos:
* ```window``` (do tipo ```pyglet.window.Window```): janela da aplicação
* ```tree``` (do tipo ```QuadTree```): QuadTree a ser utilizada
* ```available_functions``` (do tipo ```Vector.StaticVector```): vetor com as funções disponíveis 
* ```root_color```, ```positive_color```, ```negative_color```, ```inside_color```, ```border_color``` (tuplas no formato RGB): são as cores a serem utilizadas. A primeira é a cor do traçado da curva de nível $f(x,y)=0$ no modo de visualização 1 e 2. A segunda e terceira são respectivamente a cor da região positiva e a cor da região negativa, no modo de visualização 2. A quarta e a quinta são respectivamente a cor da parte interna e da borda dos retângulos desenhados no modo de visualização 3.
* ```border_width``` (```int```): largura da borda dos retângulos no modo de visualização 3, em pixels.

Por padrão, a função inicial a ser escolhida e aquela que é mostrada na inicialização do desenho é o primeiro elemento de ```available_functions```. 

### Desenho da curva: ```App.gameloop```
Essa função é responsável pelo gerenciamento dos eventos que ocorrem na aplicação (teclas apertadas, batch redesenhado, etc.): isto é, é o loop principal. Há um par de "flags" (valores booleanos) muito importantes para a manutenção da sincronização entre tela (parte gráfica) e os dados em si (valores de parâmetros como profundidade, função escolhida e modo de visualização): 
* ```updated_batch```: sinaliza se o batch atual (```<myApp>.tree.batch```) corresponde ao batch esperado, dados os valores atuais de parâmetros como a profundidade de desenho, a função escolhida e o modo de visualização.
* ```updated_tree```: sinaliza se a árvore em si corresponde à árvore esperadam, dada a profundidade atual ```<myApp>.program_depth``` escolhida pelo usuário. Se ```<myApp>.program_depth <= <myApp>.tree.max_depth```, a árvore não precisa ser atualizada, pois todos os nós até aquela profundidade atual já foram construídos. O caso contrário, no entanto, que ocorre quando o usário aperta ```D``` um número de vezes suficiente para que tenhamos ```<myApp>.program_depth > <myApp>.tree.max_depth```, leva à necessidade de construir novos níveis na árvore e, portanto, representa uma falta de sincronização entre o estado atual da árvore e o estado exigido pelo programa.

Essas flags gerenciam o processamento de eventos de desenho: o batch só será desenhado/redesenhado se tanto ```updated_batch == True``` quanto ```updated_tree == True```.  

#### Funcionalidades implementadas (atalhos de teclado)
Por fim, essa função implementa a função das diferentes teclas que podem ser utilizadas para customizar a visualização, e que foram descritas na primeira seção, "Atalhos de teclado/uso do programa".

### Geração de texto e interface
A aplicação pode apresentar duas caixas de texto contendo informações: a primeira, permanente, informa o estado atual de parâmetros como profundidade, função escolhida (representada apenas pelo seu índice no vetor de funções disponíveis ```<myApp>.available_functions```) e modo de visualização (1, 2, 3). Sua geração é implementada no método ```App.update_info_label```.

A segunda é gerada conforme ocorre uma modificação nesses parâmetros, e informa se um update do batch (apertar a tecla ```B```) é necessário (ocorre quando ```<myApp>.update_batch == False and <myApp>.updated_tree == True```) ou se um update geral, da árvore e do batch de desenho (apertar a tecla ```U```) é necessário (ocorre quando ```<myApp>.updated_tree == False```). Essa funcionalidade é implementada no método ```App.generate_warning_if_outdated```.

## main.py e configurações recomendadas
O arquivo ```main.py``` representa o programa principal. Nele são estabelecidos alguns valores padrão para certos parâmetros: 
* O tamanho da janela é fixado como 800x800, que foi escolhido pelo equilíbrio entre boa visualização e boa precisão de desenho.
* As cores também são fixadas.
* Construímos a árvore com uma profundidade **inicial** de 7.
Esses parâmetros não necessariamente precisavam de valores fixos, mas isso foi feito para simplificar o uso da aplicação, devido sobretudo à sua baixa relevância/baixo impacto na visualização. 
Por fim, é em ```main.py``` que definimos as funções escolhidas. Apresentamos no estado atual 5 funções disponíves:
* Círculo de centro (400, 400) e raio 100
* Quadrado de centro (400, 400) e lado 200.
* Curva senóide $f(x,y) = 200*\sin(\frac{x}{100}) + 400 - y$ 
* Cardióide (deslocado e com tamanho aumentado para melhor visualização)
* Topologist's sine curve (ver [1])

A expressão de cada função foi escolhida pensando em resoluções 800x800, o que explica a abordagem de resolução fixa escolhida. A última função foi especificamente escolhida para mostrar como funções com variações muito rápidas em regiões muitas pequenas do $\mathbb{R}^2$ podem levar a grande imprecisão no desenho geral.

### Profundidade máxima recomendada
Recomendamos que a visualização seja feita com uma **profundidade menor ou igual a 9**, uma vez que escolher uma profundidade de 10 ou maior implica em um grau de refinamento muito preciso (precisão da ordem de um único pixel) e, com isso, no estado atual de otimização dessa aplicação, pode levar vários segundos para renderização. 

## Possíveis otimizações
Seria possível a escolha de uma implementação que constrói a árvore "sob demanda": isto é, não constrói as subárvores de nós que representam retângulos de profundidade maior ou igual a 2 e onde a função apresenta o mesmo sinal em todos os vértices.

Embora isso fosse, possivelmente, acelerar a construção da árvore, isso vincula de forma inseparável árvore e função e, com isso, exigiria que para cada função disponível fosse criada uma árvore diferente. Ainda que a aplicação disponibilize apenas poucas funções atualmente, pensando no caso de aplicações maiores, que disponibilizassem $10^3$ ou $10^4$ funções diferentes, optamos por não utilizar essa abordagem em vista dos limites de memória.

## Referências
[1] https://en.wikipedia.org/wiki/Topologist%27s_sine_curve
