##**기타 메모메모(무시하세유)**
mongodb+srv://apple:1234@panguin5225.m6oav.mongodb.net/?retryWrites=true&w=majority&appName=Panguin5225
https://www.notion.so/Minhwa-Studio-2547cdb288bf80e7a18ee507a07335aa
pip install email-validator
pip install python-multipart
nodejs 20.15.1

# 설치할 때 필요한 명령어

python -m venv venv
pip install -r requirments.txt
pip install python-jose[cryptography] passlib[bcrypt]

# 실행할 때

uvicorn app.main:app --reload

backend/

│

├── app/

│ ├── main.py # FastAPI 서버 엔트리포인트

│ ├── api/

│ │ ├── routes/

│ │ │ ├── predict.py # /predict 라우터

│ │ │ └── user.py # /user 관련 라우터

│ │ └── deps.py # 의존성 주입 (예: DB 연결 등)

│ ├── core/

│ │ ├── config.py # 설정 파일 (env 변수 등)

│ │ └── model_loader.py # SD3 로딩 함수

│ ├── models/

│ │ └── user.py # MongoDB 모델 스키마 (Pydantic)

│ ├── services/

│ │ └── predict_service.py # 모델 추론 로직 분리

│ └── db/

│ ├── mongodb.py # MongoDB 연결 및 헬퍼

│ └── schemas/ # Pydantic 스키마 분리

│

├── .env # 환경변수 (Mongo URL 등)

├── requirements.txt

└── README.md
