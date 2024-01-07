import json
import paramiko
import random
import os
import time


#token = input("Enter your token here!")
token = "MTE0Nzk3NTg3NTk2MzM5MjEyMA.GH2ec-.jsiYiuP5qk1cEYctl4tm7jiNghq2LUeKEIII20"

f = open("config.json", "x")
json.dump({"Token": token, "Prefix": "="}, f)


SSH_Client = paramiko.SSHClient()
SSH_Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
SSH_Client.connect( hostname="155.138.214.243", port=22, username="root",
                   password= "Xz8=KdN@qbkW*Xsc", look_for_keys= False
                 )


sftp_client = SSH_Client.open_sftp()
user_id = random.randint(100000, 999999)
list_dir = os.listdir("./home")
SSH_Client.exec_command(f"mkdir {user_id}")
sftp_client.put("config.json", f"./{user_id}/config.json")

for i in list_dir:
  local_filepath = f"./home/{i}"
  remote_filepath = f"./{user_id}/{i}"
  sftp_client.put(local_filepath, remote_filepath)

sftp_client.close()
SSH_Client.exec_command(f"cd {user_id};python3 main.py")
SSH_Client.close()