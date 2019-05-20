NTUST Webpages Development
網頁製作
==============================
## Contributors 組員
|github|學號|姓名|
|---|---|---|
|CoyoteLeo|B10532013|林佑恩|
|weeturn|B10532001|黃哲韋|
|amura87516|B10532027|林科廷|
|willy142857|B10532030|楊博惟|


# environment
python 3.6+
```shell
# create virtual python environment 
$ python3 -m venv venv
$ .\venv\Scripts\activate
$ pip install -r requirements.txt
```

if you pip install any module, please update the requirements.txt via the command below
```shell
$ pip freeze > requirements.txt
```

# Project Setup
1. 在settings.py的同目錄下新增local_settings.py
2. 貼上下列程式碼
    ```python
    import os

    DEBUG = True

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    ```

