# 人脸识别

## 效果预览

<div align="center">
  <img src="https://github.com/liziniu/face_cognition/blob/master/face_recognition.gif">
</div>

## 硬件要求
下面是我购买的硬件，总计约500元。部分给出了淘宝连接。

1.树莓派开套套件([淘宝399元](https://detail.tmall.com/item.htm?id=551247172510&spm=a1z09.2.0.0.1a942e8dHwbjZj&_u=cmrfg466926))
 
- 树莓派3B
- 电源线
- 网线或[无线网卡](https://item.taobao.com/item.htm?spm=a1z09.2.0.0.1b482e8dJNVmUs&id=15467431750&_u=cmrfg4662ac)(注意上面399元链接不包含无线网卡）
- HDMI线
- SD卡
- 读卡器

2.键盘([淘宝45元](https://detail.tmall.com/item.htm?id=43062116591&spm=a1z09.2.0.0.1b482e8dJNVmUs&_u=cmrfg466bda&sku_properties=5919063:6536025))。最好不要蓝牙键盘。

3.鼠标([淘宝29元](https://detail.tmall.com/item.htm?id=45366723358&spm=a1z09.2.0.0.1b482e8dJNVmUs&_u=cmrfg46f8c7&sku_properties=5919063:6536025))。最好不要蓝牙鼠标。

4.独立显示器。最好HDMI接口，因为这是树莓派的接口，没有的话需要购买VGA转HDMI转接口。

5.USB摄像头(600万像素，30元）。


## 如何使用

1.为树莓派烧录操作系统，我使用的是Ubuntu-mate。

2.安装或更新如下软件或包依赖。

- Python 2.7或3.x(我使用的是2.7, 因为安装opencv方便)

- Python依赖库：numpy, PIL, scipy, opencv, face_recognition

- opencv可以直接使用apt-get安装python-opencv，因为我们只需要opencv读取视频，不需要opencv处理

- face_recognition依赖dlib, 需要提前编译dlib

3.连接摄像头。如果使用了USB分裂器，请确保电影供电充足。

4.在程序的当前目录下创建picture文件夹，将你要识别的人的图片加入，同时修改程序中含路径的部分.不加入图片也没关系，可以通过窗口程序加入，但确保picture文件夹存在。

5.运行main.py程序。

## 额外说明

如果你在安装运行的过程中遇到了一些问题，可以发邮件给我，或许我还记得那些bug怎么修复- -.

Good Luck!
