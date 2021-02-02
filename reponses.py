class ErrorResponses:
    def not_found_error(error):
        return f"No API exists: {error}.\n", 404

    def home_page_error():
        return f"Please route to a specific version.\n", 500

    def version_not_inputted():
        return f"Please insert the version.\n", 500

    def version_or_name_not_inputted():
        return f"Please insert the version and name.\n", 500

    def version_name_or_field_not_inputted():
        return f"Please insert the version name and field.\n", 500

    def version_doesnt_exist(version):
        return f"Version {version} doesn't exist.\n", 404

    def platform_not_found(platform_name):
        return f"Cannot find the requested platform {platform_name}.\n", 404

    def platform_already_exists(platform_name):
        return f"Platform {platform_name} already exists.\n", 500

    def field_missing_for_platform(field, platform_name):
        return f"Cannot find the requested field {field} for platform {platform_name}.\n", 404

    def missing_value_in_form():
        return f"Please assign the argument 'value' as a POST argument.\n", 500

class SuccessResponses:
    def successfully_added_platform():
        return f"Successfully added a platform.\n", 200

    def successfully_removed_platform():
        return f"Successfully removed a platform.\n", 200

    def successfully_changed_field():
        return f"Successfully changed a platform's field (and added the platform if it didn't exist).\n", 200

    def successfully_removed_field():
        return f"Successfully removed a platform's field.\n", 200

    def successfully_loaded_version():
        return f"Successfully loaded version!\n", 200
