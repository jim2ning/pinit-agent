import json, math, os, sqlite3, statistics, urllib.request

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

def propose(goal, category, multiplier):
    endpoint, model, key = (os.environ.get(x) for x in ("AI_ENDPOINT", "AI_MODEL", "AI_API_KEY"))
    if not all((endpoint, model, key)):
        raise ValueError("AI_ENDPOINT, AI_MODEL, AI_API_KEY 환경 변수가 필요합니다.")
    prompt = f"목표: {goal}\n카테고리: {category}\n개인 보정 계수: {multiplier}. 목표를 현실적이고 구체적인 순서로 분해하세요. 각 항목은 완료 기준이 명확하며 base_minutes에 보정 계수를 곱해도 30분 이하여야 합니다. 작업을 생략하거나 시간을 줄여 표시하지 말고 더 작은 행동으로 나누세요. JSON만 반환: {{\"tasks\":[{{\"title\":\"...\",\"done_when\":\"...\",\"base_minutes\":15}}]}}"
    payload = json.dumps({"model": model, "messages": [{"role":"user", "content":prompt}]}).encode("utf-8")
    req = urllib.request.Request(endpoint, data=payload, headers={"Authorization":"Bearer "+key, "Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=60) as response:
        result = json.load(response)
    return validate(json.loads(result["choices"][0]["message"]["content"])["tasks"], multiplier)

def record(db, user, category, base, actual):
    if not user.strip() or not category.strip() or not all(math.isfinite(x) and 0 < x <= 1440 for x in (base, actual)):
        raise ValueError("사용자, 카테고리와 0보다 크고 1440 이하인 시간이 필요합니다.")
    db.execute("INSERT INTO history VALUES (?, ?, ?, ?)", (user, category, base, actual))
    db.commit()

