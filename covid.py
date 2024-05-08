import csv
import re
from datetime import datetime
from collections import Counter


def convert_date_format(date_str):
   
    date_obj = datetime.strptime(date_str, "%d.%m.%Y")
  
    return date_obj.strftime("%m.%d.%Y")


with open("covidTrain.csv", "r", newline='') as csvfile:
    csvReader = csv.reader(csvfile)
    header = next(csvReader)  

    
    all_rows = []

    
    province_dict = {}

    
    for row in csvReader:
        all_rows.append(row)
        
        if row[6] != "NaN":
            if row[4] not in province_dict.keys():
                province_dict[row[4]] = []

    
    for row in all_rows:
        if row[6] != "NaN":
            province_dict[row[4]].append(float(row[6]))

   
    average_dict = {}
    for province, values in province_dict.items():
        total = sum(values)  # Calculate total sum of values
        average = total / len(values)  # Calculate average
        average_dict[province] = round(average, 2)  # Store average in the new dictionary

   
    for row in all_rows:
        if row[6] == "NaN":
            if row[4] in average_dict.keys():
                row[6] = str(average_dict[row[4]])

   
    longitude_dict = {}
    for row in all_rows:
        if row[7] != "NaN":
            if row[4] not in longitude_dict.keys():
                longitude_dict[row[4]] = []
            longitude_dict[row[4]].append(float(row[7]))

    
    average_longitude_dict = {}
    for province, values in longitude_dict.items():
        total_longitude = sum(values)
        average_longitude = total_longitude / len(values)
        average_longitude_dict[province] = round(average_longitude, 2)

   
    for row in all_rows:
        if row[7] == "NaN":
            if row[4] in average_longitude_dict.keys():
                row[7] = str(average_longitude_dict[row[4]])

   
    for row in all_rows:
        
        for i in [8, 9, 10]:
            row[i] = convert_date_format(row[i])

        
        res = re.search("[0-9]+-+[0-9]+", row[1])
        if res:
            str1 = row[1].split("-")
            average = round((int(str1[0]) + int(str1[1])) / 2)
            row[1] = str(average)  

    
    most_common_dict = {}

    
    province2_dict = {}
    for row in all_rows:
        if row[4] not in province2_dict.keys():
            province2_dict[row[4]] = []
    for row in all_rows:
        if row[3] != "NaN":
            province2_dict[row[4]].append(row[3])

   
    for province, values in province2_dict.items():
        most_common_value = Counter(values).most_common(1)[0][0]
        most_common_dict[province] = most_common_value

    
    for row in all_rows:
        if row[3] == "NaN":
            row[3] = most_common_dict[row[4]]

    
    province_symptoms_dict = {}

    
    for row in all_rows:
        province = row[4]
        symptoms = row[11].split(';')  
        for symptom in symptoms:
            symptom = symptom.strip()  
            if province not in province_symptoms_dict:
                province_symptoms_dict[province] = []
            province_symptoms_dict[province].append(symptom)

    
    for province, symptoms_list in province_symptoms_dict.items():
        symptoms_count = Counter(symptoms_list)
        most_common_symptoms = sorted(symptoms_count.items(), key=lambda x: (-x[1], x[0]))
        province_symptoms_dict[province] = most_common_symptoms[0][0]

    for row in all_rows:
        if row[11] == "NaN":
            province = row[4]
            if province in province_symptoms_dict:
                row[11] = province_symptoms_dict[province]
with open("covidResult.csv", "w", newline='') as modified_csvfile:
    csvWriter = csv.writer(modified_csvfile)
    csvWriter.writerow(header)  # Write the header
    csvWriter.writerows(all_rows)  # Write the modified rows