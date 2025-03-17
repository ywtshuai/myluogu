from fastapi import Depends, Query
from typing import Optional
import json
import base64
from app.core.exceptions import InvalidQueryError


async def get_query_params(
        query: Optional[str] = None,
        filter: Optional[str] = None,
        fields: Optional[str] = None,
        page: Optional[int] = Query(1, ge=1),
        page_size: Optional[int] = Query(10, ge=1, le=100),
        sort: Optional[str] = None
) -> dict:
    params = {
        "page": page,
        "page_size": page_size,
        "sort": sort
    }

    if query:
        try:
            params["query"] = json.loads(base64.b64decode(query))
        except:
            raise InvalidQueryError("Invalid query parameter")

    if filter:
        try:
            params["filter"] = json.loads(filter)
        except:
            raise InvalidQueryError("Invalid filter parameter")

    if fields:
        params["fields"] = fields.split(',')

    return params