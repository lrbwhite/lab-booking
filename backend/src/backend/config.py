from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    # 指定读取 .env 文件
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"   # 忽略.env里多余的变量，防止报错
    )

    # 数据库零散配置
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    # FastAPI 运行环境
    app_debug: bool = True

    @property
    def database_url(self) -> str:
        """自动拼接 SQLAlchemy 使用的数据库连接字符串"""
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


# 全局单例，项目其他地方直接 import 使用
config = Config()