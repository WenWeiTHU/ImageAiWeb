# Backend final task: ImageAI Web
A Web service based on the HTTP protocol provides a Web API to add, delete, and change specified data to the database based on the basic registration, login, and logout functions.
## Author

* **Name**: Liu Yong (2017013578), Liu Wei (2017013590).


## Environment

* **System**: Windows 10 x64
* **Project Interpreter**: Python 3.7.1
* **IDE**: 2019.2.1 Professional

## Requirments: 

* django 2.2.4
* tensorflow 1.4.0+
* numpy 1.13.1+
* scipy 0.19.1+
* opencv-python
* pillow
* matplotlib
* h5py
* requests
* [imageai](https://imageai-cn.readthedocs.io/zh_CN/latest/ImageAI.html)
* keras 2.x+

```
pip install django
pip install tensorflow
pip install numpy
pip install scipy
pip install opencv-python
pip install pillow
pip install matplotlib
pip install h5py
pip install keras
```
```
pip install https://github.com/OlafenwaMoses/ImageAI/releases/download/2.0.1/imageai-2.0.1-py3-none-any.whl
```
## Usage


```
cd image_ai
```

Put downloaded models into ./media/models

Run server in **localhost(127.0.0.1)**, default **port 8000**

```
python manage.py runserver
```
Then open your Google Chrome, input the URL
```
127.0.0.1:8000/login/
```
## URL patterns

* login/
* logon/
* logout/
* index/
* about/
* record/<username>/
* admin/login/

## Contact

* [liuyong1095556447@gmail.com](mailto:liuyong1095556447@gmail.com)
* [liuwei.wendy17@gmail.com](mailto:liuwei.wendy17@gmail.com)