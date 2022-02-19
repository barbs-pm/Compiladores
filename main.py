import xml.etree.ElementTree as ET
from geracaoAutomato import *
from compilador import *

arquivo_tokens = list(open('configuracao/tks.txt'))
codigo_programador  = list(open('configuracao/codigo.txt'))
arvore = ET.parse('configuracao/parsing.xml')
root = arvore.getroot()

def main():
    block, vivos, alcan, regras_finais, fita, escopo, simbolos, estados, tabela_simbolos, fita_saida = [], [], [], [], [], [], [], [], [], []
    epTransicao, gramatica, simbolo_redu, tabela = {}, {}, {}, {}
    gramatica['S'] = []
    estadoinicial = ''
    
    for x in arquivo_tokens: #le o arquivo_tokens
        if '<S> ::=' in x:
            estadoinicial = x
        if '::=' in x:
            tratar_gramatica(x, estadoinicial, simbolos, gramatica) #funcao que trata a gramatica
        else:
            tratar_token(x, simbolos, gramatica, regras_finais) #trata os tokens e salva na regra da gramatica
    
    #gerar autômato
    criar_automato_finitos(gramatica, tabela, estados, simbolos, regras_finais)  
    eliminar_et(tabela, regras_finais)
    determizinar(tabela, estados, simbolos, regras_finais)
    buscar_alcansaveis('S', alcan, tabela)
    eliminar_inalcansaveis(tabela, alcan)
    estado_erro(tabela, simbolos)
    vivos.extend(regras_finais)    #adiciona as regras regras_finais ao vivos
    buscar_vivos(tabela, vivos)
    eliminar_mortos(tabela, vivos)
    criar_csv(tabela, regras_finais)

    # fazer a analise do código
    analisador_lexico(codigo_programador, regras_finais, fita_saida, simbolos, tabela_simbolos, tabela)
    analisador_sintatico(root, simbolo_redu, fita, tabela_simbolos, escopo, block, fita_saida)
    analisador_semantico(block, tabela_simbolos)
    codigo_intermediario(tabela_simbolos)

    print('Compilado com sucesso!')

print('\n')
main()