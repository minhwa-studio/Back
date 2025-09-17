
---

# **민화사진관 Back (FastAPI)**

* **개요**: 사용자가 업로드한 사진을 민화풍으로 변환하고, 전시 데이터(개인/공용 전시관)를 관리하는 백엔드 서버
* **핵심 흐름**: 이미지 업로드 → AI 변환 요청 → 결과 저장 → 전시 등록/조회
* **기술**: FastAPI, MongoDB, Motor, Pydantic, JWT Auth
* **Front 연동**: REST API 제공 (변환, 유저 인증, 전시 관리)

---

## 1) 개요

* FastAPI 기반 백엔드
* MongoDB + Motor Async Client 연동
* 주요 기능:

  * 사용자 인증 (회원가입/로그인/JWT 발급)
  * 이미지 업로드 → 변환 서버 호출 (AI inference 서버와 통신)
  * 민화 전시관 관리 (개인 앨범/디지털 전시)

---

## 2) 주요 기능

### 2-1. 인증/Auth

* 회원가입
* 로그인 (JWT Access Token 발급)
* 토큰 검증 미들웨어
* 비밀번호 해싱(bcrypt)

### 2-2. 민화 변환

* 업로드된 이미지 파일 수신
* 변환 서버(`http://localhost:8500/generate`) 호출
* 변환된 이미지 저장 및 MongoDB 기록
* 결과 Response

### 2-3. 민화 전시관

* **나만의 전시관**

  * 내 변환 결과 조회
  * 전시 등록 (타이틀, 설명, 이미지 목록)
* **디지털 전시관**

  * 전시 목록 조회 (검색/정렬)
  * 전시 상세 조회 (작품, 작성자, 좋아요 등)

---

## 3) 기술 스택 & 아키텍처

* Framework: **FastAPI**
* DB: **MongoDB (motor async)**
* Auth: **JWT (PyJWT + bcrypt)**
* 모델 관리: **Pydantic**
* AI 연동: **외부 변환 서버 API 호출 ([http://localhost:8500/generate](http://localhost:8500/generate))**
* 배포: Docker, Uvicorn

---

## 4) 프로젝트 구조

```
Back-bepo-gwang/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── user.py        # 회원가입/로그인/유저 관리
│   │   │   ├── image.py       # 이미지 업로드, 변환 요청
│   │   │   ├── gallery.py     # 전시관 관련 API
│   │   └── __init__.py
│   ├── core/
│   │   ├── config.py          # 환경변수, 설정
│   │   ├── security.py        # JWT, 인증 관련
│   ├── db/
│   │   ├── mongodb.py         # Mongo 연결
│   ├── models/
│   │   ├── user.py            # UserModel
│   │   ├── image.py           # ImageModel
│   │   ├── exhibition.py      # ExhibitionModel
│   ├── services/
│   │   ├── minhwa_service.py  # 변환 서버 호출 로직
│   └── main.py                # FastAPI 엔트리포인트
├── .env                       # 환경 변수
├── requirements.txt
├── Dockerfile
```

---

## 5) 빠른 시작 (Windows cmd)

```cmd
# 백엔드 실행
0. 깃 클론
git clone <repo-url> minhwa-back
cd minhwa-back

1. 가상환경 생성 및 진입
python -m venv venv
.\venv\Scripts\activate

2. 의존성 설치
pip install -r requirements.txt

3. 환경 변수 설정 (.env)
MONGO_URI=mongodb://localhost:27017
MONGO_DB=minhwa
JWT_SECRET=your-secret-key
GENERATE_URL=http://localhost:8500/generate

4. 서버 실행
uvicorn app.main:app --reload --port 8000
```

---

## 6) API 엔드포인트

### Auth

* `POST /api/auth/register` → 회원가입
* `POST /api/auth/login` → 로그인 (JWT 발급)

### 변환

* `POST /api/image/upload` → 이미지 업로드 + 변환 요청
* `GET /api/image/{id}` → 변환 결과 조회

### 전시관

* `POST /api/gallery/my` → 나만의 전시관 등록
* `GET /api/gallery/my` → 내 전시 조회
* `GET /api/gallery/public` → 디지털 전시관 전체 조회
* `GET /api/gallery/{id}` → 특정 전시 상세

---

## 7) 화면 & 사용자 흐름 (백엔드 관점)

1. 사용자 로그인 → JWT 발급
2. 변환소: 사진 업로드 → AI 변환 서버 요청 → 변환 이미지 반환
3. 전시 등록: 내 앨범에서 작품 선택 → 전시 데이터 MongoDB 저장
4. 전시관 조회: 전체 전시 목록 제공 (검색/정렬 포함)

---
