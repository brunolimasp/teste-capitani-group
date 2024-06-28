import json
import os

import pandas as pd
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy import URL, create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from ..models.product import Product
load_dotenv()


class DataBase:
    def __init__(self):
        self.url_object = URL.create(
            os.getenv("DB_ENGINE"),
            username=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_DATABASE"),
        )
        # Tenta conectar ao banco de dados
        try:
            self.db = create_engine(self.url_object)
            self.cursor = self.db.connect()

            # 4. Crie as tabelas no banco de dados
            Product.metadata.create_all(self.db)
            print(
                f"The database {os.getenv('DB_DATABASE')} connection has been established!"
            )
        except SQLAlchemyError as err:
            print(f"Failed to try connect to the bank, {err}")

    def execute(self, query):
        try:
            with self.db.connect() as connection:
                
                if 'select' in query.lower() or "returning" in query.lower():
                    data = json.loads(
                        pd.read_sql(text(query), connection).to_json(orient="records")
                    )
                    if data == []:
                        return None
                    return data
                elif 'insert' in query.lower() or 'update' in query.lower():

                    result = connection.execute(text(query))
                    affected_rows = result.rowcount
                    connection.commit()
                    if affected_rows == 0:
                        raise HTTPException(
                            status_code=417,
                            detail=f"No rows were affected by the operation.",
                        )
                    return {
                        "status": "Success",
                        "message": f"Operation completed successfully, {affected_rows} lines were changed",
                    }

        except SQLAlchemyError as err:
            print(f"Failed to execute query: {err}")
            raise HTTPException(
                status_code=500, detail=f"Failed to execute query: {err}"
            )


db = DataBase()
