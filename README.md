# INSTRING Backend

> INSTRING 서비스의 백엔드 API 서버

INSTRING Backend는 기타 연습 및 관리 서비스 **INSTRING**의 서버 애플리케이션입니다.  
이 저장소는 사용자 인증, 곡 검색 및 추천, 녹음 데이터 관리, AI 분석 결과 처리, ESP32 디바이스 및 프론트엔드와의 실시간 통신 기능을 제공합니다.

---

## Overview

INSTRING Backend는 FastAPI 기반으로 구현된 서버입니다.  
REST API와 WebSocket을 통해 프론트엔드 및 ESP32 디바이스와 통신하며, PostgreSQL, Redis, AWS S3와 연동하여 서비스의 핵심 데이터를 처리합니다.

백엔드는 다음 역할을 담당합니다.

- 사용자 회원가입, 로그인, 토큰 인증 처리
- 곡 정보 조회, 검색, 추천 API 제공
- 녹음 파일 업로드 및 분석 결과 저장
- ESP32 디바이스와의 실시간 센서/오디오 데이터 통신
- PostgreSQL, Redis, AWS S3 등 외부 인프라 연동

이 문서는 **INSTRING 백엔드 서버 저장소 기준 README**입니다.  
프론트엔드 UI, ESP32 펌웨어 구현, AI 모델 학습 파이프라인 자체는 이 저장소의 주된 범위에 포함하지 않습니다.

---

## Scope

### Included

- 인증 및 인가
- 사용자 정보 관리
- 곡 검색 및 추천 API
- 녹음 데이터 저장 및 조회
- AI 분석 결과 처리 및 반환
- 실시간 WebSocket 통신
- DB, Redis, S3 연동
- 서버 실행 및 배포 설정

### Excluded

- 프론트엔드 UI 구현
- ESP32 펌웨어 및 하드웨어 회로 구성
- AI 모델 학습 파이프라인
- 디자인 리소스 및 화면 설계

---

## Features

### Authentication

- JWT 기반 Access / Refresh Token 인증
- 이메일 OTP 인증
- Redis 기반 Refresh Token 관리
- 로그아웃 시 Access Token blacklist 처리
- Argon2 기반 비밀번호 해싱

### Song Search

- PostgreSQL Full-Text Search 기반 검색
- `pg_trgm` 기반 오타 허용 검색
- 카테고리별 곡 조회
- 곡 상세 정보 및 연습용 YouTube 링크를 통해 프론트에서 유튜브프레임 api로 접근

### Recommendation

- 사용자 레벨, 클릭 기록, 연주 이력 기반 추천
- 난이도 및 선호도 반영
- 분석된 연주 결과와 유사한 곡 추천

### Recording & Analysis

- 녹음 파일 업로드 처리
- 분석 결과(코드, 주법, BPM) 저장
- 녹음 목록 / 상세 조회 / 검색 / 수정 / 삭제 API 제공

### Device Integration

- ESP32 디바이스 연결 상태 관리
- 온습도 데이터 수신 및 프론트 실시간 중계
- 녹음 바이너리 데이터 수신
- 녹음 완료 이벤트 처리

---

## Tech Stack

| Category | Tech |
|---|---|
| Framework | FastAPI |
| Language | Python 3.13 |
| ORM | SQLModel / SQLAlchemy |
| Database | PostgreSQL |
| Cache | Redis |
| Storage | AWS S3 |
| AI / Audio | PyTorch, librosa, NumPy |
| Auth | PyJWT, pwdlib (Argon2) |
| Migration | Alembic |
| Mail | FastAPI-Mail |
| Deploy | Docker, Docker Compose |
| Package Manager | uv |

---

## Architecture

~~~text
[ Frontend ]
     │
     │ REST API / WebSocket
     ▼
[ FastAPI Backend ]
     ├─ PostgreSQL
     ├─ Redis
     ├─ AWS S3
     └─ ESP32 Device (WebSocket)
~~~

### Communication

- **Frontend ↔ Backend**
  - REST API: 사용자, 곡, 추천, 녹음 데이터 처리
  - WebSocket: 실시간 온습도, 녹음 완료 이벤트 수신

- **ESP32 ↔ Backend**
  - WebSocket: 센서 데이터 및 녹음 데이터 전송

---

## Project Structure

~~~text
INewApp/
├── main.py                         # FastAPI 앱 진입점
├── core/
│   ├── config.py                   # 환경변수 설정
│   ├── db_engine.py                # DB 엔진 설정
│   ├── dependencies.py             # 공통 의존성 주입
│   ├── middlewares.py              # 미들웨어 및 CORS
│   ├── redis_set.py                # Redis 연결
│   ├── connect_s3.py               # S3 연결
│   ├── security/
│   │   ├── jwt_token.py            # JWT 처리
│   │   └── auth_mange.py           # 인증, OTP, 비밀번호 처리
│   └── error/
│       ├── exceptions.py
│       ├── exception_messages.py
│       └── exception_handlers.py
│
├── common/
│   ├── base_model.py               # 공통 모델
│   ├── common_models/              # 공통 테이블/링크 테이블
│   └── utils/                      # 공용 유틸리티
│
└── domains/
    ├── users/                      # 사용자 도메인
    ├── song/                       # 곡 검색/추천 도메인
    ├── record/                     # 녹음 도메인
    ├── device/                     # 디바이스 및 소켓 도메인
    ├── ai/                         # AI 추론 관련 코드
    └── infos/                      # 카테고리/레벨/기타줄 정보
~~~

---

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- AWS S3 버킷
- SMTP 메일 서버

### 1. 환경변수 설정

~~~bash
cp .env .env.docker
~~~

`.env.docker` 파일에 아래 값을 설정합니다.

~~~env
# Database
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432
DB_NAME=instring

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# JWT
KEY=your_jwt_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
REFRESH_TOKEN_EXPIRE_SECONDS=604800

# Guitar String
STRING_MAX_DAY=30

# Mail
MAIL_USERNAME=your_email
MAIL_PASSWORD=your_app_password
MAIL_FROM=your_email
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
USE_CREDENTIALS=True
VALIDATE_CERTS=True

# AWS S3
S3_BUCKET_NAME=your_bucket
AWS_ACCESS_KEY=your_access_key
AWS_SECRET_KEY=your_secret_key
AWS_REGION=ap-northeast-2

# CORS
CORS_ORIGINS=["http://localhost:3000"]
~~~

### 2. 컨테이너 실행

~~~bash
docker compose up --build -d
~~~

### 3. 데이터베이스 마이그레이션

~~~bash
docker compose exec app uv run alembic upgrade head
~~~

### 4. 실행 확인

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## API Summary

### Auth

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/email_check` | 이메일 중복 확인 및 OTP 발송 | - |
| POST | `/check_otp` | OTP 검증 | - |
| POST | `/join` | 회원가입 | - |
| POST | `/auth/login` | 로그인 | - |
| POST | `/auth/logout` | 로그아웃 | Bearer |
| POST | `/refresh` | 토큰 재발급 | - |

### User

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/modal_check` | 초기 설문 여부 확인 | Bearer |
| POST | `/modal_add` | 초기 설문 제출 | Bearer |
| GET | `/user/level` | 사용자 레벨 조회 | Bearer |
| GET | `/user/string-status` | 기타줄 상태 조회 | Bearer |
| PATCH | `/change_level` | 레벨 변경 | Bearer |
| PATCH | `/change_string` | 기타줄 교체 처리 | Bearer |
| POST | `/change_info_check` | 비밀번호 변경용 이메일 인증 | - |
| POST | `/change/check_otp` | 비밀번호 변경용 OTP 검증 | - |
| PATCH | `/change_password` | 비밀번호 변경 | Temp |
| DELETE | `/user_delete` | 회원 탈퇴 | Bearer |

### Song

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/song/{song_id}` | 곡 상세 조회 | - |
| GET | `/songs/search?q=&limit=` | 곡 검색 | - |
| GET | `/search/category/{ca_id}` | 카테고리별 곡 조회 | - |
| GET | `/song/recommend?limit=` | 개인화 추천 | Bearer |
| POST | `/song_contain` | 곡 등록 | - |
| GET | `/user/song/click/{song_id}` | 곡 클릭 기록 | Bearer |

### Record

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/record/list` | 녹음 목록 조회 | Bearer |
| GET | `/record/info/{record_id}` | 녹음 상세 조회 | Bearer |
| GET | `/records/search?q=&limit=` | 녹음 검색 | Bearer |
| PATCH | `/record/change/info/{record_id}` | 녹음 이름 수정 | Bearer |
| DELETE | `/record/delete/info/{record_id}` | 녹음 삭제 | Bearer |

### Device

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/device/check` | 등록 여부 확인 | Bearer |
| POST | `/device/register` | 디바이스 등록 | Bearer |
| DELETE | `/device/unregister` | 디바이스 등록 해제 | Bearer |

---

## WebSocket

| Endpoint | Description |
|---|---|
| `ws://host/ws/device/{device_id}` | ESP32 디바이스 연결 |
| `ws://host/ws/front?token=` | 프론트 실시간 연결 |

### Usage

- 디바이스 → 서버: 온습도 데이터, 녹음 바이너리 데이터 전송
- 서버 → 프론트: 실시간 센서값 중계, 녹음 완료 알림 전달

---

## Storage Responsibilities

### PostgreSQL

- 사용자, 곡, 녹음, 카테고리 등 핵심 데이터 저장
- 곡 검색용 인덱스 및 검색 벡터 관리

### Redis

- Refresh Token 저장
- Access Token blacklist 처리
- OTP 인증 코드 관리

### AWS S3

- 녹음 파일 저장
- 스펙트로그램 이미지 저장
- AI 모델 파일 관리

---

## AI Analysis

백엔드는 업로드되거나 수신된 오디오 데이터를 기반으로 아래 분석 결과를 처리합니다.

- 코드 인식
- 주법 분류
- BPM 추정

분석 결과는 저장 후 API 응답 또는 상세 조회 기능을 통해 제공합니다.

> 모델에 대한 자세한 내용은 AI 리드미를 참고하세요
---

## Notes

- API 상세 명세는 Swagger UI(`/docs`)에서 확인할 수 있습니다.
- 이 README는 백엔드 서버 저장소 기준 문서입니다.
- 서비스 전체 소개, 프론트엔드 구조, ESP32 펌웨어 상세 설명은 별도 프로젝트 문서에서 다루는 것을 권장합니다.

---

## License

이 프로젝트는 비공개 프로젝트입니다.
