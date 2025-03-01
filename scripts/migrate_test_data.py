import csv
import os
import sys
from collections import defaultdict

from sqlalchemy import select

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.models.tag import TagOrigin, TagValue

from app.models.company import (
    Company,
    CompanyLocalizedName,
    CompanyTag,
    CompanyNameToken,
)
from app.services.tokenizer import TokenizeService


from app.database import get_db


print("start migrate")

db = next(get_db())
with open("scripts/company_tag_sample.csv", newline="") as csvfile:
    rows = csv.DictReader(csvfile)

    # create tag
    all_rows = []
    all_tags = []
    tag_aggregates = defaultdict(set)
    tag_origin_ids = {}
    for row in rows:
        all_rows.append(row)
        for language in ["ko", "en", "ja"]:
            tags = row[f"tag_{language}"].split("|")
            all_tags += tags

    for t in all_tags:
        _s = t.split("_")[-1]
        tag_aggregates[f"_{_s}"].add(t)

    for k, vs in tag_aggregates.items():
        query = select(TagValue).where(TagValue.value.in_(vs))
        result = db.execute(query).scalars().all()
        if not result:
            to = TagOrigin()
            db.add(to)
            db.flush()
            for v in vs:
                tv = TagValue(tag_origin_id=to.id, value=v)
                db.add(tv)
            tag_origin_ids[k] = to.id
        else:
            tag_origin_ids[k] = result[0].tag_origin_id

    db.commit()

    # create company
    for row in all_rows:
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
                tags = row[f"tag_{language}"]
                for tag in tags.split("|"):
                    _s = tag.split("_")[-1]
                    to_id = tag_origin_ids[f"_{_s}"]
                    new_tag = CompanyTag(
                        company_id=company.id,
                        tag=tag,
                        language=language,
                        tag_origin_id=to_id,
                    )
                    db.add(new_tag)

        db.commit()

print("end migrate")
