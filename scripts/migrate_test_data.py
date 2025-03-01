import csv


print("start migrate")

with open("scripts/company_tag_sample.csv", newline="") as csvfile:
    rows = csv.DictReader(csvfile)
    for r in rows:
        print(r)


print("end migrate")
