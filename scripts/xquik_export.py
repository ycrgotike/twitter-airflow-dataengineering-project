import csv
import json
from pathlib import Path


TEXT_FIELDS = ("text", "tweet", "full_text", "content", "body")
TIME_FIELDS = ("created_at", "published_at", "timestamp", "time")
COUNT_FIELDS = {
    "like_count": ("like_count", "favorite_count", "favorites", "likes"),
    "retweet_count": ("retweet_count", "retweets", "reposts"),
    "reply_count": ("reply_count", "replies"),
    "quote_count": ("quote_count", "quotes"),
}


def _first_value(record, fields, default=""):
    for field in fields:
        value = record.get(field)
        if value is not None and str(value).strip():
            return value
    return default


def _count_value(record, fields):
    value = _first_value(record, fields, 0)
    return int(value or 0)


def _json_records(raw_text, file_name):
    if file_name.endswith(".jsonl"):
        return [
            json.loads(line)
            for line in raw_text.splitlines()
            if line.strip()
        ]
    parsed = json.loads(raw_text)
    if isinstance(parsed, list):
        return parsed
    if isinstance(parsed, dict):
        for key in ("data", "tweets", "results", "items"):
            value = parsed.get(key)
            if isinstance(value, list):
                return value
        return [parsed]
    raise ValueError("Xquik export must be a JSON object or array.")


def _csv_records(raw_text):
    return list(csv.DictReader(raw_text.splitlines()))


def load_xquik_rows(export_path):
    path = Path(export_path)
    raw_text = path.read_text(encoding="utf-8-sig")
    suffix = path.suffix.lower()
    if suffix == ".csv":
        records = _csv_records(raw_text)
    elif suffix in {".json", ".jsonl"}:
        try:
            records = _json_records(raw_text, path.name.lower())
        except json.JSONDecodeError as exc:
            raise ValueError("Xquik JSON export contains invalid JSON.") from exc
    else:
        raise ValueError("Xquik export must be a .json, .jsonl, or .csv file.")

    rows = []
    for record in records:
        if not isinstance(record, dict):
            continue
        text = str(_first_value(record, TEXT_FIELDS)).strip()
        if not text:
            continue
        row = {
            "username": str(record.get("username") or record.get("user") or record.get("author") or "xquik"),
            "text": text,
            "created_at": _first_value(record, TIME_FIELDS),
            "lang": record.get("lang") or record.get("language") or "",
            "extracted_at": _first_value(record, ("extracted_at",), ""),
        }
        for output_field, input_fields in COUNT_FIELDS.items():
            row[output_field] = _count_value(record, input_fields)
        rows.append(row)
    return rows
