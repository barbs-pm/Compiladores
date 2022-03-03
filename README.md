## Trabalho Prático - Compilador

**Objetivo:** Implementar um compilador de código usando análise léxica sintática e geração do código intermediário  <br>

**Funcionamento:** 
O código deverá ser capaz de ler o arquivo do código (codigo.txt) e analisar cada caractere em busca de erros, bem como também verifica as estruturas formadas por esses caracteres. Utilizamos de uma ferramenta externa chamada Gold Parser para a criação da tabela LALR, utilizada para a verificação sintática, a partir da nossa linguagem base, a fim de economizar trabalho, e evitar erros.

**Saída do programa:**
<br>
Ao executar o programa, o mesmo retorna a fita de saída, erros de código e sua respectiva linha. Exemplo:
- Ao compilar corretamente:
```
Fita de saída da etapa léxica:
['DEF', 'S1', ';', 'DEF', 'S1', '#', 'S2', ';', 'S1', '#', 'S2', '+', 'S2', '~', 'S1', '/', 'S1', '-', 'S2', ';', 'DEF', 'S1', '#', 'S2', ';', 'S1', '#', 'S1', '+', 'S1', ';', 'ENQUANTO', 'S1', 'MAIOR', 'S2', '{', 'DEF', 'S1', '#', 'S2', ';', 'SE', 'S2', 'MENOR', 'S2', '{', 'S1', '#', 'S2', ';', '}', '}', 'DEF', 'S1', ';', 'S1', '#', 'S2', ';', 'SE', 'S1', 'MENOR', 'S2', '{', 'DEF', 'S1', '#', 'S2', ';', '}', 'EOF']
Compilado com sucesso!
```

- Ao compilar código com um erro:
```
Fita de saída da etapa léxica:
['DEF', 'S1', ';', 'DEF', 'S1', '#', 'S2', ';', 'S1', '#', 'S2', '+', 'S2', '~', 'S1', '/', 'S1', '-', 'S2', ';', 'DEF', 'S1', '#', 'S2', ';', 'S1', '#', 'S1', '+', 'S1', 'ENQUANTO', 'S1', 'MAIOR', 'S2', '{', 'DEF', 'S1', '#', 'S2', ';', 'SE', 'S2', 'MENOR', 'S2', '{', 'S1', '#', 'S2', ';', '}', '}', 'DEF', 'S1', ';', 'S1', '#', 'S2', ';', 'SE', 'S1', 'MENOR', 'S2', '{', 'DEF', 'S1', '#', 'S2', ';', '}', 'EOF']
Erro sintático: linha 8, sentença "enquanto" não reconhecida!
```
<br>

**Arquivo do código de exemplo para compilação:**

``` 
def a;
def ab # 1000;
a # 0 + 1011 ~ ab / a - 100;

def cy # 1;
a # a + cy;

enquanto ab maior 100 {
    def abcy # 1001;
    se 1001 menor 1000 {
        a # 1111;
    }
}

def z;
z # 0;

se z menor 1 {
    def abc # 10;
}

```
<br>

## Implementação

Funções desenvolvidas foram:
1. Gerar o autômato finito
2. Carregar o arquivo do código
3. Análise léxica
4. Análise sintática
5. Geração do arquivo intermediário
6. Reportar os dados das análises e fita de saída


## Como Contribuir

Para contribuir e deixar a comunidade open source um lugar incrivel para aprender, projetar, criar e inspirar outras pessoas. Basta seguir as instruções logo abaixo:

1. Realize um Fork do projeto
2. Crie um branch com a nova feature (`git checkout -b feature/featureCompilador`)
3. Realize o Commit (`git commit -m 'Add some featureCompilador'`)
4. Realize o Push no Branch (`git push origin feature/featureCompilador`)
5. Abra um Pull Request

<br>

## Autores

- **[Bárbara Pegoraro Markus](https://github.com/barbs-pm)** - _Acadêmica do Curso de Ciência da Computação -UFFS_. 
- **[Lucas Jaenisch](https://github.com/lucasjaenisch)** - _Acadêmico do Curso de Ciência da Computação -UFFS_. 
