#!/bin/bash

pwd

#  создание файла для логов, если его не существует
touch  /app/logs/crontab.log

# обеспечение прав на выполнение файла
chmod a+x /app/collect.py

# добавление правила периодического задания для cron
# * * * * * – выполнение задания один раз в каждую минуту
echo "0 * * * *  /usr/local/bin/python /app/collect.py >> /app/logs/crontab.log 2>&1" > /etc/crontab

# сохранение текущих значений переменных окружения в файле для cron
printenv >> /etc/environment

# регистрация созданного правила
crontab /etc/crontab

# запуск cron
/usr/sbin/service cron start

pwd

ls

# вывод логов
tail -f /app/logs/crontab.log

