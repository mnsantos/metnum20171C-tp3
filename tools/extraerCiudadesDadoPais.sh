countryName=Argentina

filename=../data/temperaturas/GlobalLandTemperaturesByCity.csv

# Obtener entradas para el pais
grep $countryName $filename > ciudades$countryName.csv

# Obtener solamente la fecha, temperatura y ciudad
awk -F"," '$2!="" { print $1" "$2" "$4 }' ciudades$countryName.csv > tmp && mv tmp ciudades$countryName.csv

# Contar cantidad de ciudades
numberOfCities=$(awk '{print $3}' ciudades$countryName.csv | sort | uniq | wc -l)

# Dejar solamente datos de anios donde estan todos los meses
minYear=$(head -n 1 ciudades$countryName.csv | cut -d'-' -f1)
maxYear=$(tail -n 1 ciudades$countryName.csv | cut -d'-' -f1)
rm -f aux
for i in $(seq $minYear $maxYear); do
	numberOfMonths=$(awk -F'-' -v year=$i '$1==year {count++}END{print count}' ciudades$countryName.csv)
	if [[ "$numberOfMonths" -ge "12*$numberOfCities" ]]; then
		awk -F'-' -v year=$i '$1==year' ciudades$countryName.csv >> aux
	fi
done
sort -k3 aux > ciudades$countryName.csv
rm aux


rm -f perMonthciudades$countryName.csv
while read line; do
	year=$(echo $line | cut -d'-' -f1)
	month=$(echo $line | cut -d'-' -f2)
	temp=$(echo $line | cut -d' ' -f2)
	city=$(echo $line | cut -d' ' -f3)
	date=$(bc <<< "scale=5;$year+($month-1)/12")
	echo $date $temp $city >> perMonthciudades$countryName.csv
done < ciudades$countryName.csv


# Separar por ciudad
dir=ciudades
rm -r -f $dir
mkdir -p $dir
IFS=' ' read -r -a array <<< $(awk '{print $3}' perMonthciudades$countryName.csv | sort | uniq)
for c in "${array[@]}"; do
	awk -F" " -v city=$c '$3==city { print $1" "$2 }' perMonthciudades$countryName.csv > $dir/$c.csv
done