# Pinit Agent

독립형 일정 분해 프로토타입. Python 3.10 이상과 OpenAI 호환 chat completions API가 필요합니다.

PowerShell에서 AI_ENDPOINT에 API 전체 URL, AI_MODEL에 모델명, AI_API_KEY에 키를 설정한 후 실행합니다.

    python main.py plan --user user1 --category 취업 --goal "자소서 작성"
    python main.py feedback --user user1 --category 취업 --base-minutes 15 --actual-minutes 20
    python -m unittest -v

완료한 작업의 base_minutes와 실제 시간을 기록하면 카테고리별 최근 100개 중 5개 이상일 때 실제/기본 예상 시간 비율 중앙값을 보정에 사용합니다. 기록이 적으면 보정 계수는 1입니다. 보정 후 30분을 넘는 AI 결과는 거부합니다. 30분은 예측이며 실제 완료를 보장하지 않습니다.

목표와 카테고리는 설정한 AI 제공자에 전송됩니다. 민감한 정보를 넣지 마세요. 기록은 로컬 history.sqlite3에 저장됩니다. 인증, 암호화, 계획 저장, 자동 재시도 및 Pinit 연동은 아직 구현되지 않았습니다. 공유 서버에 그대로 배포하지 마세요. 실제 AI 제공자 연결은 검증되지 않았습니다.

