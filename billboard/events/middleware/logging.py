import logging
import time
from datetime import datetime

logging.basicConfig(
    filename="usersActivity.log", level=logging.NOTSET, format="%(message)s"
)


class usersActivityLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        username = request.user.username if request.user.username else "Anonymous"

        request_data = f"{time.strftime("%m.%d.%Y %H:%M")} | " \
                            f"{username} | URL={request.get_full_path()}"

        logging.info(request_data)

        return response
