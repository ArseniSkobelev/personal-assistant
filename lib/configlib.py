class Config:
    def __init__(self):
        self.telegram_config = None
        self.kubernetes_config = None
        self.database_config = None


class TelegramConfig:
    def __init__(self, allowed_users, telegram_token, bot_name, log_separator):
        # telegram
        self.telegram_token = telegram_token
        self.allowed_users = allowed_users
        self.bot_name = bot_name
        self.log_separator = log_separator


class KubernetesConfig:
    def __init__(self, k8s_api_url, k8s_serviceaccount_token, k8s_healthz_url, namespace='personalhub'):
        # k8s
        self.k8s_api_url = k8s_api_url
        self.k8s_serviceaccount_token = k8s_serviceaccount_token
        self.k8s_healthz_url = k8s_healthz_url
        self.namespace = namespace

        self.k8s_api_url_namespaced = f"{self.k8s_api_url}/namespaces/{namespace}"


class DatabaseConfig:
    def __init__(self, db_host, db_port, db_user, db_pass, db_name, db_auth_source):
        # db
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name
        self.db_auth_source = db_auth_source


class DefaultValues:
    DEAFAULT_NAMESPACE = 'personalhub'
