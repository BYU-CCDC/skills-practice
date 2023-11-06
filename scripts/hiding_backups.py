import os
import shutil
import random
import string
import subprocess
import time
import datetime


def find_os():
    if os.path.exists("/etc/redhat-release"):
        return "redhat"
    elif os.path.exists("/etc/debian_version"):
        return "debian"
    elif os.path.exists("/etc/alpine-release"):
        return "alpine"
    elif os.path.exists("C:\\Windows\\System32\\winver.exe"):
        return "windows"
    else:
        return "unknown"


def find_webserver():
    if os.path.exists("/etc/nginx"):
        return "nginx"
    elif os.path.exists("/etc/apache2"):
        return "apache"
    elif os.path.exists("C:\\Windows\\System32\\inetsrv"):
        return "iis"
    else:
        return "unknown"


def make_backup_of_apache():
    possible_backup_directory_names = [
        "back",
        "backup",
        "backups",
        "old",
        "backup_old",
        "old_backup",
        "backup_1",
        "old_1",
        "backup_old_1",
        "old_backup_1",
    ]
    apache_directories = ["/var/www", "/etc/apache2"]
    backup_directory = random.choice(possible_backup_directory_names)
    backup_path = os.path.join("/", backup_directory)
    try:
        os.makedirs(backup_path)
    except:
        pass
    for directory in apache_directories:
        if os.path.exists(directory):
            new_path = os.path.join(backup_path, directory[1:])
            if os.path.exists(new_path):
                shutil.rmtree(new_path)
            shutil.copytree(directory, new_path, dirs_exist_ok=True, symlinks=True)
    return backup_path


def compress_backup(backup_path):
    possible_compression_formats = ["tar"]
    compression_format = random.choice(possible_compression_formats)
    shutil.make_archive(
        backup_path, compression_format, root_dir="/", base_dir=backup_path
    )
    shutil.rmtree(backup_path)
    return backup_path + "." + compression_format


def encrypt_backup(compressed_backup_path):
    possible_password_choices = ["password", "123456", "random", "password1"]
    password = random.choice(possible_password_choices)
    possible_extensions = [".enc", ".crypt", ".locked", ".encrypted"]
    extension = random.choice(possible_extensions)
    subprocess.Popen(
        [
            "openssl",
            "enc",
            "-aes-256-cbc",
            "-salt",
            "-in",
            compressed_backup_path,
            "-out",
            compressed_backup_path + extension,
            "-k",
            password,
        ]
    )
    return compressed_backup_path + extension


def hide_backup(os_name, compressed_encrypted_backup_path, number_of_backups=1):
    possible_backup_locations_debian = [
        "/var",
        "/var/backups",
        "/var/lib/backups",
        "/var/local/backups",
        "/var/opt/backups",
        "/var/local",
        "/",
        "/etc/apache2",
        "/archive",
        "/var/archive"
    ]
    for i in range(number_of_backups):
        copy_file_name = compressed_encrypted_backup_path + "." + str(i)
        for j in range(10):
            if os.path.exists(compressed_encrypted_backup_path):
                break
            else:
                time.sleep(1)
        shutil.copy2(compressed_encrypted_backup_path, copy_file_name)
        if os_name == "alpine":
            hidden_backup_location = random.choice(possible_backup_locations_debian)
            possible_backup_locations_debian.remove(hidden_backup_location)
            if i == 0:
                hidden_backup_name = "".join(
                    random.choices(string.ascii_uppercase + string.digits, k=10)
                )
            else:
                hidden_backup_name = copy_file_name[1:]
            
            hidden_backup_path = os.path.join(
                hidden_backup_location, hidden_backup_name
            )
            try:
                os.makedirs(hidden_backup_location)
            except:
                pass
            if i == 1:
                random_month = random.randint(1, 12)
                random_day = random.randint(1, 28)
                random_hour = random.randint(0, 23)
                random_minute = random.randint(0, 59)
                creation_datetime = datetime.datetime(2022, random_month, random_day, random_hour, random_minute) 
                modification_datetime = datetime.datetime(2022, random_month, random_day, random_hour, random_minute)
                creation_timestamp = creation_datetime.timestamp()
                modification_timestamp = modification_datetime.timestamp()
                os.utime(hidden_backup_path, (creation_timestamp, modification_timestamp))
            elif i == number_of_backups - 1:
                shutil.move("/root/.ash_history", "/root/.ash_history.tmp")
                file1 = open("/root/.ash_history.tmp", "w")
                L = ["mv "+copy_file_name+" "+hidden_backup_path+"\n"]
                file1.writelines(L)
                file1.close()
                #shutil.move("/root/.ash_history.tmp", "/root/.ash_history")
            shutil.move(copy_file_name, hidden_backup_path)
            log_backup_location(hidden_backup_path)
    os.remove(compressed_encrypted_backup_path)


def log_backup_location(backup_path):
    with open("/root/backup_locations.txt", "a") as f:
        f.write(backup_path + "\n")


def backup():
    os_name = find_os()
    webserver = find_webserver()
    if os_name == "alpine" and webserver == "apache":
        backup_path = make_backup_of_apache()
        compressed_backup_path = compress_backup(backup_path)
        compressed_encrypted_backup_path = encrypt_backup(compressed_backup_path)
        hide_backup(os_name, compressed_encrypted_backup_path, 3)
        os.remove(compressed_backup_path)
    else:
        return "OS/webserver combination not supported."


backup()
