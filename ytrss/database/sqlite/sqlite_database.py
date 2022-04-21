import os
import sqlite3
from contextlib import contextmanager
from sqlite3 import Connection
from typing import Iterable, Iterator

from ytrss.configuration.configuration import Configuration
from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.core.entity.movie import Movie

from ytrss.database.database import Database, DatabaseStatus
from ytrss.database.entity.movie_task import MovieTask


class SqliteDatabase(Database):
    """
    Database implementation in sqlite3
    """

    @contextmanager
    def _database_handler(self) -> Iterator[Connection]:
        conn = sqlite3.connect(self._db_file)
        yield conn
        conn.close()

    def __init__(self, configuration: Configuration):
        self.__configuration = configuration
        self._db_file = os.path.join(configuration.conf.config_path, "ytrss.db")
        with self._database_handler() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS movies_tasks (
                    identity TEXT NOT NULL UNIQUE,
                    url TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    try INT DEFAULT 0,
                    state CHAR(10) DEFAULT "wait",
                    comment TEXT
                )
            ''')

    def change_type(self, movie: Movie, db_type: DatabaseStatus) -> None:
        with self._database_handler() as conn:
            conn.execute(f'''
                UPDATE movies_tasks
                set state = "{db_type.value}"
                where identity = "{movie.identity}"
            ''')
            conn.commit()

    def is_new(self, movie: Movie, destination: DestinationId) -> bool:
        with self._database_handler() as conn:
            cursor = conn.execute(f'''
                SELECT identity
                FROM movies_tasks
                WHERE identity = "{movie.identity}" and (state = "wait" or state = "error" or state = "progress")
            ''')
            rows = cursor.fetchall()
        return len(rows) > 0

    def movies(self) -> Iterable[MovieTask]:
        with self._database_handler() as conn:
            cursor = conn.execute('''
                SELECT identity, url, destination
                FROM movies_tasks
                WHERE state = "wait" or state = "error"
            ''')
            rows = cursor.fetchall()

        for row in rows:
            movie_task = MovieTask.from_json({
                "id": row[0],
                "url": row[1],
                "destination": row[2]
            })
            if self.is_new(movie_task.movie, movie_task.destination):
                yield movie_task

    def queue_mp3(self, movie: Movie, destination: DestinationId) -> bool:
        """
        Add address to download.
        """
        try:
            with self._database_handler() as conn:
                conn.execute(f'''
                    INSERT INTO movies_tasks (identity, url, destination)
                    VALUES ('{movie.identity}', '{movie.url}', '{destination}')
                ''')
                conn.commit()
        except sqlite3.IntegrityError:
            return False
        return True
