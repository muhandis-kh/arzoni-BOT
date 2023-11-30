from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config

class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        language_code varchar(5) null,
        date_of_registration date
        );
        """
        await self.execute(sql, execute=True)
    

    async def details(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Details (
        id SERIAL PRIMARY KEY,
        active_users INTEGER NULL,
        deactive_users INTEGER NULL,
        ads_text VARCHAR(255) NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_channels(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Channels (
        id SERIAL PRIMARY KEY,
        name varchar(100) NULL,
        username varchar(100) NULL,
        limit_user INTEGER Default 0,
        active Boolean default true
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id, language_code):
        sql = "INSERT INTO users (full_name, username, telegram_id, language_code, date_of_registration) VALUES($1, $2, $3, $4, NOW()::DATE) returning *"
        return await self.execute(sql, full_name, username, telegram_id, language_code, fetchrow=True)

    async def add_detail(self, active_users, deactive_users):
        sql = "INSERT INTO details (active_users, deactive_users) VALUES($1, $2) returning *"
        return await self.execute(sql, active_users, deactive_users, fetchrow=True)

    async def add_kino(self, kino_id, kino_name, kino_link):
        sql = "INSERT INTO kino (kino_id, kino_name, kino_link) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, kino_id, kino_name, kino_link, fetchrow=True)

    async def add_channel(self, name, username, limit_user):
        sql = "INSERT INTO channels (name, username, limit_user) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, name, username, limit_user, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)
    
    async def select_all_user_by_lang(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)
   

    async def select_all_details(self):
        sql = "SELECT * FROM Details"
        return await self.execute(sql, fetch=True)

    async def select_channels(self):
        sql = "SELECT * FROM Channels"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    
    async def select_all_user_count_by_lang(self, **kwargs):
        sql = "SELECT COUNT(*) FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_ids(self):
        sql = "SELECT * FROM Kino WHERE kino_id IS NOT NULL"
        return await self.execute(sql, fetch=True)
    
    async def select_id_kino(self):
        sql = "SELECT kino_id FROM Kino"
        return await self.execute(sql, fetch=True)
    
    async def select_kino_by_id(self, kino_id):
        sql = f"SELECT * FROM Kino WHERE kino_id LIKE '%{kino_id}%'"
        return await self.execute(sql, fetch=True)

    async def select_channel_by_id(self, channel_id):
        sql = f"SELECT * FROM Channels WHERE id={channel_id}"
        return await self.execute(sql, fetch=True)

    async def select_channel_by_username(self, username):
        sql = f"SELECT * FROM Channels WHERE username LIKE '%{username}%'"
        return await self.execute(sql, fetch=True)

    async def select_channel_is_active(self):
        sql = f"SELECT * FROM Channels WHERE active=True"
        return await self.execute(sql, fetch=True)

    async def delete_channel_by_username(self, username):
        sql = f"DELETE FROM Channels WHERE username LIKE '%{username}%'"
        return await self.execute(sql, fetch=True)
    
    async def count_users_by_month(self):
        sql = "SELECT DATE_TRUNC('MONTH', date_of_registration)::date m, COUNT(*) FROM Users GROUP BY m"
        return await self.execute(sql, fetch=True)
    
    async def count_users_by_day(self):
        sql = "SELECT DATE_TRUNC('DAY', date_of_registration)::date d, COUNT(*) FROM Users GROUP BY d"
        return await self.execute(sql, fetch=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def count_active_users(self):
        sql = "SELECT active_users FROM Details"
        return await self.execute(sql, fetchval=True)

    async def count_deactive_users(self):
        sql = "SELECT deactive_users FROM Details"
        return await self.execute(sql, fetchval=True)

    async def count_details(self):
        sql = "SELECT COUNT(*) FROM Details"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def update_channel(self, username, id):
        sql = "UPDATE Channels SET username=$1 WHERE id=$2"
        return await self.execute(sql, username, id, execute=True)

    async def update_active_users(self, active_users, id):
        sql = "UPDATE Details SET active_users=$1 WHERE id=$2"
        return await self.execute(sql, active_users, id, execute=True)

    async def update_deactive_users(self, deactive_users, id):
        sql = "UPDATE Details SET deactive_users=$1 WHERE id=$2"
        return await self.execute(sql, deactive_users, id, execute=True)

    async def update_mini_ads(self, text, id):
        sql = "UPDATE Details SET ads_text=$1 WHERE id=$2"
        return await self.execute(sql, text, id, execute=True)

    async def update_mini_ads_to_null(self, id):
        sql = "UPDATE Details SET ads_text=NULL WHERE id=$1"
        return await self.execute(sql, id, execute=True)

    async def deactive_channel(self, username):
        sql = "UPDATE Channels SET active=False WHERE username=$1"
        return await self.execute(sql, username, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)