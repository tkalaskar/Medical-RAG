import sys


class CustomException(Exception):

    def __init__(self, message, error_details=None):
        super().__init__(message)

        self.error_message = self.get_detailed_error_message(
            message,
            error_details
        )
    @staticmethod
    def get_detailed_error_message(message, error_details):

        if error_details is None:
            return message

        _, _, exc_tb = sys.exc_info()

        if exc_tb is None:
            return message

        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        return (
            f"{message} | "
            f"Error: {error_details} | "
            f"File: {file_name} | "
            f"Line: {line_number}"
        )

    def __str__(self):
        return self.error_message