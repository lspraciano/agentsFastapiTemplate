import os

from dynaconf import Dynaconf, Validator


class AppConfig:
    APP_ENV_VAR_PREFIX: str = "AGENTS_TEMPLATE"

    def __init__(self):
        self._root: str = self._resolve_root()
        self.settings: Dynaconf = self._build()

    @staticmethod
    def _resolve_root() -> str:
        current_dir: str = os.path.dirname(p=__file__)

        return os.path.abspath(
            path=os.path.join(
                current_dir,
                os.pardir,
            )
        )

    def _build(self) -> Dynaconf:
        return Dynaconf(
            root_path=self._root,
            envvar_prefix=self.APP_ENV_VAR_PREFIX,
            settings_files=[
                "./configuration/settings.toml",
                "./configuration/.secrets.toml",
            ],
            environments=[
                "production",
                "development",
                "sandbox",
            ],
            env_switcher=f"{self.APP_ENV_VAR_PREFIX}_ENVIRONMENT",
            validators=[
                Validator(
                    names="_ENVIRONMENT",
                    must_exist=True,
                )
            ],
            load_dotenv=False,
            sysenv_fallback=True,
        )


settings: Dynaconf = AppConfig().settings
