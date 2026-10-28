# Pinit Agent

LangGraph와 OpenAI GPT를 사용하는 독립형 일정 분해 프로토타입입니다. Python 3.10 이상이 필요합니다.

## 설치와 실행

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    $env:OPENAI_API_KEY = "발급받은 API 키"
    $env:OPENAI_MODEL = "계정에서 사용 가능한 모델 ID"
    python main.py plan --user user1 --category 취업 --goal "자소서 작성"
    python main.py feedback --user user1 --category 취업 --base-minutes 15 --actual-minutes 20
    python -m unittest -v

API 키를 코드나 저장소에 넣지 마세요. API 사용에는 요금이 발생할 수 있습니다.

## 처리 흐름

LangGraph가 사용자·카테고리별 통계를 조회하고 GPT에 분해를 요청한 뒤, 보정된 시간이 30분을 초과하지 않는지 코드로 검증합니다. 실패 시 오류를 GPT에 전달하여 최대 3회까지 다시 요청하며, 계속 실패하면 결과를 저장하지 않고 오류를 반환합니다. 반환된 예상 시간은 보장된 완료 시간이 아닙니다.

완료한 작업의 base_minutes와 실제 시간을 feedback으로 기록합니다. 카테고리별 최근 100개 중 5개 이상이면 실제/기본 예상 시간 비율의 중앙값(0.5~3)을 적용하며, 기록이 부족하면 1을 적용합니다. 중단되거나 부분적으로 완료된 작업은 기록하지 마세요.

목표와 카테고리, 보정 계수는 OpenAI에 전송됩니다. 개인별 원본 기록과 user ID는 전송하지 않습니다. 개인 기록은 로컬 history.sqlite3에 저장됩니다. 이는 단일 사용자 프로토타입으로, 인증·암호화·Pinit 연동·계획 저장 기능이 없습니다. 공유 서버에 그대로 배포하지 마세요. 실제 GPT 호출은 API 키가 필요합니다.


## PyCharm에서 API 키 설정

프로젝트 폴더에서 .env.example을 .env로 복사하고 .env 파일에 API 키를 직접 입력합니다.
OPENAI_MODEL은 계정에서 사용할 수 있는 모델 ID로 바꿀 수 있습니다. .env는 Git에 포함되지 않습니다.
이미 설정된 환경 변수는 .env보다 우선합니다. 키를 채팅이나 GitHub에 올리지 마세요.
PyCharm의 Python 인터프리터에서 requirements.txt 패키지를 설치한 다음 실행합니다.
