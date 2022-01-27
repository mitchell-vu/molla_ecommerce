Nhớ tải python
Chạy pip install virtualenv
virtualenv env
active env 

install các package Django, Pillow, mysqlclient
Script chạy: python (python3) manage.py runserver
Tạo admin: python3 manage.py createsuperuser


config database ở trong phần molla_theme/setting.py

❯ python manage.py dumpdata orders store category carts accounts > data_dump.json