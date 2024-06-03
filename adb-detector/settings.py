from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFileDialog
from qfluentwidgets import PushSettingCard, FluentIcon, qconfig, SettingCardGroup, Flyout, InfoBarIcon, \
    FlyoutAnimationType
from utils.config import MyConfig


class Settings(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text.replace(' ', '-'))

        self.cfg = MyConfig()
        qconfig.load('config.json', self.cfg)

        self.logs_card = PushSettingCard(
            '选择文件夹',
            FluentIcon.FOLDER,
            '日志文件夹',
            self.cfg.get(self.cfg.logs_folder)
        )
        self.logs_card.clicked.connect(self.choose_logs_folder)

        self.resource_card = PushSettingCard(
            '选择文件夹',
            FluentIcon.FOLDER,
            '资源文件夹',
            self.cfg.get(self.cfg.resource_folder)
        )
        self.resource_card.clicked.connect(self.choose_resource_folder)

        self.result_card = PushSettingCard(
            '选择文件夹',
            FluentIcon.FOLDER,
            '导出检测结果文件夹',
            self.cfg.get(self.cfg.result_folder)
        )
        self.result_card.clicked.connect(self.choose_result_folder)

        self.model_weight_card = PushSettingCard(
            '选择文件',
            FluentIcon.DOCUMENT,
            '权重文件',
            self.cfg.get(self.cfg.model_weight_path)
        )
        self.model_weight_card.clicked.connect(self.choose_model_weight)

        self.setting_group = SettingCardGroup('默认文件夹路径')
        self.setting_group.addSettingCard(self.logs_card)
        self.setting_group.addSettingCard(self.resource_card)
        self.setting_group.addSettingCard(self.result_card)
        self.setting_group.addSettingCard(self.model_weight_card)

        layout = QVBoxLayout()
        layout.addWidget(self.setting_group)
        self.setLayout(layout)

    def choose_logs_folder(self):
        path = QFileDialog.getExistingDirectory(self, '选择文件夹')
        if path:
            self.logs_card.setContent(path)
            self.cfg.set(self.cfg.logs_folder, path)
            Flyout.create(
                icon=InfoBarIcon.WARNING,
                title='提示',
                content="更改内容将在重启程序后生效！",
                target=self.logs_card,
                parent=self,
                isClosable=True,
                aniType=FlyoutAnimationType.PULL_UP
            )

    def choose_resource_folder(self):
        path = QFileDialog.getExistingDirectory(self, '选择文件夹')
        if path:
            self.resource_card.setContent(path)
            self.cfg.set(self.cfg.resource_folder, path)
            Flyout.create(
                icon=InfoBarIcon.WARNING,
                title='提示',
                content="更改内容将在重启程序后生效！",
                target=self.resource_card,
                parent=self,
                isClosable=True,
                aniType=FlyoutAnimationType.PULL_UP
            )

    def choose_result_folder(self):
        path = QFileDialog.getExistingDirectory(self, '选择文件夹')
        if path:
            self.result_card.setContent(path)
            self.cfg.set(self.cfg.result_folder, path)
            Flyout.create(
                icon=InfoBarIcon.WARNING,
                title='提示',
                content="更改内容将在重启程序后生效！",
                target=self.result_card,
                parent=self,
                isClosable=True,
                aniType=FlyoutAnimationType.PULL_UP
            )

    def choose_model_weight(self):
        path, _ = QFileDialog.getOpenFileName(self, '选择文件', '', 'Weight (*.pt *.pth)')
        if path:
            self.model_weight_card.setContent(path)
            self.cfg.set(self.cfg.model_weight_path, path)
            Flyout.create(
                icon=InfoBarIcon.WARNING,
                title='提示',
                content="更改内容将在重启程序后生效！",
                target=self.model_weight_card,
                parent=self,
                isClosable=True,
                aniType=FlyoutAnimationType.PULL_UP
            )
