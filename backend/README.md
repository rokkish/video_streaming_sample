## Minimum stream video with FastAPI
```console
cd backend
# put file as backend/test.mp4
uv sync
uv run uvicorn main:app --host localhost --port 8000 --reload
```
open http://localhost:8000/
