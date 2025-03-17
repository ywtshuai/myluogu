from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import NodeNotFoundError, InvalidQueryError, DatabaseError

async def error_handler(request: Request, exc: Exception):
    if isinstance(exc, NodeNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"error": str(exc)}
        )
    elif isinstance(exc, InvalidQueryError):
        return JSONResponse(
            status_code=400,
            content={"error": str(exc)}
        )
    elif isinstance(exc, DatabaseError):
        return JSONResponse(
            status_code=500,
            content={"error": "Database error occurred"}
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )