# Problem 1 Done
import csv
from collections import Counter

fire_pokemon_levels = []
total_fire_pokemon = 0
fire_pokemon_above_40 = 0

with open('pokemonTrain.csv') as pokemonFile:
    csvReader = csv.reader(pokemonFile)
    next(csvReader)  
    for row in csvReader:
        if row[4] == "fire":
            total_fire_pokemon += 1
            if float(row[2]) >= 40 and row[4] =="fire":
                fire_pokemon_above_40 += 1

percentage = (fire_pokemon_above_40 / total_fire_pokemon)*100
percentage1 = round(percentage)

with open("pokemon1.txt", "w") as output_file:
    output_file.write("Percentage of fire type Pokemons at or above level 40 = " + str(percentage1))



# Problem 2 and 3 Done
import csv
from collections import Counter

data = []
header = []


with open('pokemonTrain.csv') as pokemonFile:
    csvReader = csv.reader(pokemonFile)
    header = next(csvReader)
    data = list(csvReader)


weakness_to_type_mapping = {}
for row in data:
    if row[4] != "NaN":
        weakness = row[5]
        if weakness not in weakness_to_type_mapping:
            weakness_to_type_mapping[weakness] = []
        if row[4] not in weakness_to_type_mapping[weakness]:
            weakness_to_type_mapping[weakness].append(row[4])

for row in data:
    if row[4] == "NaN":
        weakness = row[5]
        if weakness in weakness_to_type_mapping:
            type_counts = Counter(weakness_to_type_mapping[weakness])
            most_common_type = sorted(type_counts.items(), key=lambda x: (-x[1], x[0]))[0][0]
            row[4] = most_common_type

# Problem 2 and 3 
atk_count_above_40 = 0
atk_sum_above_40 = 0
df_count_above_40 = 0
df_sum_above_40 = 0
hp_count_above_40 = 0
hp_sum_above_40 = 0
atk_count_below_40 = 0
atk_sum_below_40 = 0
df_count_below_40 = 0
df_sum_below_40 = 0
hp_count_below_40 = 0
hp_sum_below_40 = 0

for row in data:
    if row[6] != "NaN":
        if float(row[2]) > 40:
            atk_sum_above_40 += float(row[6])
            atk_count_above_40 += 1
        else:
            atk_sum_below_40 += float(row[6])
            atk_count_below_40 += 1

    if row[7] != "NaN":
        if float(row[2]) > 40:
            df_sum_above_40 += float(row[7])
            df_count_above_40 += 1
        else:
            df_sum_below_40 += float(row[7])
            df_count_below_40 += 1

    if row[8] != "NaN":
        if float(row[2]) > 40:
            hp_sum_above_40 += float(row[8])
            hp_count_above_40 += 1
        else:
            hp_sum_below_40 += float(row[8])
            hp_count_below_40 += 1


avg_attack_above_40 = round(atk_sum_above_40 / atk_count_above_40,1) if atk_count_above_40 != 0 else 0
avg_defense_above_40 = round(df_sum_above_40 / df_count_above_40,1) if df_count_above_40 != 0 else 0
avg_hp_above_40 = round(hp_sum_above_40 / hp_count_above_40,1) if hp_count_above_40 != 0 else 0

avg_attack_below_40 = round(atk_sum_below_40 / atk_count_below_40,1) if atk_count_below_40 != 0 else 0
avg_defense_below_40 = round(df_sum_below_40 / df_count_below_40,1) if df_count_below_40 != 0 else 0
avg_hp_below_40 = round(hp_sum_below_40 / hp_count_below_40,1) if hp_count_below_40 != 0 else 0


for row in data:
    if row[6] == "NaN":
        if float(row[2]) > 40:
            row[6] = str(float(avg_attack_above_40))
        else:
            row[6] = str(float(avg_attack_below_40))

    if row[7] == "NaN":
        if float(row[2]) > 40:
            row[7] = str(float(avg_defense_above_40))
        else:
            row[7] = str(float(avg_defense_below_40))

    if row[8] == "NaN":
        if float(row[2]) > 40:
            row[8] = str(float(avg_hp_above_40))
        else:
            row[8] = str(float(avg_hp_below_40))


with open('pokemonResult.csv', 'w', newline='') as updatedFile:
    csvWriter = csv.writer(updatedFile)
    csvWriter.writerow(header)  
    csvWriter.writerows(data)  


# Problem 4 Done
import csv 


with open("pokemonResult.csv") as pokefile:
    csvReader = csv.reader(pokefile)
    header = next(csvReader)
    dict1 = {}
    
 
    for row in csvReader:
        if row[4] not in dict1:
            dict1[row[4]] = []
    
    
    pokefile.seek(0)
    
   
    csvReader = csv.reader(pokefile)
    next(csvReader)  
    
    # Second pass through the file
    for row1 in csvReader:
        if row1[4] in dict1:
            dict1[row1[4]].append(row1[3])
    sorted_keys = sorted(dict1.keys())

with open("pokemon4.txt", "w") as file:
  
    for key in sorted_keys:
        file.write(f"{key}: {', '.join(map(str, dict1[key]))}\n")



# Problem 5 Done
import csv

with open("pokemonResult.csv") as pokefile:
    csvReader = csv.reader(pokefile)
    header = next(csvReader)
    stage_count = 0
    hp_sum = 0
    for row5 in csvReader:
        if row5[9] == "3.0":
            stage_count += 1
            hp_sum += float(row5[8])      
    average_hp_3 = hp_sum / stage_count
    average_hp_4 = round(average_hp_3)
with open("pokemon5.txt", "w") as pokefile2:
    pokefile2.write("Average hit point for Pokemons of stage 3.0 = " + str(average_hp_4))