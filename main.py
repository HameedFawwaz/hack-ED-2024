import json
import paramiko
import random
import os



def main(inputs):
    token = inputs['token']
    client_id = int(inputs['client_id'])
    invite_link = f"https://discord.com/oauth2/authorize?client_id={client_id}&scope=bot&permissions=268479550"

    
    SSH_Client = paramiko.SSHClient()
    SSH_Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    SSH_Client.connect(hostname="155.138.214.243", port=22, username="root", password= "Xz8=KdN@qbkW*Xsc", look_for_keys= False)


    sftp_client = SSH_Client.open_sftp()
    user_id = random.randint(100000, 999999)
    list_dir = os.listdir("/home")
    SSH_Client.exec_command(f"mkdir {user_id}")

    f = open("config.json", "x")
    json.dump({"Token": token, "Prefix": "="}, f)
    f.close()

    sftp_client.put("config.json", f"./{user_id}/config.json")

    for i in list_dir:
        local_filepath = f"/home/{i}"
        remote_filepath = f"./{user_id}/{i}"
        sftp_client.put(local_filepath, remote_filepath)

    sftp_client.close()
    SSH_Client.exec_command(f"cd {user_id};python3 main.py")
    SSH_Client.close()
    return{"invite_link": invite_link}
