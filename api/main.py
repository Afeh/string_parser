from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from .database import Base, engine, SessionLocal
from .models import StringRecord
from .utils import analyze_string
from .nlp_parser import parse_query
from sqlalchemy.orm import Session
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.post("/strings", status_code=201)
def create_string(data: dict, db: Session = Depends(get_db)):
    value = data.get("value")
    if not isinstance(value, str):
        raise HTTPException(status_code=422, detail="Value must be a string")
    existing = db.query(StringRecord).filter_by(value=value).first()
    if existing:
        raise HTTPException(status_code=409, detail="String already exists")

    props = analyze_string(value)
    new_string = StringRecord(id=props["sha256_hash"], value=value, properties=props)
    db.add(new_string)
    db.commit()
    db.refresh(new_string)
    return {
        "id": new_string.id,
        "value": new_string.value,
        "properties": props,
        "created_at": new_string.created_at
    }


@app.get("/strings/filter-by-natural-language")
def filter_by_natural_language(query: str, db: Session = Depends(get_db)):
    try:
        parsed_filters = parse_query(query)
    except ValueError:
        raise HTTPException(status_code=400, detail="Unable to parse natural language query")

    # Reuse the filtering logic from /strings
    records = db.query(StringRecord).all()
    filtered = []
    for rec in records:
        props = rec.properties
        if "is_palindrome" in parsed_filters and props["is_palindrome"] != parsed_filters["is_palindrome"]:
            continue
        if "min_length" in parsed_filters and props["length"] < parsed_filters["min_length"]:
            continue
        if "max_length" in parsed_filters and props["length"] > parsed_filters["max_length"]:
            continue
        if "word_count" in parsed_filters and props["word_count"] != parsed_filters["word_count"]:
            continue
        if "contains_character" in parsed_filters and parsed_filters["contains_character"] not in rec.value:
            continue
        filtered.append(rec)

    return {
        "data": [
            {
                "id": r.id,
                "value": r.value,
                "properties": r.properties,
                "created_at": r.created_at
            }
            for r in filtered
        ],
        "count": len(filtered),
        "interpreted_query": {
            "original": query,
            "parsed_filters": parsed_filters,
        },
    }


@app.get("/strings/{string_value}")
def get_string(string_value: str, db: Session = Depends(get_db)):
    record = db.query(StringRecord).filter_by(value=string_value).first()
    if not record:
        raise HTTPException(status_code=404, detail="String not found")
    return {
        "id": record.id,
        "value": record.value,
        "properties": record.properties,
        "created_at": record.created_at
    }


@app.get("/strings")
def list_strings(
    is_palindrome: Optional[bool] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    word_count: Optional[int] = None,
    contains_character: Optional[str] = None,
    db: Session = Depends(get_db)
):
    records = db.query(StringRecord).all()

    # Apply filters
    filtered = []
    for rec in records:
        props = rec.properties
        if is_palindrome is not None and props["is_palindrome"] != is_palindrome:
            continue
        if min_length is not None and props["length"] < min_length:
            continue
        if max_length is not None and props["length"] > max_length:
            continue
        if word_count is not None and props["word_count"] != word_count:
            continue
        if contains_character is not None and contains_character not in rec.value:
            continue
        filtered.append(rec)

    filters_applied = {
        "is_palindrome": is_palindrome,
        "min_length": min_length,
        "max_length": max_length,
        "word_count": word_count,
        "contains_character": contains_character,
    }

    return {
        "data": [
            {
                "id": r.id,
                "value": r.value,
                "properties": r.properties,
                "created_at": r.created_at
            }
            for r in filtered
        ],
        "count": len(filtered),
        "filters_applied": {k: v for k, v in filters_applied.items() if v is not None},
    }


@app.delete("/strings/{string_value}", status_code=204)
def delete_string(string_value: str, db: Session = Depends(get_db)):
    record = db.query(StringRecord).filter_by(value=string_value).first()
    if not record:
        raise HTTPException(status_code=404, detail="String not found")
    db.delete(record)
    db.commit()
    return

