import logging

def setup_logging():
    logger = logging.getLogger("barbearia")
    logger.setLevel(logging.INFO)
    if logger.handlers:
        return logger

    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s", "%d/%m/%Y : %H:%M:%S"
    )

    arquivo = logging.FileHandler("mcp_tools.log", encoding='utf-8')
    arquivo.setFormatter(formato)
    logger.addHandler(arquivo)
    return logger

logger = setup_logging()