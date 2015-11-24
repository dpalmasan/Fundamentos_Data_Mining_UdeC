# Con este script se extraeran palabras claves de los textos.

# Third party dependencies
library(tm);

# Leer argumento de linea
N <- 240

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

filename <- "palabra_documento/mapeo.txt"
l <- apply(AA.matrix, 1, function(x) which(x > 0, arr.ind=TRUE, useNames = FALSE))
sink(filename)
for (i in 1:length(l))
    cat(names(l[i]), paste(l[[i]], collapse = " "), "\n")
sink()


# Para cada documento extraer las 10 palabras con mayor ponderacion, y guardarlas
# en archivo.
path <- "documentos_keywords/"
for(i in 1:N) {
    filename <- paste0(path, i, ".txt")
    fileConn<-file(filename)
    # Extraer las palabras mas relevantes
    tmp <- rownames(as.matrix(AA.matrix[AA.matrix[, i] > 1, i]))
    writeLines(paste(tmp, collapse = " "), fileConn)
    close(fileConn)
}