from datetime import datetime
import logging


class Log():
    def __init__(self):
        self.fecha_actual = datetime.now().strftime('%m-%d-%G')
        logging.basicConfig(
            filename=f'logs_{self.fecha_actual}.log', 
            filemode='a',
            level=logging.DEBUG, 
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def create_log(self,type: str, text:str):
        logs = {
            "debug":logging.debug(text),
            "info":logging.info(text)
        }
        
        logs[type]

