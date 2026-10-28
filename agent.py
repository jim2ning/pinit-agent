import math, sqlite3, statistics

def connect(path="history.sqlite3"):
    db = sqlite3.connect(path)
    db.execute("CREATE TABLE IF NOT EXISTS history (user_id TEXT, category TEXT, base REAL, actual REAL)")
    return db

def factor(db, user, category):
    rows = db.execute("SELECT base, actual FROM history WHERE user_id=? AND category=? ORDER BY rowid DESC LIMIT 100", (user, category)).fetchall()
    ratios = [a/b for b, a in rows if b > 0 and a > 0]
    return (max(.5, min(3, statistics.median(ratios))) if len(ratios) >= 5 else 1), len(ratios)

def validate(items, multiplier):
    if not isinstance(items, list) or not 1 <= len(items) <= 50:
        raise ValueError("1~50개의 할 일이 필요합니다.")
    output = []
    for item in items:
        title, done, base = item.get("title"), item.get("done_when"), item.get("base_minutes")
        if not isinstance(title, str) or not title.strip() or not isinstance(done, str) or not done.strip() or isinstance(base, bool) or not isinstance(base, (int, float)) or not math.isfinite(base) or base <= 0:
            raise ValueError("제목, 완료 기준, 양수 시간이 필요합니다.")
        adjusted = math.ceil(base * multiplier)
        if adjusted > 30:
            raise ValueError("보정 후 30분 초과: 더 작은 할 일로 분해해야 합니다.")
        output.append({"title": title, "done_when": done, "base_minutes": base, "estimated_minutes": adjusted})
    return output

def record(db, user, category, base, actual):
    if not user.strip() or not category.strip() or not all(math.isfinite(x) and 0 < x <= 1440 for x in (base, actual)):
        raise ValueError("사용자, 카테고리와 0보다 크고 1440 이하인 시간이 필요합니다.")
    db.execute("INSERT INTO history VALUES (?, ?, ?, ?)", (user, category, base, actual))
    db.commit()


