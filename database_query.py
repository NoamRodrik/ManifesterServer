from utilities import make_args_hashable
from functools import lru_cache
import json

class DatabaseQuery:
    @make_args_hashable
    @lru_cache()
    def filter_by_fields(fields, db):
        return {key: dict(db[key]) for key in db if DatabaseQuery._dict_contain_fields(fields, db[key])}

    @make_args_hashable
    @lru_cache()
    def filter_by_queries(queries, db):
        for query in queries:
            db = DatabaseQuery._filter_by_query(json.loads(query), db)
        return db

    @make_args_hashable
    @lru_cache()
    def filter_by_names(names, db):
        return {key: dict(db[key]) for key in db if key in names}

    @make_args_hashable
    @lru_cache()
    def _dict_contain_fields(fields, db):
        return all([field in db for field in fields])

    @make_args_hashable
    @lru_cache()
    def _dict_in_dict(inner_db, outer_db):
        return all([(key, value) in outer_db.items() for (key, value) in inner_db.items()])

    @make_args_hashable
    @lru_cache()
    def _filter_by_query(query, db):
        return {key: dict(db[key]) for key in db if DatabaseQuery._dict_in_dict(query, db[key])}

    @make_args_hashable
    @lru_cache()
    def _filter_by_query_not(query, db):
        return {key: dict(db[key]) for key in db if not DatabaseQuery._dict_in_dict(query, db[key])}
