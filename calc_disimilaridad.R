library(lsa)
load('lsa_space.RData')

# Leer comando de linea
umbral_disim <- as.numeric(commandArgs(trailingOnly = TRUE))

# Calculos de disimilaridad con las reglas obtenidas.
reglas <- read.table("reglas.txt")[-2]
colnames(reglas) <- c("ant", "cons")
reglas <- as.matrix(reglas)
disim <- apply(reglas , 1, function(x) 1 - cosine(new_matrix[x[1],], new_matrix[x[2], ]))
mayor_que_umbral <- disim > umbral_disim
reglas <- as.data.frame(reglas)
reglas$disim <- disim
reglas$mayor_que_umbral <- mayor_que_umbral
unique(reglas[ order(-reglas[,3], reglas[,1]), ])