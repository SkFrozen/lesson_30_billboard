import logging
import time

logger = logging.getLogger("usersActivityLogger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("usersActivity.log")
formatter = logging.Formatter("%(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class usersActivityLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        username = request.user.username if request.user.username else "Anonymous"

        request_data = (
            f"{time.strftime("%m.%d.%Y %H:%M")} | "
            f"{username} | URL={request.get_full_path()}"
        )

        logger.info(request_data)

        return response
