# Experimentos Tarea 1 Data Mining 2015.

# Entrenar LSA con los documentos obtenidos

file="lsa_space.RData"

if [ -f "$file" ]
then
	echo "LSA entrenado, procediendo al siguiente paso..."
else
	echo "Entrenando LSA..."
	Rscript train_lsa.R
fi

# Limpiar directorio
rm -r runs/experimento*

# Mantener constantes el número de entrada a todo el proceso, los umbrales
# correr el programa y registrar las reglas que se generan.
echo "Experimento 1" >> runs/experimento1.txt
echo "Cantidad de Documentos = 240" >> runs/experimento1.txt
echo "Support mínimo = 70%" >> runs/experimento1.txt
echo "Umbral de Disimilaridad = 90%" >> runs/experimento1.txt
echo >> runs/experimento1.txt
echo "================================" >> runs/experimento1.txt
echo " Reglas de Asociación Obtenidas" >> runs/experimento1.txt
echo "================================" >> runs/experimento1.txt

python reglas_asociacion.py 240 0.7
Rscript calc_disimilaridad.R 0.9 >> runs/experimento1.txt

# Incrementar el número de documentos de entrada a todo el proceso (en múltiplos de 10)
# correr el programa y registrar las reglas que se generan (mantenga constante los umbrales)
echo "Experimento 2" >> runs/experimento2.txt
array=( 40 80 120 160 200 240 )
for n_doc in "${array[@]}"; do
	echo "Cantidad de Documentos = $n_doc" >> runs/experimento2.txt
	echo "Support mínimo = 70%" >> runs/experimento2.txt
	echo "Umbral de Disimilaridad = 90%" >> runs/experimento2.txt
	echo >> runs/experimento2.txt
	echo "================================" >> runs/experimento2.txt
	echo " Reglas de Asociación Obtenidas" >> runs/experimento2.txt
	echo "================================" >> runs/experimento2.txt
	python reglas_asociacion.py $n_doc 0.7
	Rscript calc_disimilaridad.R 0.9 >> runs/experimento2.txt
	echo >> runs/experimento2.txt
done

# Mantener fijo el número de documentos, incrementar el umbral de support, correr el programa, y
# registrar las reglas que se generan (mantenga constante el umbral de disimilaridad).
echo "Experimento 3" >> runs/experimento3.txt
array=( 0.3 0.5 0.7 0.9 )
for support in "${array[@]}"; do
	echo "Cantidad de Documentos = $240" >> runs/experimento3.txt
	echo "Support mínimo = $support" >> runs/experimento3.txt
	echo "Umbral de Disimilaridad = 90%" >> runs/experimento3.txt
	echo >> runs/experimento3.txt
	echo "================================" >> runs/experimento3.txt
	echo " Reglas de Asociación Obtenidas" >> runs/experimento3.txt
	echo "================================" >> runs/experimento3.txt
	python reglas_asociacion.py 240 $support
	Rscript calc_disimilaridad.R 0.9 >> runs/experimento3.txt
	echo >> runs/experimento3.txt
done

# Incrementar en pasos de 2% el umbral de disimilaridad, y registrar las reglas que se generan
# (mantenga constante el número de documentos y el umbral de support)
echo "Experimento 4" >> runs/experimento4.txt
python reglas_asociacion.py 240 0.7
array=( 0.38 0.42 0.46 0.5 )
for disim in "${array[@]}"; do
	echo "Cantidad de Documentos = 240" >> runs/experimento4.txt
	echo "Support mínimo = 0.7" >> runs/experimento4.txt
	echo "Umbral de Disimilaridad = $disim" >> runs/experimento4.txt
	echo >> runs/experimento4.txt
	echo "================================" >> runs/experimento4.txt
	echo " Reglas de Asociación Obtenidas" >> runs/experimento4.txt
	echo "================================" >> runs/experimento4.txt
	Rscript calc_disimilaridad.R $disim >> runs/experimento4.txt
	echo >> runs/experimento4.txt
done

# Limpiar
rm -r reglas.txt

