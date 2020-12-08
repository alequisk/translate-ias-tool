# TRANSLATE IAS TOOL

Esse script foi feito com intuito de facilitar a escrita de código para IAS, computador eletrônico feito por Von Neumman.

Para facilitar a conversão de texto para instruções, devemos seguir algumas convenções que admitimos que esteja colocada em prática na escrita de um código IAS:

- Cada linha deverá conter 2 (duas) instruções separadas por um espaço. Não deverá haver qualquer outro espaço entre eles. Caso necessário, utilize o "_" (underline) para fazer o papel de espaço no código.
- Para indicar espaços reservados da memória, você deve usar o prefixo **VAR** antes de "declará-las" e no restante a palavra que você deseja nomear. A segunda instrução deverá ser 
- Caso você tenha que referenciar um endereço de memória M(x), por exemplo, **LOAD M(X)** você deve usar o comando indicado para esse procedimento (nesse caso o comando se chama *LOAD*) e para indicar o espaço da memória deveremos colocar seu nome de acordo com o já pre-estabelecido no segundo ponto precedido um sinal de igualdade (=). Logo, teremos o comando **LOAD=VAR_NUMERO**
- Caso você queira indicar o final da execução do programa use o comando **ABORT_PROGRAM** que ele irá fazer que o IAS preencha o espaço uma instrução **00 000**.
- Os endereços atribuídos para o conversor são dinâmicos. Então, caso você queira fazer um JUMP para uma parte do código deve-se atrubuir uma linha em branco para a criação de um LABEL que identificará aquele trecho. Antes do bloco que você queira identificar, atribua o nome com um prefixo **LAB**. Exemplo:
```
JUMP_NOIF_LEFT=LAB_SOMA ABORT_PROGRAM
...
...
LAB_SOMA
LOAD=VAR_NUMERO_1 ADD=VAR_NUMERO_2
```
- Existem apenas 3 (três) comandos que você não precisa atribuir o sinal de igualdade: LOAD_MQ, RSH, LSH. Todos eles já são, por padrão, atribuídos **000** aos endereço que se referenciam.
- Os valores que você define para criação de espaço de memória serão convertidos para hexadecimal(uma vez que o simulador recebe entradas hexadecimais para facilitação de escrita de instruções), então não é preciso se preocupar em conversões ao definir valores.
- Todas os espaços de memória que são usadas dentro do código **deverão ser declaradas**, com preferência, no final do código. Comandos para parada de execução do programa também são recomendadas antes da declaração delas, porém, não são obrigatórias.

# LISTA DE COMANDOS DISPONÍVEIS

LOAD_MQ | LOAD_MQ_M | STOR | LOAD | LOAD_NEG | LOAD_MOD | LOAD_NEG_MOD | JUMP_NOIF_LEFT | JUMP_NOIF_RIGHT | JUMP_IF_LEFT | JUMP_IF_RIGHT | ADD | ADD_MOD | SUB | SUB_MOD | MUL | DIV | LSH |RSH | STOR_REPL_LEFT | STOR_REPL_RIGHT | ABORT_PROGRAM

Para reportar bugs sobre o script ou ajudar a melhorá-lo, pode-se fazer um pull request caso tenha uma solução já pronta ou abrir issues para apenas reportá-los.