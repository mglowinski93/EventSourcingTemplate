from eventsourcing.application import Application

from .core import DATABASE_URL


class PersistentEventApplication(Application):
    env = {
        "PERSISTENCE_MODULE": "eventsourcing_sqlalchemy",
        "SQLALCHEMY_URL": DATABASE_URL,
    }
