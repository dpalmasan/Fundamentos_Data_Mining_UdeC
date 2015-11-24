library(tm); library(lsa)

N <- 240
# Leer argumento de linea

corpus <- rep("", N)
path <- "documentos_procesados2/"

for(i in 1:N) {
    filename <- paste0(path, i, ".txt")
    tmp <- readChar(filename, file.info(filename)$size)
    corpus[i] <- gsub("\n", " ", tmp)
}

# Transformar datos a corpus (para biblioteca tm)
corpus <- Corpus(VectorSource(corpus))

# corpus <- tm_map(corpus, stemDocument, language = "spanish")  

# Crear matriz de terminos-documentos a partir del corpus
AA <- TermDocumentMatrix(corpus)

# Formato como matriz de R
AA.matrix <- as.matrix(AA)

lsa_space <- lsa(AA)
new_matrix <- as.textmatrix(lsa_space)
save(new_matrix, file="lsa_space.RData")

