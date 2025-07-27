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

python app/main.py
실행 코드

설치 코드
pip install -r requirements.txt

https://www.mongodb.com/try/download/community
.msi 설치

# MongoDB 서비스 상태 확인

net start | find "MongoDB"

# MongoDB 시작

net start MongoDB

MongoDB for VS Code vscode 확장자
