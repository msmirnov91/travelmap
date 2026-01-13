from dotenv import load_dotenv


def load_env_vars(base_dir=None):
    load_dotenv('.env.common')
    load_dotenv('.env', override=True)
