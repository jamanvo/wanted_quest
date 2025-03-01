# Wanted Quest
---

# 구성
- docker compose를 이용해서 api서버 및 db를 구성했습니다.
- fastapi + sqlalchemy(+alembic) 을 이용했습니다.
- 테스트는 pytest를 이용했으며, 별도의 test db는 사용하지 않았습니다.
- 테스트 코드는 fastapi에서 사용하기 위한 일부 변화가 있습니다.

# 실행
- docker가 실행중인 머신이어야 합니다.
```bash
docker compose up --build
docker exec -it wanted_app bash
alembic upgrade head
python scripts/migrate_test_data.py
```
- 접속 가능한 포트는 8000 입니다.
