import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message=error_message
        _,_,exc_tb=error_details.exc_info()

        self.lineno=exc_tb.tb_lineno
        self.filename=exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "Erro Occured in python script name [{0}] line number [{1}] erro message [{2}]".format(
            self.file_name,
            self.lineno,
            str(self.error_message)
        )

if __name__=="__main__":
    try:
        logger.logging.info("enter the try block")
        a=1/0
        print("this will not be printed")
        # we will see divide byzero error
    except Exception as e:
        raise NetworkSecurityException(e,sys)