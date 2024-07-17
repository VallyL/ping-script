import subprocess
import time

def ping(host):
    """Пинг указанного адреса и возвращает время отклика в миллисекундах."""
    try:
        output = subprocess.check_output(["ping", "-c", "1", "-W", "1", host], stderr=subprocess.STDOUT)
        for line in output.decode("utf-8").splitlines():
            if "time=" in line:
                time_ms = int(line.split("time=")[-1].split(" ")[0].replace("ms", ""))
                return time_ms
        return None  
    except subprocess.CalledProcessError:
        return None  


host = input("Введите адрес для пинга: ")


failed_pings = 0

while True:
    ping_time = ping(host)
    if ping_time is not None:
        if ping_time > 100:
            print(f"Высокое время отклика: {ping_time} мс")
        else:
            print(f"Время отклика: {ping_time} мс")
        failed_pings = 0  
    else:
        print("Не удалось выполнить пинг")
        failed_pings += 1
        if failed_pings >= 3:
            print("Пинг не доступен в течение 3 последовательных попыток. Остановка скрипта.")
            break 

    time.sleep(1)
