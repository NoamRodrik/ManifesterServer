import json

class DatabaseQuery:
    def filter_by_fields(fields, database):
        return {key: database[key] for key in database if DatabaseQuery._dict_contain_fields(fields, database[key])}

    def filter_by_queries(queries, database):
        for query in queries:
            database = DatabaseQuery._filter_by_query(json.loads(query), database)
        return database

    def filter_by_names(names, database):
        return {key: database[key] for key in database if key in names}
    
    def _dict_contain_fields(fields, database):
        return all([field in database for field in fields])

    def _dict_in_dict(inner_database, outer_database):
        return all([(key, value) in outer_database.items() for (key, value) in inner_database.items()])

    def _filter_by_query(query, database):
        return {key: database[key] for key in database if DatabaseQuery._dict_in_dict(query, database[key])}
