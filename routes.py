import flask
from flask import request, jsonify
from database import database
from database_query import DatabaseQuery
from reponses import ErrorResponses, SuccessResponses
from frozendict import frozendict
from utilities import filter_by_arglist

####################
# Global variables #
####################
_flask_application = flask.Flask(__name__)
_flask_application.config["DEBUG"] = True

@_flask_application.errorhandler(404)
def _route_page_not_found(error):
    return ErrorResponses.not_found_error(error)

@_flask_application.route('/', methods=['GET'])
def _route_home():
    return ErrorResponses.home_page_error()

@_flask_application.route('/<version>', methods=['GET'])
def _route_get_all_platforms(version):
    if not version:
        return ErrorResponses.version_not_inputted()
    
    if not database.has_version(version):
        return ErrorResponses.version_doesnt_exist(version)

    db = database.to_dict(version)
    db = filter_by_arglist('field', DatabaseQuery.filter_by_fields,  db)
    db = filter_by_arglist('q',     DatabaseQuery.filter_by_queries, db)
    db = filter_by_arglist('name',  DatabaseQuery.filter_by_names,   db)

    return db

@_flask_application.route('/<version>/<platform_name>', methods=['GET'])
def _route_get_platform(version, platform_name):
    if not version or not platform_name:
        return ErrorResponses.version_or_name_not_inputted()

    if not database.has_version(version):
        return ErrorResponses.version_doesnt_exist(version)

    if not database.contains_key(version, platform_name):
        return ErrorResponses.platform_not_found(platform_name)

    return database.get_by_key(version, platform_name)

@_flask_application.route('/<version>/<platform_name>', methods=['POST'])
def _route_add_platform(version, platform_name):
    if not version or not platform_name:
        return ErrorResponses.version_or_name_not_inputted()

    if not database.has_version(version):
        return ErrorResponses.version_doesnt_exist(version)

    if not database.contains_key(version, platform_name):
        return ErrorResponses.platform_already_exists(platform_name)

    database.set_by_key(version, platform_name, dict())
    return SuccessResponses.successfully_added_platform()

@_flask_application.route('/<version>/<platform_name>', methods=['DELETE'])
def _route_remove_platform(version, platform_name):
    if not version or not platform_name:
        return ErrorResponses.version_or_name_not_inputted()

    if not database.has_version(version):
        return ErrorResponses.version_doesnt_exist(version)

    if not database.contains_key(version, platform_name):
        return ErrorResponses.platform_not_found(platform_name)

    database.rm_by_key(version, platform_name)
    return SuccessResponses.successfully_removed_platform()

@_flask_application.route('/<version>/<platform_name>/<field>', methods=['POST'])
def _route_change_platform_field(version, platform_name, field):
    if not version or not platform_name or not field:
        return ErrorResponses.version_name_or_field_not_inputted()

    if not database.has_version(version):
        return ErrorResponses.version_doesnt_exist(version)

    value = request.form.get('value')
    if not value:
        return ErrorResponses.missing_value_in_form()

    # If platform doesn't exist, give it a default value.
    if not database.contains_key(version, platform_name):
        database.set_by_key(version, platform_name, dict())

    database.change_field_for_key(version, platform_name, field, value)
    return SuccessResponses.successfully_changed_field()

@_flask_application.route('/<version>/<platform_name>/<field>', methods=['DELETE'])
def _route_remove_platform_field(version, platform_name, field):
    if not version or not platform_name or not field:
        return ErrorResponses.version_name_or_field_not_inputted()

    if not database.has_version(version):
        return ErrorResponses.version_doesnt_exist(version)

    if not database.contains_key(version, platform_name):
        return ErrorResponses.platform_not_found(platform_name)

    if not database.key_contains_field(version, platform_name, field):
        return ErrorResponses.field_missing_for_platform(field, platform_name)

    database.remove_field_for_key(version, platform_name, field)
    return SuccessResponses.successfully_removed_field()

@_flask_application.route('/<version>/<platform_name>/<field>', methods=['GET'])
def _route_get_field(version, platform_name, field):
    if not version or not platform_name or not field:
        return ErrorResponses.version_name_or_field_not_inputted()

    if not database.has_version(version):
        return ErrorResponses.version_doesnt_exist(version)

    if not database.contains_key(version, platform_name):
        return ErrorResponses.platform_not_found(platform_name)

    if not database.key_contains_field(version, platform_name, field):
        return ErrorResponses.field_missing_for_platform(field, platform_name)

    return database.get_field_by_key(version, platform_name, field)

@_flask_application.route('/<version>/load', methods=['GET'])
def _route_load(version):
    if not version:
        return ErrorResponses.version_not_inputted()

    database.reload_version(version)
    return SuccessResponses.successfully_loaded_version()

def run_flask():
    _flask_application.run()
