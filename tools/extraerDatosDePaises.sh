declare -a countries=("Argentina" "South_Africa" "Romania")

filename=../data/temperaturas/GlobalLandTemperaturesByCountry.csv

# Obtener entradas para los paises
rm -f subset.csv
touch subset.csv
for i in "${countries[@]}"; do
	grep "$i" $filename >> subset.csv
done

# Obtener solamente la fecha, la temperatura y el pais
awk -F"," '$2!="" { print $1" "$2" "$4 }' subset.csv > tmp && mv tmp subset.csv

# Contar cantidad de paises
numberOfCountries=$(awk '{print $3}' subset.csv | sort | uniq | wc -l)

# Dejar solamente datos de anios donde estan todos los meses
minYear=$(sort subset.csv | head -n 1 | cut -d'-' -f1)
maxYear=$(sort subset.csv | tail -n 1 | cut -d'-' -f1)
rm -f aux
for i in $(seq $minYear $maxYear); do
	numberOfMonths=$(awk -F'-' -v year=$i '$1==year {count++}END{print count}' subset.csv)
	if [[ "$numberOfMonths" -ge "12*$numberOfCountries" ]]; then
		awk -F'-' -v year=$i '$1==year' subset.csv >> aux
	fi
done
sort -k3 aux > subset.csv
rm aux


rm -f perMonthsubset.csv
while read line; do
	year=$(echo $line | cut -d'-' -f1)
	month=$(echo $line | cut -d'-' -f2)
	temp=$(echo $line | cut -d' ' -f2)
	country=$(echo $line | cut -d' ' -f3)
	date=$(bc <<< "scale=5;$year+($month-1)/12")
	echo $date $temp $country >> perMonthsubset.csv
done < subset.csv


# Separar por pais
dir=paises
rm -r -f $dir
mkdir -p $dir
IFS=' ' read -r -a array <<< $(awk '{print $3}' perMonthsubset.csv | sort | uniq)
for c in "${array[@]}"; do
	awk -F" " -v country=$c '$3==country { print $1" "$2 }' perMonthsubset.csv > $dir/$c.csv
done