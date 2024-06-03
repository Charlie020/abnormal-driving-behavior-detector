from pathlib import Path

from qfluentwidgets import QConfig, qconfig, ConfigItem, ConfigValidator, FolderValidator


class FileValidator(ConfigValidator):
    """
        由于 qfluentwidgets 中没有判别文件是否存在的校验器
        故自己写了个 File validator
    """

    def validate(self, value):
        return Path(value).exists()

    def correct(self, value):
        path = Path(value)
        if not path.exists():
            path.mkdir(exist_ok=True, parents=True)
        return str(path.absolute()).replace("\\", "/")


class MyConfig(QConfig):
    """ Config of application """
    # 配置项所在组、配置项名称、配置项默认值、判断配置项值是否合法的校验器
    logs_folder = ConfigItem("directory", "logs_folder", "logs", FolderValidator(), restart=True)
    resource_folder = ConfigItem("directory", "resource_folder", "resource", FolderValidator(), restart=True)
    result_folder = ConfigItem("directory", "result_folder", "result", FolderValidator(), restart=True)

    model_weight_path = ConfigItem("file", "model_weight_path", "resource/model_weight/best.pt", FileValidator(), restart=True)

