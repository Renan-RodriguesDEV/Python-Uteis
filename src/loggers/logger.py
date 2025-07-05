import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from colorama import Fore, Style, init

LOG_FILE_PATH = "logs/app.log"  # Caminho do arquivo de log

# Inicializa o colorama para cores no Windows
init(autoreset=True)

# Definir cores para os níveis de log
LOG_COLORS = {
    "DEBUG": Fore.BLUE,
    "INFO": Fore.GREEN,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
    "CRITICAL": Fore.MAGENTA + Style.BRIGHT,
}


# Criar um formatador personalizado com data/hora
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        record.asctime = self.formatTime(record, self.datefmt)
        log_color = LOG_COLORS.get(record.levelname, Fore.WHITE)
        log_message = (
            f"{Fore.CYAN}{record.asctime} {Fore.WHITE}[{record.filename}:{record.lineno}] "
            f"{log_color}[{record.levelname}] {log_color}{record.msg}{Style.RESET_ALL}"
        )
        return log_message


# Criar o logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)

# Criar o formatador com data/hora
formatter = ColoredFormatter(
    "[%(asctime)s] [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s"
)
formatter.default_time_format = "%Y-%m-%d %H:%M:%S"
formatter.default_msec_format = "%s.%03d"

# Manipulador para exibir no console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Manipulador para gravar em arquivo (geração diária)
# Certifique-se de que o diretório para os logs exista, por exemplo,
file_handler = TimedRotatingFileHandler(
    LOG_FILE_PATH, when="midnight", interval=1, backupCount=7, encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
