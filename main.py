import argparse, json, sys
from agent import connect, record
from graph_agent import plan

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)
    for name in ("plan", "feedback"):
        c = sub.add_parser(name)
        c.add_argument("--user", required=True)
        c.add_argument("--category", required=True)
        if name == "plan": c.add_argument("--goal", required=True)
        else:
            c.add_argument("--base-minutes", type=float, required=True)
            c.add_argument("--actual-minutes", type=float, required=True)
    a = p.parse_args()
    with connect() as db:
        if a.command == "plan":
            print(json.dumps(plan(db, a.user, a.category, a.goal), ensure_ascii=False, indent=2))
        else:
            record(db, a.user, a.category, a.base_minutes, a.actual_minutes)
            print("기록했습니다.")

if __name__ == "__main__":
    try: main()
    except Exception as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)

