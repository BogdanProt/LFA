def load_sections(numefis):
  dict = {}
  try:
    f = open(numefis)
  except FileNotFoundError:
    print("Fila nu exista")
    return 0
  liniiContinut = [[x.rstrip('\n')] for x in f]
  for linie in liniiContinut:
    if linie[0][0] == '[':
      lista = []
      dict[linie[0]] = lista
    else:
      if linie[0][0] != '#':
        lista.append(linie[0])
  return dict

def load_sigma(myDict):
  listaSigma = myDict['[Sigma]']
  if len(listaSigma) == 0:
    print("ERROR! There are no symbols in the vocabulary")
    return 0
  if len(listaSigma) != len(set(listaSigma)):
    print("ERROR! There are duplicates in the vocabulary")
    return 0
  listaSigma = [symbol.rstrip(' ') for symbol in listaSigma]
  return listaSigma

def load_states(myDict):
  listaStates = myDict['[States]']
  if len(listaStates) == 0:
    print("ERROR! There are no states in the file")
  ok = 0
  for state in listaStates:
    if "S" in state:
      ok+=1
  if ok == 0:
    print("ERROR! There is no beginning state")
    return 0
  elif ok > 1:
    print("ERROR! There are too many beginning states")
    return 0
  ok = 0
  for state in listaStates:
    if "F" in state:
      ok+=1
  if ok == 0:
    print("ERROR! There is no final state")
    return 0
  elif ok > 1:
    print("ERROR! There are too many final states")
    return 0
  listaStates = [state.rstrip(' ') for state in listaStates]
  return listaStates


def load_actions(myDict):
  listaActions = myDict['[Actions]']
  if len(listaActions) == 0:
    print("ERROR! There are no actions in the file")
    return 0
  listaStates = load_states(myDict)
  for action in listaActions:
    listaActiuneCurenta = []
    listaActiuneCurenta = action.split()
    ok = 0
    for i in range(len(listaStates)):
      if listaActiuneCurenta[0] not in listaStates[i]:
        ok+=1
        #Verific de cate ori nu apare state-ul in lista mare de states
        #pentru a evita eroarea pentru state-urile de start si final
    if ok == len(listaStates):
      print("ERROR! The state does not exist")
      return 0
    ok = 0
    for i in range(len(listaStates)):
      if listaActiuneCurenta[2] not in listaStates[i]:
        ok+=1
    if ok == len(listaStates):
      print("ERROR! The state does not exist")
      return 0
    listaSigma = load_sigma(myDict)
    if listaActiuneCurenta[1] not in listaSigma:
      print("ERROR! The symbol does not appear in the alphabet")
      return 0
  return listaActions

continutDictionar = load_sections("fila.txt")
print(load_sigma(continutDictionar))
print(load_states(continutDictionar))
print(load_actions(continutDictionar))

def emulate_dfa(dfa, strn):
  listaStari = load_states(dfa)
  listaActiuni = load_actions(dfa)
  for s in listaStari:
    if 'S' in s:
      s_c = s[0:2]
  for s in strn:
    for action in listaActiuni:
      if s == action[3] and s_c == action[0:2]:
        s_c = action[5:7]
        break
  for s in listaStari:
    if 'F' in s:
      s_f = s[0:2]
  
  if s_c == s_f:
    return True
  return False

def emulate_nfa(nfa, strn):
  listaStari = load_states(nfa)
  listaActiuni = load_actions(nfa)
  s_c = []
  for s in listaStari:
    if 'S' in s:
      s_c.append(s[0:2])
  for s in strn:
    l = []
    for action in listaActiuni:
      if s == action[3] and action[0:2] in s_c:
        l.append(action[5:7])
    s_c = l  

  for s in listaStari:
    if 'F' in s:
      s_f = s[0:2]

  if s_f in s_c:
    return True
  return False

strn = input()
print(emulate_dfa(continutDictionar, strn))
print(emulate_nfa(continutDictionar, strn))
