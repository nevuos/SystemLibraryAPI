# messages_logger.py

# Mensagens relacionadas à verificação da conexão com a internet
ERROR_NO_INTERNET = "Sem conexão com a internet."
INFO_INTERNET_SUCCESS = "Conexão com a internet bem-sucedida."

# Mensagens relacionadas à verificação do banco de dados
ERROR_DATABASE_NOT_FOUND = "Banco de dados não encontrado."
INFO_DATABASE_NOT_FOUND = "Banco de dados não encontrado. Criando novo banco de dados..."
INFO_NEW_DATABASE_CREATED = "Novo banco de dados criado."
INFO_DATABASE_FOUND = "Banco de dados encontrado."

# Mensagens relacionadas à verificação de atualizações
INFO_UPDATE_AVAILABLE = "Nova versão {version} disponível."
INFO_UP_TO_DATE = "Está na versão mais recente."
INFO_UPDATE_SUCCESS = "Versão atualizada para {version}."
ERROR_REQUEST_FAILURE = "Falha na solicitação: {error}"
ERROR_CODE_UPDATE_FAILURE = "Erro ao atualizar o código: {error}"

# Mensagens relacionadas ao backup local
INFO_SOURCE_FOLDER_MISSING = "A pasta de origem {source_folder} não existe!"
INFO_BACKUP_FOLDER_CREATED = "Pasta de backup {backup_folder} criada com sucesso!"
INFO_BACKUP_CREATED_LOCALLY = "Backup de {zip_file_name} realizado localmente com sucesso!"

# Mensagens relacionadas ao backup no Supabase
INFO_BACKUP_FOLDER_MISSING = "A pasta de backup local {backup_folder} não existe!"
INFO_BACKUP_UPLOAD_SUCCESS = "Backup de {file_name} para Supabase realizado com sucesso!"
ERROR_BACKUP_UPLOAD_FAILURE = "Falha ao fazer backup de {file_name} para Supabase. Tentativa {attempt}. Erro: {error}"
