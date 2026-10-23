import time 
from functools import wraps
from loggs.logger_config import logger

def log_tool(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("CHAMADA | %s | args=%s kwargs=%s", func.__name__, args, kwargs)
        inicio = time.perf_counter()
        try:
            resultado = func(*args, **kwargs)
            ms = (time.perf_counter() - inicio) * 1000
            logger.info("OK        | %s | %.0f ms | retorno=%s",
                        func.__name__, ms, str(resultado)[:300])
            return resultado
        except Exception:
            logger.exception("ERRO  | %s", func.__name__)
            raise
    return wrapper