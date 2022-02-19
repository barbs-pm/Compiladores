def analisador_lexico(codigo_programador, regras_finais, fita_saida, simbolos, tabela_simbolos, tabela):
    separadores = [' ', '\n', '\t', '+', '-', '{', '}', '#', ';']
    espacadores = [' ', '\n', '\t']
    operadores  = ['+', '-', '#', ';']
    id = 0
    for idx, linha in enumerate(codigo_programador): #pega numero da linha e código de cada linha
        E = 'S'
        string = ''
        for char in linha:
            if char in operadores and string:   #caso lemos um operador e a string não está vazia
                if string[-1] not in operadores:    #se o ultimo caracter não é um operador
                    if E in regras_finais: #a regra do caracter lido é um dos regras_finais
                        tabela_simbolos.append({'Line': idx, 'State': E, 'Label': string}) 
                        fita_saida.append(E) #adicionamos a regra na fita de saida
                    else:
                        tabela_simbolos.append({'Line': idx, 'State': 'Error', 'Label': string})
                        fita_saida.append('Error')
                    E = tabela['S'][char][0]    #mapeamento para a próxima estrutura de operadores
                    string = char
                    id += 1
                else:   #se o último caractere é um operador
                    string += char  #adiciona na string o caracter e continua normalmente
                    if char not in simbolos:
                        E = '€'
                    else:
                        E = tabela[E][char][0]
            elif char in separadores and string:
                if E in regras_finais:
                    tabela_simbolos.append({'Line': idx, 'State': E, 'Label': string}) #adiciona em tabela_simbolos linha, estado e descricao
                    fita_saida.append(E) #caso seja um final, adiciona na fita de saida
                else:
                    tabela_simbolos.append({'Line': idx, 'State': 'Error', 'Label': string})
                    fita_saida.append('Error')
                E = 'S'
                string = ''
                id += 1
            else:
                if char in espacadores: #se for um espaçador, continua
                    continue
                if char not in separadores and char not in operadores and string:   #caso n seja um separador, operador e já exista algo na string
                    if string[-1] in operadores:    #caso não seja um separador ele somente incrementa na string
                        if E in regras_finais: #operado é um final
                            tabela_simbolos.append({'Line': idx, 'State': E, 'Label': string})
                            fita_saida.append(E)
                        else:
                            tabela_simbolos.append({'Line': idx, 'State': 'Error', 'Label': string})
                            fita_saida.append('Error')
                        E = 'S'
                        string = ''
                        id += 1
                string += char
                if char not in simbolos:    #caso o caracter não esteja na tabela de simbolos
                    E = '€'
                else:
                    E = tabela[E][char][0]  #o E recebe a regra do caracter 
    tabela_simbolos.append({'Line': idx, 'State': 'EOF', 'Label': ''})
    fita_saida.append('EOF')
    erro = False
    for linha in tabela_simbolos:
        if linha['State'] == 'Error':   #caso exita erro léxico, imprime
            erro = True
            print('Erro léxico: linha {}, sentença "{}" não reconhecida!'.format(linha['Line']+1, linha['Label']))
    if erro:
        exit()  #finaliza caso exista erro

    print("Fita de saída da etapa léxica: ")
    print(fita_saida)

def mapeamento(symbols, simbolo_redu, fita_saida, fita, tabela_simbolos):
    symbols_indexes = {}    #é feito um reverso com o index x name
    for index, symbol in enumerate(symbols):
        symbols_indexes[symbol['Name']] = str(index)
        simbolo_redu[str(index)] = symbol['Name']
    for fta in fita_saida: #nos estados que eram nomes, sao alterados pelo indice para ser reconhecido sintaticamente
        if fta == 'S1' or fta == 'ENQUANTO1:S1' or fta == 'IGUAL1:S1': 
            fta = 'VAR' 
        elif fta == 'S2':
            fta = 'NUM'
        elif fta == '$':
            fta = 'EOF'
        fita.append(symbols_indexes[fta])

    for line in tabela_simbolos: #troca S1 e S2 na fita_saida por VAR e NUM
        if line['State'] == 'S1' or line['State'] == 'ENQUANTO1:S1' or line['State'] == 'IGUAL1:S1':
            line['State'] = 'VAR'
        elif line['State'] == 'S2':
            line['State'] = 'NUM'
        elif line['State'] == '$':
            line['State'] = 'EOF'

def analisador_sintatico(root, simbolo_redu, fita, tabela_simbolos, escopo, block, fita_saida): #aqui é lido o arquivo_tokens xml pelas suas tags, nome, type, etc
    redux_symbol, symbols, productions, lalr_table, pilha  = [], [], [], [], ['0']

    def charge():
        xml_symbols = root.iter('Symbol')
        for symbol in xml_symbols:
            symbols.append({
                'Index': symbol.attrib['Index'],
                'Name': symbol.attrib['Name'],
                'Type': symbol.attrib['Type']
            })

        xml_productions = root.iter('Production')
        for production in xml_productions:
            productions.append({
                'NonTerminalIndex': production.attrib['NonTerminalIndex'],
                'SymbolCount': int(production.attrib['SymbolCount']),
            })

        lalr_states = root.iter('LALRState')
        for state in lalr_states:
            lalr_table.append({})
            for action in state:
                lalr_table[int(state.attrib['Index'])][str(action.attrib['SymbolIndex'])] = {
                    'Action': action.attrib['Action'],
                    'Value': action.attrib['Value']
                }

    def parser():
        idx = 0
        while True:
            ultimo_fita = fita[0]
            try:
                action = lalr_table[int(pilha[0])][ultimo_fita] #busca pelas acoes e valores
            except:
                print('Erro sintático: linha {}, sentença "{}" não reconhecida!'.format(tabela_simbolos[idx]['Line']+1, tabela_simbolos[idx]['Label']))
                exit()  #apresente o erro caso exista
                break

            if action['Action'] == '1':
                pilha.insert(0, fita.pop(0))    #remove da fita e add na pilha
                pilha.insert(0, action['Value'])
                idx += 1
            elif action['Action'] == '2':
                size = productions[int(action['Value'])]['SymbolCount'] * 2
                while size:
                    pilha.pop(0)
                    size -= 1
                redux_symbol.append(productions[int(action['Value'])]['NonTerminalIndex']) #adiciona não terminal na lista
                pilha.insert(0, productions[int(action['Value'])]['NonTerminalIndex'])  #insere na pilha tbm
                pilha.insert(0, lalr_table[int(pilha[1])][pilha[0]]['Value'])   
            elif action['Action'] == '3':
                print('salto')
            elif action['Action'] == '4':
                break

    def catch_statements(): #aqui é pego as declarações
        pilha_aux = [1]
        id = 1
        for symbol in redux_symbol:
            if simbolo_redu[symbol] == 'CONDS':
                id += 1
                pilha_aux.insert(0, id)
                block.append(pilha_aux[1])
            elif simbolo_redu[symbol] == 'REP' or simbolo_redu[symbol] == 'COND':
                pilha_aux.pop(0)
            elif simbolo_redu[symbol] == 'RVAR':
                escopo.append(pilha_aux[0])

    def complete_ts():  #completa a tabela de simbolos
        for token in tabela_simbolos:
            if token['State'] == 'VAR': #se o token for VAR
                token['Scope'] = escopo.pop(0)  # adiciona o escopo em que ela está

    charge()
    mapeamento(symbols, simbolo_redu, fita_saida, fita, tabela_simbolos)
    parser()
    catch_statements()
    complete_ts()

def analisador_semantico(block, tabela_simbolos):
    var_scope = {}
    error = False

    def check_scope(scope_use, scope_dec):  #verifica se o escopo utilizado é o mesmo do escopo declarado
        if scope_use == scope_dec:
            return True
        elif scope_use == 1:
            return False
        else:
            return check_scope(block[scope_use-2], scope_dec)


    for index, token in enumerate(tabela_simbolos):
        if token['State'] == 'VAR' and tabela_simbolos[index-1]['State'] == 'DEF':
            if token['Label'] in var_scope: #caso a variável já esteja declarada
                error = True
                print('Erro semântico: linha {}, variável "{}" já declarada!'.format(token['Line']+1, token['Label']))
            else:
                var_scope[token['Label']] = token['Scope']  #adiciona o scopo da variavel

        if token['State'] == 'VAR' and tabela_simbolos[index-1]['State'] != 'DEF':
            if token['Label'] in var_scope:
                if not check_scope(token['Scope'], var_scope[token['Label']]):  #se o escopo n for o mesmo do declarado, erro
                    error = True
                    print('Erro semântico: linha {}, variável "{}" escopo inválido!'.format(token['Line']+1, token['Label']))
            else:
                error = True
                print('Erro semântico: linha {}, variável "{}" não declarada!'.format(token['Line']+1, token['Label']))
    if error:
        exit()

def codigo_intermediario(tabela_simbolos):
    ts_code = []
    int_code = []

    def encontra_operacoes():
        flag = False
        operacao = []
        for idx, token in enumerate(tabela_simbolos):
            if token['State'] == 'VAR' and tabela_simbolos[idx+1]['State'] == '#' and tabela_simbolos[idx+1]['State'] != ';':  #se for atribuicao de variavel, VAR # 1 ;
                operacao.append(token['Label'])
                flag = True
            elif token['State'] == ';' and tabela_simbolos[idx-2]['State'] != 'DEF': #verifica se for definicao de variavel, def VAR;
                ts_code.append(operacao)
                operacao = []
                flag = False
            elif flag:
                operacao.append(token['Label'])


    def gera_temp(operacao, temp):
        flag = False
        cod, copy = [], []
        copy.extend(operacao)

        for idx in range(len(operacao)-1):  #pega inicio e fim da linha
            if operacao[idx+1] == '~' or operacao[idx+1] == '/':    #se for multiplicacao ou divisao
                for i in range(-1, 2):
                    cod.insert(0, copy[idx])    #salva em cod as proximas contas, a # 0 "~b/1" por exemplo
                    copy.pop(idx)
                copy.insert(idx, 'T' + str(temp))
                flag = True
                break

        if not flag:
            for idx in range(len(operacao)-1):
                if operacao[idx+1] == '+' or operacao[idx+1] == '-':    #caso seja soma ou subtracao
                    for i in range(-1, 2):
                        cod.insert(0, copy[idx])    #salva em cod as proximas contas
                        copy.pop(idx)
                    copy.insert(idx, 'T' + str(temp))
                    break

        cod.insert(0, '#')
        cod.insert(0, 'T'+str(temp))    #insere em T+numero qtd chamada da funcao as contas
        return copy, cod

    def gera_codigo():
        temp = 1
        for operacao in ts_code:
            while True:
                if len(operacao) == 3:  #se for uma operacao simples, a # 0;
                    cod = []
                    for x in range(len(operacao)):
                        cod.append(operacao[x]) #adiciona em cod a operacao 

                    int_code.append(cod)
                    break

                operacao, cod = gera_temp(operacao, temp)   #passa a operacao e o variavel aux parar se colocada em T1, T2, etc
                temp += 1
                int_code.append(cod) #salva no código intermediario

    def exporta_codigo():
        file = open('configuracao/codigo_intermediario.txt', 'w+')
        for x in int_code:  #exporta codigo intermediario para cada linha do arquivo_tokens
            file.write(str(x).replace('[','').replace(']','').replace("'",'').replace(',','') +'\n')

    encontra_operacoes()
    gera_codigo()
    exporta_codigo()
