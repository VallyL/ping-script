#!/bin/bash

ping_host() {
    output=$(ping -c 1 -W 1 "$1" 2>&1)
    if [[ $? -eq 0 ]]; then
        echo "$output" | grep "time=" | awk -F'time=' '{print $2}' | awk '{print $1}' | sed 's/ms//'
    else
        echo "failed"
    fi
}

read -p "Введите адрес для пинга: " host

failed_pings=0

while true; do
    ping_time=$(ping_host "$host")
    if [[ "$ping_time" != "failed" ]]; then
        if (( $(echo "$ping_time > 100" | bc -l) )); then
            echo "Высокое время отклика: ${ping_time} мс"
        else
            echo "Время отклика: ${ping_time} мс"
        fi
        failed_pings=0
    else
        echo "Не удалось выполнить пинг"
        failed_pings=$((failed_pings + 1))
        if (( failed_pings >= 3 )); then
            echo "Пинг не доступен в течение 3 последовательных попыток. Остановка скрипта."
            break
        fi
    fi
    sleep 1
done
