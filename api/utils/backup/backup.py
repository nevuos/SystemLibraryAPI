from api.utils.backup.backup_functions import backup_data_locally, backup_data_to_supabase


def do_backup(logger):
    backup_data_locally(logger)
    backup_data_to_supabase(logger)
