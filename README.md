# Translate Set Instruction IAS-Tool

Esse script foi feito com intuito de facilitar a escrita de instruções para o computador IAS dentro da disciplina de Introdução a Arquitetura de Computadores.

Com esse script, você pode usar as instruções que estão no set de instruções do IAS sem precisar fazer a conversão/escrita do opcode ou valor em hexadecimal, apenas
usando instruções simples e de facil leitura definidas no script, para que seja feita toda a conversão e gerado um arquivo ou uma saída com valores convertidos e prontos
para serem colocados na memória do IAS.

---
## Requisitos

Para que você consiga executar esse script, é necessário `python` na versão 3 ou superior.

---
## Como usar

Você deve criar um arquivo onde você escreverá seu código e abrir o terminal de comandos (cmd ou bash) na pasta onde você baixou esse script e usar o python3 para executá-lo:

Exemplo com arquivo `codigo.txt` na mesma pasta:

```bash
python3 main.py codigo.txt
```

Se você quiser gerar um arquivo com a saída traduzida para IAS, vocẽ poderá adicionar mais um argumento na linha de comando para que seja o nome do arquivo que vai conter os códigos traduzidos. Exemplo:

```bash
python3 main.py codigo.txt saida.txt
```

Por padrão, o projeto já vem com um arquivo `code.txt` na mesma pasta que contém um programa para calcular o fatorial do número 3, onde você pode modificá-lo e escrever suas próprias instruções. Então para traduzir apenas use no terminal:
```bash
python3 main.py code.txt
```

Os códigos gerados podem ser simulador usando o ___simulador de IAS da Unicamp___ nesse [link](https://www.ic.unicamp.br/~edson/disciplinas/mc404/2017-2s/abef/IAS-sim/).


---
## Como escrever instruções para o script
> Os códigos escritos são *case-insensitive*, ou seja, não há diferenciação de minúscula ou maiúscula. Os espaços também são totalmente desconsiderados, sendo apenas considerados as instruções por linhas e o demilitador de instruções (`,`).

> Para facilitar a conversão de texto para as instruções do IAS, devemos seguir algumas convenções que admitimos que esteja colocada em prática na escrita de um código para essa ferramenta funcionar com êxito na tradução:

- Cada linha deverá conter 2 (duas) instruções separadas por uma virgula (`,`).

  Exemplo de uma linha de instruções escritas para IAS-Tool.
  
  ```
    sub=var2,  stor=var_result
  ```

- Para indicar espaços reservados da memória, você deve usar o prefixo `var` seguido por um nome que desejar sem espaço (devendo estar junto ao prefixo `var`) e atribuir um valor com o simbolo `='valor'`.
  > Uma variável/espaço na memória é declarada apenas uma vez  por linha, não podendo criar duas variáveis por linha ou adicionar uma instrução ao lado da variável.
  
  > O valor que desejar atribuir deverá ser um valor em decimal, e o script se encarrega de converté-lo para hexadecimal.

  Exemplo de declarações:
  
  ```
  var0 = 1
  var_variavel = 3
  varnomedaminhavariavel = 7
  var_com_nome_legal = 12
  ```
- Para instruções que carregam esses valores de espaços/variáveis da memória, devemos usar o sinal de igualdade (`=`) seguido do nome desse espaço que você criou.

  Exemplo de instruções que carregam valores da memória.
  ```
  load=var0,                  sub=var_varivel
  add=varnomedaminhavariavel, stor=var_com_nome_legal
  ```

- Algumas instruções não precisam que seja passados os endereços para eles, que é o caso do `LSH` (*Left shift*), `RSH` (*Right shift*), `LOAD MQ` (*load AC to MQ*) e `ABORT` (*Faz o programa parar colocando a instrução 00 000*), então nesses casos você não precisa usar a igualdade (`=`) na instrução.

  Exemplos:
  ```
  load=var0, rsh
  loadmq,    abort
  ```

- Caso você queira indicar o final da execução do programa use o comando `ABORT` que ele irá fazer que o IAS-Tool preencha no espaço uma instrução *00 000*.

- Os endereços atribuídos para o script são dinâmicos, então caso você queira fazer um `JUMP` para uma parte do código, deve-se criar uma linha antes da linha alvo e  criar uma *LABEL* que identificará a linha que voê deseja pular. Para criar essa label, você deve usar o prefixo `LAB` e o nome da label, sem espaços do prefixo com o nome.
  
  Exemplo onde meu fluxo deve pular para a instrução `LOAD=VAR_A1`:
  ```
  jumpl=lab_soma, abort
  ...
  ...
  lab_soma
  load=var_a1,    add=var_a2
  stor=var_a1,    sub=var3
  ```

- Todos os espaços de memória que são usados dentro do código **deverão ser declaradas**, com preferência, no final do código. Comandos para parada de execução do programa também são recomendadas antes da declaração delas, porém, não são obrigatórias.

---
## LISTA DE COMANDOS DISPONÍVEIS

> Instruções que acessam a memória declarada, ou seja, `M(x)`.

+ ***STOR*** - `STOR M(x)`

  Salva o valor em `AC` na memória declarada.

+ ***LOADMMQ*** - `LOAD MQ M(x)`
  
  Carrega o valor da memória declarada para o `MQ`.

+ ***LOAD*** - `LOAD M(x)`

  Carrega o valor da memória declarada para `AC`.

+ ***LOADN*** - `LOAD -M(x)`

  Carrega o valor negativo da memória declarada para `AC`.

+ ***LOADBAS*** - `LOAD |M(x)|`
  
  Carrega o valor absoluto da memória declarada para `AC`.

+ ***LOADNABS*** - `LOAD -|M(x)|`

  Carrega o negativo do valor absoluto da memória declarada para `AC`.

+ ***ADD*** - `ADD M(x)`

  Soma o valor do `AC` com o valor na memória declarada. Guarda o resultado em `AC`.

+ ***ADDABS*** - `ADD |M(x)|`

  Soma o valor do `AC` com o valor absoluto na memória declarada. Guarda o resultado em `AC`.

+ ***SUB*** - `SUB M(x)`

  Subtrai o valor do `AC` com o valor na memória declarada. Guarda o resultado em `AC`.

+ ***SUB_MOD*** - `SUB |M(x)|`

  Subtrai o valor do `AC` com o valor absoluto na memória declarada. Guarda o resultado em `AC`.

+ ***MUL*** - `MUL M(x)`

  Multiplica a memória declarada com `MQ`, salva o resultado em `MQ` e o valor que ultrapassou o capacidade de `MQ` em `AC`. 

+ ***DIV*** - `DIV M(x)`

  Divide o conteúdo de `AC` pela memória declarada. Coloca o quociente em `MQ` e o resto no `AC`.

+ ***STORREPLL*** - `STOR M(x, 8:19)`

  Troca o endereço da instrução da esquerda da memória declarada pelos os 12 bits mais significativos de `AC`.

+ ***STORREPLR*** - `STOR M(x, 28:39)`

  Troca o endereço da instrução da direita da memória declarada pelos os 12 bits mais significativos de `AC`.

> Instruções que acessam a uma linha específica da memória no programa, ou seja, que utilizam labels.

+ ***JUMPIL*** - `JUMP+ M(0:19)`

  Faz um pulo condicional para a instrução da esquerda da linha seguinte ao label se o valor em `AC` for não-negativo (maior ou igual a 0).
  
  Exemplo:

  ```
  jumpil=lab_soma, abort
  ...
  lab_soma
  load=var_1, add=var_2 <- executa a instrução da esquerda (load=var_1).
  ```

+ ***JUMPIR*** - `JUMP+ M(20:39)`

  Faz um pulo condicional para a instrução da direita da linha seguinte ao label se o valor em `AC` for não-negativo (maior ou igual a 0).
  
  Exemplo:

  ```
  jumpir=lab_soma, abort
  ...
  lab_soma
  load=var_1, add=var_2 <- executa a instrução da direita (add=var_2).
  ```

+ ***JUMPL*** - `JUMP M(0:19)`

  Faz um pulo incondicional para a instrução da esquerda da linha seguinte ao label.
  
  Exemplo:

  ```
  jumpl=lab_soma, abort
  ...
  lab_soma
  load=var_1, add=var_2 <- executa a instrução da esquerda (load=var_1).
  ```
+ ***JUMPR*** - `JUMP M(20:39)`
  
  Faz um pulo incondicional para a instrução da direita da linha seguinte ao label.
  
  Exemplo:

  ```
  jumpr=lab_soma, abort
  ...
  lab_soma
  load=var_1, add=var_2 <- executa a instrução da direita (add=var_2).

> Instruções que não precisam de atribuidor (`=`).

+ ***LOADMQ*** - `LOAD MQ`

  Move o conteúdo de `MQ` para `AC`.

+ ***LSH*** - `LSH`

  Realiza um *Left shift* em `AC` (Multiplica `AC` por 2).

+ ***RSH*** - `RSH`

  Realiza um *Right shift* em `AC` (Divide `AC` por 2).

+ ***ABORT*** - `ABORT`

  Preenche a instrução com *00 000*, onde faz com que o programa pare, uma vez que o opcode *00* não existe.

Para reportar bugs sobre o script ou ajudar a melhorá-lo, pode-se fazer um pull request caso tenha uma solução já pronta ou abrir issues para apenas reportá-los.