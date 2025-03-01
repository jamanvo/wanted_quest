import csv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import get_db
from app.models.company import (
    Company,
    CompanyLocalizedName,
    CompanyTag,
    CompanyNameToken,
)
from app.services.tokenizer import TokenizeService

print("start migrate")

db = next(get_db())

with open("scripts/company_tag_sample.csv", newline="") as csvfile:
    rows = csv.DictReader(csvfile)

    for row in rows:
        company = Company()
        db.add(company)
        db.flush()

        for language in ["ko", "en", "ja"]:
            if row[f"company_{language}"]:
                name = CompanyLocalizedName(
                    company_id=company.id,
                    name=row[f"company_{language}"],
                    language=language,
                )
                db.add(name)
                for t_name in TokenizeService.tokenize_name(row[f"company_{language}"]):
                    token_name = CompanyNameToken(
                        company_id=company.id,
                        tokenized_name=t_name,
                    )
                    db.add(token_name)
            if row[f"tag_{language}"]:
                for tag in row[f"tag_{language}"].split("|"):
                    new_tag = CompanyTag(
                        company_id=company.id,
                        tag=tag,
                        language=language,
                    )
                    db.add(new_tag)

        db.commit()

print("end migrate")
