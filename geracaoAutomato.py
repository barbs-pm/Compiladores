import csv

repeticao = 0

def eliminar_mortos(tabela, vivos):
    mortos = []
    for x in tabela:
        if x not in vivos and x != '€': #adiciona a regra aos mortos caso não esteja em vivos e não seja €
            mortos.append(x)

    for x in mortos:
        del tabela[x]   #deleta da tabela os mortos

def buscar_vivos(tabela, vivos):
    mudou = False

    for regra in tabela:
        for simbolo in tabela[regra]:
            if tabela[regra][simbolo][0] in vivos and regra not in vivos:
                vivos.append(regra) # se o simbolo esta em vivos e a regra não está, add em vivos a regra
                mudou = True

    if mudou:
        buscar_vivos(tabela, vivos)  #chama novamente, mudando a flag no inicio da funcao

def eliminar_inalcansaveis(tabela, alcan):
    loop = {}
    loop.update(tabela)
    for regra in loop:
        if regra not in alcan:  #remove regra da tabela se não estiverem em alcan
            del tabela[regra]

def buscar_alcansaveis(estado, alcan, tabela):
    if estado not in alcan: #adiciona estado no alcan caso n esteja
        alcan.append(estado)
        for simbolo in tabela[estado]: #passa por cada simbolo de estado da tabela 
            if tabela[estado][simbolo] and tabela[estado][simbolo][0] not in alcan: #continua adicionando os simbolos em alcan
                buscar_alcansaveis(tabela[estado][simbolo][0], alcan, tabela)

def encontrar_eps_set(e_transicoes, tabela):    #encontra os estados que possuem o epsilon
    for x in e_transicoes:
        for y in tabela[x]['&']:
            if y not in e_transicoes:
                e_transicoes.append(y)
    return e_transicoes

def eliminar_et(tabela, regras_finais):
    for regra in tabela:
        et_set = encontrar_eps_set(tabela[regra]['&'], tabela)
        for estado in et_set:
            if estado in regras_finais: #verifica se o estado que possui & está nos regras_finais, se não está add
                regras_finais.append(regra)
            for simbolo in tabela[estado]:
                for transicao in tabela[estado][simbolo]:   #verifica a transicao do estado e add na tabela caso ela não esteja
                    if transicao not in tabela[regra][simbolo]:
                        tabela[regra][simbolo].append(transicao)
        tabela[regra]['&'] = []

def criar_novos(nstates, tabela, estados, simbolos, regras_finais):
    for x in nstates:
        tabela[x] = {}
        estados.append(x)   #salva o novo estado na tabela de estados
        for y in simbolos:
            tabela[x][y] = []
        tabela[x]['&'] = []

    for state in nstates:
        estadosjuntar = sorted(state.split(':'))
        for x in estadosjuntar:
            if x in regras_finais and state not in regras_finais: #faz uma nova verificação se está nos regras_finais, caso não esteja adiciona
                regras_finais.append(state)
            for simbolo in simbolos:
                for transition in tabela[x][simbolo]:
                    if not tabela[state][simbolo].__contains__(transition): #verifica se existe na tabela e add caso não esteja
                        tabela[state][simbolo].append(transition)
    determizinar(tabela, estados, simbolos, regras_finais) #verifica novamente

def determizinar(tabela, estados, simbolos, regras_finais):
    novosestados = []
    for regra in tabela:
        for producao in tabela[regra]:
            if len(tabela[regra][producao]) > 1:    #busca pela regra com mais de 1 producao
                novo = []
                for estado in tabela[regra][producao]:
                    if ':' in estado:
                        for aux in estado.split(':'):   #verifica e divide se tem mais regra
                            if aux not in novo:
                                novo.append(aux)    #adiciona na variavel nova
                    else:
                        if estado not in novo:
                            novo.append(estado) #adiciona na varivel nova

                if novo:
                    novo = sorted(novo)
                    novo = ':'.join(novo)   #cria nova regra
                if novo and novo not in novosestados and novo not in list(tabela.keys()):
                    novosestados.append(novo)
                tabela[regra][producao] = novo.split() #salva na tabela a nova regra
    if novosestados:
        criar_novos(novosestados, tabela, estados, simbolos, regras_finais)

def criar_automato_finitos(gramatica, tabela, estados, simbolos, regras_finais): #cria automato finito
    for x in gramatica:
        tabela[x] = {}
        estados.append(x)   #pega todos estados da lista de gramatica
        for y in simbolos:
            tabela[x][y] = []
        tabela[x]['&'] = [] #limpado o estado do &
    

    for regra in gramatica:
        for producao in gramatica[regra]:
            if len(producao) == 1 and producao.islower() and regra not in regras_finais:
                regras_finais.append(regra)    #adiciona a regra nas regras regras_finais caso seja = 1, minuscula e já n esteja nas regras_finais
            elif producao == '&' and regra not in regras_finais:
                regras_finais.append(regra)    #adiciona $ nas regras_finais
            elif producao[0] == '<':
                tabela[regra]['&'].append(producao.split('<')[1][:-1]) #remove <> da regra e adiciona o que tem entre eles
            elif producao != '&':
                tabela[regra][producao[0]].append(producao.split('<')[1][:-1])  #remove <> da regra e inicial

def criar_sn(s, gramatica):
    global repeticao
    if 'S' + str(repeticao) in gramatica:
        return
    gramatica['S' + str(repeticao)] = s.replace('\n', '').split(' ::= ')[1].replace('>', str(repeticao) + '>').split(' | ')

def tratar_gramatica(gram, s, simbolos, gramatica):
    global repeticao #aux numero de repetições
    gram = gram.replace('\n', '')
    for x in gram.split(' ::= ')[1].replace('<', '').replace('>', '').split(' | '): #separa letra da regra na posicao 0
        if x[0] not in simbolos and not x[0].isupper(): #verifica se não esta em simbolos e se não é maiuscula 
            simbolos.append(x[0])   #salva em simbolos
    regra = gram.split(' ::= ')[0].replace('>', str(repeticao)).replace('<', '') #concatena letra da regra + número da repetição
    
    if regra[0] == 'S': #se a regra for S, repeticao+1
        repeticao += 1
        gramatica['S'] += gram.split(' ::= ')[1].replace('>', str(repeticao) + '>').split(' | ')    #concatena na linha as próximas regras, ex: S0::=aS1
    else:
        gramatica[regra] = gram.split(' ::= ')[1].replace('>', str(repeticao)+'>').split(' | ')  

    if '<S>' in gram.split(' ::= ')[1]:
        criar_sn(s, gramatica)

def tratar_token(token, simbolos, gramatica, regras_finais):
    token = token.replace('\n', '') #replace a cada \n pra pegar o token
    cp_token = token
    token = list(token) #quebra o token em caracteres
    for x in range(len(token)):
        if token[x] not in simbolos and not token[x].isupper(): #joga os caracteres dos tokens pra dentro de simbolos
            simbolos.append(token[x])

        if len(token) == 1:
            iniregra = '<' + cp_token.upper() + '>'
            gramatica['S'] += str(token[x] + iniregra).split() #salva na gramatica as regras de tamanho 1
            gramatica[cp_token.upper()] = []
            regras_finais.append(cp_token.upper()) #salva na lista os tokens de tamanho 1
        elif x == 0 and x != len(token)-1:
            iniregra = '<' + cp_token.upper() + '1>'
            gramatica['S'] += str(token[x] + iniregra).split()  #salva na gramatica as regras de tamanho maior que 1 / o inicio deles
        elif x == len(token)-1:
            finregra = '<' + cp_token.upper() + '>'
            gramatica[cp_token.upper() + str(x)] = str(token[x] + finregra).split() #salva na gramatica as regras de tamanho maior que 1 / o fim deles
            gramatica[cp_token.upper()] = []
            regras_finais.append(cp_token.upper()) #salva na lista os tokens de tamanho maior que 1
        else:
            proxregra = '<' + cp_token.upper() + str(x+1) + '>'
            gramatica[cp_token.upper() + str(x)] = str(token[x] + proxregra).split() #salva na gramatica as regras de tamanho maior que 1 / o meio fim deles

def criar_csv(tabela, regras_finais):
    with open('afnd.csv', 'w', newline='') as f:
        w = csv.writer(f)
        copydict = {}
        copydict.update(tabela)
        w.writerow(list(copydict['S'].keys()) + ['regra'])
        for x in copydict:
            if x in regras_finais:
                copydict[x]['nomeregra'] = x + '&' #adiciona nome da regra concatenado com o epsilon
            else:
                copydict[x]['nomeregra'] = x #se não for final, não concatena com o epsilon
            w.writerow(copydict[x].values())

def estado_erro(tabela, simbolos):
    tabela['€'] = {}
    for y in simbolos:
        tabela['€'][y] = [] #adiciona todos os simbolos no € como posição
    tabela['€']['&'] = []   #epsilon também
    for regra in tabela:
        for simbolo in tabela[regra]:
            if not tabela[regra][simbolo]:
                tabela[regra][simbolo] = ['€']  #adicona € nas posições do simbolo da regra com valor nulo