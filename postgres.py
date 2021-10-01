import re
import subprocess
import psycopg2
from colorama import Fore

def open_file(file_name):
    with open(file_name, 'r', encoding='UTF-8') as file:
        data = file.read()
    return data

def ping_ip(ip_list):
    for ip in ip_list:
        command = ['ping', '-c', '1', ip]
        exit_code = subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if exit_code == 0:
            print(Fore.GREEN + ip, '- OK')
            using_database(ip, 'OK')
        else:
            print(Fore.RED + ip, '- FAIL')
            using_database(ip, "FAIL")

def using_database(ip, status):
    conn = psycopg2.connect(dbname='database', user='db_user',
                            password='mypassword', host='localhost')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ip_list(id SERIAL PRIMARY KEY NOT NULL, ip TEXT NOT NULL UNIQUE, status TEXT NOT NULL) 
    """)
    cursor.execute(f"""
    INSERT INTO ip_list (ip, status) VALUES (%s, %s) ON CONFLICT (ip) DO NOTHING
    """, (ip, status))
    conn.commit()

def main():
    text = open_file('file.txt')
    ip_list = set(re.findall(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", text))
    ping_ip(ip_list)

if __name__ == '__main__':
    main()
