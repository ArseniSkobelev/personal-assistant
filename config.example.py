from lib.configlib import Config, KubernetesConfig, DatabaseConfig, TelegramConfig

sys_dev = Config()

sys_dev.kubernetes_config = KubernetesConfig(
    k8s_api_url="",
    k8s_healthz_url="",
    k8s_serviceaccount_token="",
    namespace="",  # optional
)

sys_dev.database_config = DatabaseConfig(
    db_host="",
    db_port="",
    db_user="",
    db_pass="",
    db_name="",
    db_auth_source="",
)

sys_dev.telegram_config = TelegramConfig(
    telegram_token="",
    allowed_users=[]
)

# /- Constants
BOT_NAME = 'TELEGRAM_BOT'
LOG_CONNECTOR = ': '
