"""FastAPI Application"""


from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.templating import Jinja2Templates

from .config import settings
from .draw_tile import generate_mvt_tile

templates = Jinja2Templates(directory=Path(__file__).parent.joinpath("templates"))

app = FastAPI(
    title="python-mvt-demo",
    description="Render Mapbox Vector Tile with Python",
    debug=settings.debug,
)


@app.get("/")
def home(request: Request) -> Response:
    return templates.TemplateResponse("mvt.html", {"request": request})


@app.get(
    "/tiles/{z}/{x}/{y}.mvt",
    response_class=Response,
    responses={200: {"content": {"application/vnd.mapbox-vector-tile": {}}}},
)
async def serve_tile(z: int, x: int, y: int) -> Response:
    serialized, render_time = generate_mvt_tile(z=z, x=x, y=y)
    if serialized:
        headers = {}
        if render_time < 30:
            headers["Cache-Control"] = "max-age=1"
        return Response(serialized, headers=headers)
    else:
        raise HTTPException(status_code=404)
