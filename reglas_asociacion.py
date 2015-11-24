import codecs
import apriori
import sys

def leer_documento(id):
	"""
	Lee un documento dado su identificador.
	"""
	s = ""
	with codecs.open("documentos_keywords/" + str(id) + ".txt", "r", "utf-8-sig") as f:
		s=f.read()
	return s.split()

def cargar_datos(N):
	"""
	Carga N documentos, para realizar los experimentos. 
	"""
	data = []
	for i in range(1, N + 1):
		data.append(leer_documento(i))
	return data


if __name__ == "__main__":
	# Leer argumentos de entrada
    N = int(sys.argv[1])
    support = float(sys.argv[2])

	# Cargar datos
    dataset = cargar_datos(N)
	# Aplicar algoritmo apriori
    L, support_data = apriori.apriori(dataset, minsupport = support)
	# Generar reglas
    apriori.generateRules(L, support_data, min_confidence = 0.0)


