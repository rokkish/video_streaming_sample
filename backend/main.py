from fastapi import FastAPI, HTTPException, Header, Response, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from pathlib import Path

app = FastAPI()
templates = Jinja2Templates(directory="templates")

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.htm", context={"request": request})

@app.get("/video", response_class=StreamingResponse)
async def read_video():
    video_path = Path("./test.mp4")

    if not video_path.exists():
        raise HTTPException(404, "not found video")

    def iterfile():
        with open(video_path, "rb") as f:
            yield from f

    return StreamingResponse(
        content=iterfile(),
        media_type="video/mp4"
    )

@app.get("/video_e", response_class=Response)
def video_endpoint(range: str = Header(None)):
    # https://stribny.name/blog/fastapi-video/
    CHUNK_SIZE = 1024*1024 // 2  # 1MB/2
    video_path = Path("./test.mp4")

    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE
    with open(video_path, "rb") as video:
        video.seek(start)
        data = video.read(end - start)
        filesize = str(video_path.stat().st_size)
        headers = {
            'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
            'Accept-Ranges': 'bytes'
        }
        return Response(data, status_code=206, headers=headers, media_type="video/mp4")
