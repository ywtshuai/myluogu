from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time
import json
from typing import Optional
from datetime import datetime


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 记录请求开始时间
        start_time = time.time()

        # 获取请求信息
        request_id = request.headers.get('X-Request-ID', '')
        path = request.url.path
        method = request.method
        query_params = dict(request.query_params)

        # 获取请求体（如果有）
        body = None
        if method in ['POST', 'PUT']:
            try:
                raw_body = await request.body()
                if raw_body:
                    body = json.loads(raw_body)
            except:
                body = "Could not parse body"

        # 记录请求日志
        logging.info(
            f"Request started | ID: {request_id} | {method} {path} | "
            f"Query Params: {query_params} | Body: {body}"
        )

        try:
            # 执行请求
            response = await call_next(request)

            # 计算处理时间
            process_time = time.time() - start_time

            # 记录响应日志
            logging.info(
                f"Request completed | ID: {request_id} | {method} {path} | "
                f"Status: {response.status_code} | Time: {process_time:.3f}s"
            )

            # 添加处理时间到响应头
            response.headers["X-Process-Time"] = str(process_time)
            return response

        except Exception as e:
            # 记录错误日志
            logging.error(
                f"Request failed | ID: {request_id} | {method} {path} | "
                f"Error: {str(e)}"
            )
            raise

        finally:
            # 记录请求结束
            logging.info(f"Request finished | ID: {request_id} | {method} {path}")