import logging

from src.services.startup_service import init_admin_user

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] - [%(levelname)s]: %(message)s')


def on_starting(server):
    init_admin_user()
    logging.info("Server has started")
