import codecs

def load_dataset():
    "Cargar dataset de ejemplo, ver diapositivas curso."
    return [['i1', 'i3', 'i4'], ['i2', 'i3', 'i5'], ['i1', 'i2', 'i3', 'i5'], ['i2', 'i5']]


def createC1(dataset):
    "Crea una lista de candidatos, de tamanho 1"
    c1 = []
    for transaction in dataset:
        for item in transaction:
            if not [item] in c1:
                c1.append([item])
    c1.sort()
    # Se aplica frozenser a cada elemento de c1 (para que conjuntos puedan ser hasheables)
    return map(frozenset, c1)


def scanD(dataset, candidates, min_support):
    "Retorna todos los candidatos con un nivel de support minimo."

	# Diccionario calcular support
    sscnt = {}
    for tid in dataset:
        for can in candidates:
            if can.issubset(tid):
                sscnt.setdefault(can, 0)
                sscnt[can] += 1

    num_items = float(len(dataset))
    retlist = []
    support_data = {}
	
	# Se calcula el support para todos los candidatos
    for key in sscnt:
        support = sscnt[key] / num_items
		# Se insertan a la lista los que tengan un support mayor que el umbral.
        if support >= min_support:
            retlist.insert(0, key)
		# Se guarda en un diccionario (hash) los datos de support calculados.
        support_data[key] = support
    return retlist, support_data


def aprioriGen(freq_sets, k):
    "A partir de los conjuntos candidatos, genera transacciones compuestas"
    retList = []
    lenLk = len(freq_sets)

	# Se generan las distintas combinaciones posibles.
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(freq_sets[i])[:k - 2]
            L2 = list(freq_sets[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(freq_sets[i] | freq_sets[j])
	# Se retornan los conjuntos compuestos.
    return retList


def apriori(dataset, minsupport=0.7):
    "Genera una lista de item sets candidatos."

	# Crear listas de tamanho 1 a partir del dataset.
    C1 = createC1(dataset)

	# Pasa a "set" todos los datos del dataset, para evitar items repetidos en algun dato.
    D = map(set, dataset)

	# Genera candidatos de tamanho 1, que cumplan con el support minimo.
    L1, support_data = scanD(D, C1, minsupport)
    L = [L1]
    k = 2

	# Genera itemsets hasta que la lista quede vacia.
    while (len(L[k - 2]) > 0):
        Ck = aprioriGen(L[k - 2], k)
        Lk, supK = scanD(D, Ck, minsupport)
        support_data.update(supK)
        L.append(Lk)
        k += 1

    return L, support_data
	
def generateRules(L, support_data, min_confidence=0):
    """Crea las reglas de asociacion.
    L: Lista de items frecuentes
    support_data: support para dichos itemsets.
    min_confidence: Umbral minimo de confidence.
    """
    # Utilizado para generar el archivo de salida con las reglas if A then B
    global file
    rules = []
    file = codecs.open('reglas.txt','w', "utf-8-sig")
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            #print "freqSet", freqSet, 'H1', H1
            if (i > 1):
                rules_from_conseq(freqSet, H1, support_data, rules, min_confidence)
            else:
                calc_confidence(freqSet, H1, support_data, rules, min_confidence)
    file.close()
    return rules


def calc_confidence(freqSet, H, support_data, rules, min_confidence=0.7):
    "Evalua la regla generada"
    global file
    pruned_H = []
    for conseq in H:
        conf = support_data[freqSet] / support_data[freqSet - conseq]
        if conf >= min_confidence:
            print >> file, iter(freqSet - conseq).next() + ' ---> '.encode('utf8') + iter(conseq).next()
            rules.append((freqSet - conseq, conseq, conf))
            pruned_H.append(conseq)
    return pruned_H


def rules_from_conseq(freqSet, H, support_data, rules, min_confidence=0.7):
    "Genera un conjunto de reglas candidatas"
    m = len(H[0])
    if (len(freqSet) > (m + 1)):
        Hmp1 = aprioriGen(H, m + 1)
        Hmp1 = calc_confidence(freqSet, Hmp1,  support_data, rules, min_confidence)
        if len(Hmp1) > 1:
            rules_from_conseq(freqSet, Hmp1, support_data, rules, min_confidence)
