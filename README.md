# 异常驾驶行为识别系统

## 一、项目描述
1.本项目旨在检测驾驶员在驾驶过程中可能发生的异常驾驶行为，并实时量化、评估当前的危险程度，予以驾驶员一定程度的提醒操作。具体而言，本项目主要检测驾驶员可能出现的疲劳驾驶行为和分心驾驶行为。通过为每一异常行为分配动态权重，得到了当前安全得分。根据得分，系统会在恰当时机对驾驶员予以提醒。

2.该项目的界面采用了PyQt5和[PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)实现，

3.该系统能够检测八种行为：<睁眼, eye_open>,<闭眼, eye_close>,<嘴巴, mouth>, <打哈欠, yawn>, <脸, face>, <抽烟, smoke>,<使用手机, phone>, <喝水, drink>。其中闭眼、打哈欠、抽烟、使用手机、喝水这五种行为被视作异常驾驶行为。检测使用了[YOLOv8](https://github.com/ultralytics/ultralytics)在自制数据集上训练的模型，模型在验证集上的PR曲线：
<div style="text-align:center;">
<img src="./assets/PR_curve.png" alt="Image" width="675" height="450">
</div>

4.该项目主要实现了以下功能：

&emsp;&emsp;(1)主页：能够快速了解项目内容和主要功能。

&emsp;&emsp;(2)操作指南页面：用户能够通过点击翻页按钮来快速浏览系统功能操作说明。

&emsp;&emsp;(3)图片/视频检测页面：用户能够上传图片、图片文件夹、视频进行检测，并且能够批量导出检测结果至本地。

&emsp;&emsp;(4)实时检测页面：调用本地摄像头进行实时检测，具有预警功能，支持生成、导出检测日志和得分曲线。

&emsp;&emsp;(5)设置页面：配置日志文件夹、资源文件夹、检测结果文件夹的路径。

## 二、文件结构
```commandline
abnormal-driving-behavior
│  README.md
│  requirements.txt
│
├─assets
|     ...
|
└─adb-detector
   │  config.json              # 存放系统文件夹路径
   │  guide_demonstrator.py    # 操作指南页面
   │  home.py                  # 主页页面
   │  main.py                  # 🔺程序入口，创建系统窗口
   │  real_time_detector.py    # 实时检测页面
   │  settings.py              # 设置页面
   │  upload_detector.py       # 图片/视频检测页面
   │
   ├─logs              # 实时检测中保存日志的文件夹
   │
   ├─resource          # 资源文件夹
   │  ├─audio
   │  ├─img
   │  └─model_weight
   │
   ├─result            # 保存检测结果的文件夹
   │  ├─file
   │  ├─folder
   │  └─video
   |
   └─utils
         config.py
         load_plot.py        # 加载绘图数据
         video_surface.py    # 视频检测时抽帧
```
1.`main.py`是整个项目的运行入口，创建系统窗口。

  主要会执行以下步骤：

&emsp;&emsp;(1)创建主页，通过创建`home.py`中`Home`实例完成。

&emsp;&emsp;(2)创建操作指南页面，通过创建`guide_demonstrator.py`中`Guide_Demonstrator`实例完成。

&emsp;&emsp;(3)创建图片/视频页面，通过创建`upload_detector.py`中`Upload_Detector`实例完成。

&emsp;&emsp;(4)创建实时检测页面，通过创建`real_time_detector.py`中`RealTime_Detector`实例完成。

&emsp;&emsp;(4)创建设置页面，通过创建`settings.py`中`Settings`实例完成。

2.项目使用YOLOv8在自制数据集上训练的模型进行检测，模型位于`./adb-detector/resource/model_weight/best.pt`。

可在`config.json`或系统中的`设置页面`修改路径，替换为自己训练的模型，修改后需要重启系统。

<br/>

（可选阅读）

3.`utils/config.py`是配置系统文件夹的路径、默认值、校验方法，不要轻易修改。若要配置路径，请修改`config.json`文件，或直接在系统的`设置页面`
中点击对应按钮进行修改即可。

4.`utils/video_surface.py`是在图片/视频检测中抽取`QMediaPlayer`输出的视频帧，便于模型进行检测。

5.`utils/load_plot.py`能够读取`.pkl`文件获取`PlotWidget`绘图数据进行绘图，`.pkl`文件通过实时检测页面中保存绘图数据获得。


## 三、使用说明
Windows系统下，在cmd中cd到requirements.txt所在目录下，执行以下命令，以安装项目所需包
```commandline
pip install -r requirements.txt
```
完成后，打开项目，运行adb-detector/main.py即可

## 四、（可选阅读）实时检测中的得分机制
系统会为每一异常驾驶行为分配默认权重，同时每一异常行为还会拥有一个权重调整系数`lamda`，该系数会随异常行为持续时间的增加而增大，用来纠正驾驶员某一长时间的异常行为。

具体而言，每一异常行为都会分配一个计时器，默认状态下，计时器为停止状态。当某种异常行为发生时，该异常行为的计时器将会启动，并每3秒检测一次该异常行为是否仍在持续。若仍在持续，则权重放大系数会从0以0.2的步长逐渐增加至1后停止。

故`lamda = min(0.2 * count, 1)`，异常行为实际权重为`(1 + lamda) * weight`。

## 五、界面展示
### 主页
![image](./assets/home.png)

### 操作指南页面
![image](./assets/guide.png)

### 图片/视频检测页面
![image](./assets/upload.png)

### 上传视频，检测结果
![image](./assets/upload_eg.png)

### 实时检测页面
![image](./assets/real-time.png)

### 设置
![image](./assets/settings.png)

