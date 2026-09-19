from datetime import UTC, datetime
from pathlib import Path

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
templates.env.filters["fecha"] = lambda segundos: (
    datetime.fromtimestamp(segundos, UTC).date().isoformat()
)
