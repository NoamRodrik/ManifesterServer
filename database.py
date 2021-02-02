import pickledb
from glob import glob

class _VersionizedDatabase:
    _DB_PATTERN = "platform_manifest_"
    _DB_TYPE = ".json"

    def __init__(self):
        self._pickledb_database = {}
        self._load_all_versions()

    def reload_version(self, version):
        self._load_version(version)
        self._save_version(version)

    def has_version(self, version):
        return version in self._pickledb_database

    def to_dict(self, version):
        return self._pickledb_database[version].db

    def contains_key(self, version, key):
        return self._pickledb_database[version].exists(key)

    def get_by_key(self, version, key):
        return self._pickledb_database[version].get(key)

    def change_field_for_key(self, version, key, field, new_value):
        data = self.get_by_key(version, key)
        data[field] = new_value
        database.set_by_key(version, key, data)

    def remove_field_for_key(self, version, key, field):
        data = self.get_by_key(version, key)
        data.pop(field)
        database.set_by_key(version, key, data)

    def key_contains_field(self, version, key, field):
        return field in database.get_by_key(version, key)

    def get_field_by_key(self, version, key, field):
        return database.get_by_key(version, key)[field]

    def set_by_key(self, version, key):
        self._pickledb_database[version].set(key, data)
        self.save_version()

    def rm_by_key(self, version, key):
        self._pickledb_database[version].rem(key)
        self.save_version()

    def _load_all_versions(self):
        # Generating DBs for each platform manifest version #
        for db_file in glob(f'*{self._DB_PATTERN}*'):
            version = db_file.replace(self._DB_PATTERN, "").replace(self._DB_TYPE, "")
            self._load_version(version)

    def _load_version(self, version):
        self._pickledb_database[version] = pickledb.load(f'{self._DB_PATTERN}{version}.json', True, False)

    def _save_version(self, version):
        self._pickledb_database[version].dump()

# Global variables #
database = _VersionizedDatabase()
