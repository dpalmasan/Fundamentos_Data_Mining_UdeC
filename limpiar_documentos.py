# -*- coding: utf-8 -*-
import codecs
import string
from nltk import word_tokenize
import unicodedata
import sys
import nltk
import enchant

# No se que tanta utilidad tiene.
tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')

# Cargar diccionario en espanol de enchant.
d = enchant.Dict("es_ES")

# Para remover puntuacion
tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
                      if unicodedata.category(unichr(i)).startswith('P'))

# Cargar stoplist de stoplist.txt
stoplist = ""
with codecs.open("stoplist.txt", "r", "utf-8-sig") as f:
	stoplist = f.read().replace('\n', ' ')

# Crear lista de stoplist.
stoplist = word_tokenize(stoplist)
stoplist.append('figura')
stoplist.append('tabla')

# Remueve puntuacion de un string codificado utf8.
def remove_punctuation(text):
    return text.translate(tbl)

# Retorna verdadero si una string dado es numero
def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

# Leer datos y retorna el string
def leer_documento(id):
	s = ""
	with codecs.open("docs/" + str(id) + ".txt", "r", "utf-8-sig") as f:
		s=f.read().replace('\n',' ').replace('-', ' ')
	return s

def procesar_documento(id):
	input_string = leer_documento(id)
	out = remove_punctuation(input_string.lower())
	out = ''.join(i for i in out if not i.isdigit())

	word_list = word_tokenize(out)

	# Eliminar stopwords, palabras de menos de 3 letras y numeros
	return [word for word in word_list if word not in stoplist]# and not is_int(word) and len(word) > 3 and d.check(word)]

def generar_bow(id):
	filtered_words = procesar_documento(id)
	# filtered_words.sort()
	with codecs.open("documentos_procesados2/" + str(id) + ".txt", "w", "utf-8-sig") as f:		
		for word in filtered_words:
			f.write("%s\n" % word)	
			
for id in range(1, 241):
	generar_bow(id)
