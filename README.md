<h1 align="center">Backend портала стажировок</h1>


  ![](https://github.com/katecapri/images-for-readme/blob/main/drf.png.png)  ![](https://github.com/katecapri/images-for-readme/blob/main/RabbitMQ.png)  ![](https://github.com/katecapri/images-for-readme/blob/main/docker.png)


##  Описание ##

В базу заносится информация о направлениях стажировок, местах проведения стажировок, уровнях доступа к информации, шаблонах проведения программ стажировок. На основании шаблонов создаются программы стажировки на определенные даты и списки требований к кандидатам. Создаются пользователи, которых можно занести в кандидаты на стажировку и которые могут, пройдя отбор, зачислиться на программу стажировки. По результатам прохождения обозначенной программы зачисленными на стажировку выгружаются табели о проделанной работе. 
![](https://github.com/katecapri/images-for-readme/blob/main/общая%20схема.png) 


##  Используемые технологии ##

- Python
- RabbitMQ.png
- SQLAlchemy
- Alembic
- Docker
- Pylint
- Openpyxl


##  Инструкция по запуску ##

1. В файле email-api/Makefile требуеся заменить переменные INTERNSHIPS_SMTP_HOST, INTERNSHIPS_SMTP_PORT, INTERNSHIPS_SMTP_USERNAME, INTERNSHIPS_SMTP_PASSWORD. В файле api/Makefile - INTERNSHIPS_SMTP_USERNAME, INTERNSHIPS_API_ACCOUNT_INIT_EMAIL.

2. Запуск всего проекта производится командой:

> make run


##  Результат ##

1. Новый пользоваель создается методом POST http://0.0.0.0:8008/api/v1/auth/signup/
   
![](https://github.com/katecapri/images-for-readme/blob/main/1signup.png)

2. Получаеv код csrf http://0.0.0.0:8008/api/v1/auth/csrf/

3. Берем присланный код подтверждения email-адреса с почты.

4. Подтверждаем почтовый адрес методом POST http://0.0.0.0:8008/api/v1/auth/email/confirm/
   
![](https://github.com/katecapri/images-for-readme/blob/main/4%20подтв%20емаил.png)

5. Логин - метод POST http://0.0.0.0:8008/api/v1/auth/login/
   
![](https://github.com/katecapri/images-for-readme/blob/main/5%20логин.png)

6. Для того, чтобы были доступны все методы - для новосозданного пользователя в таблицу users устанавливается значение поля app_role_id, равное id администратора из таблицы app_roles

7. Для перехода из кандидата в стажеры и из стажера в выпускники существуют определенные шаги, описанные в таблицах template*. Новый период проведения стажировки создается методом POST http://0.0.0.0:8008/api/v1/template/<uuid>/launch/ , где <uuid> - id из таблицы templates. Этим методом создаются соответствующие записи в таблицах route* по выбранному шаблону проведения испытаний.
   
![](https://github.com/katecapri/images-for-readme/blob/main/7.1.%20маршрут%20набор%20на%20стаж.png)
![](https://github.com/katecapri/images-for-readme/blob/main/7.2%20испытания%20на%20стажировке.png)

8. Когда новый набор на стажировку открыт, кандидаты могут начать подавать на него заявки. Заявка автоматически проходит проверку присланных данных с обозначенными параметрами кандидатов, ограниченными для данной стажировки (в соответствии с правилами из route_request_field_templates). 
   
![](https://github.com/katecapri/images-for-readme/blob/main/8%20создание%20заявки.png)
![](https://github.com/katecapri/images-for-readme/blob/main/8.2%20подтверждение%20заявки.png)

9. Если кандидат подходит по параметрам - он получает подтвержденный статус кандидата и ему начинают начисляться баллы, необходимые для окончания стажировки. Получение текущего значения баллов доступно методом GET http://0.0.0.0:8009/api/v1/points/?userId=<uuid> , где <uuid> - id кандидата. 
   
![](https://github.com/katecapri/images-for-readme/blob/main/9.%20баллы%20пользователя.png)

10. Назначение стажера на стажировку производится обновлением информации о пользователе - POST на http://0.0.0.0:8008/api/v1/user/<uuid>/, где <uuid> - id пользователя. 
   
![](https://github.com/katecapri/images-for-readme/blob/main/10.%20стажер%20на%20стажировку.png)

11. Новому стажеру автоматически генерируется расписание посещений (база timesheet). 
   
![](https://github.com/katecapri/images-for-readme/blob/main/11.%20расписание%20для%20стажера.png)

12. Если какой-то день отклоеняется от расписания (стажер заболел), оно меняется методом POST http://0.0.0.0:8008/api/v1/route/<uuid1>/timesheet/?userId=<uuid2> , где <uuid1> - id стажировки (route) , <uuid1> - id пользователя.
Либо напрямую в контейнере с расписанием стажеров POST http://0.0.0.0:8010/api/v1/timesheet/ .
   
![](https://github.com/katecapri/images-for-readme/blob/main/12.%20изменение%20расписания.png.jpg)
![](https://github.com/katecapri/images-for-readme/blob/main/12.1%20изменение%202.png)

13. Excel-файл с табелем по всем стажерам выгружается через GET http://0.0.0.0:8008/api/v1/route/<uuid>/timesheet/download/, где <uuid1> - id стажировки (route) .
   
![](https://github.com/katecapri/images-for-readme/blob/main/13.%20табель.png)
