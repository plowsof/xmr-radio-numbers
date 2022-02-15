import os
import pprint
import subprocess 
from monerorpc.authproxy import AuthServiceProxy, JSONRPCException
import datetime
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
remote_node = "http://localhost:18081/json_rpc"
def getBlockheight():
    global remote_node
    # initialisation, rpc_user and rpc_password are set as flags in the cli command
    rpc_connection = AuthServiceProxy(service_url=remote_node)

    info = rpc_connection.get_info()
    return(info["height"])

def main():
    blockHeight = getBlockheight()
    print(blockHeight)
    if os.path.isfile("numbers"):
        os.remove("numbers")
    if os.path.isfile("output.mp3"):
        os.remove("output.mp3")
    with open("numbers","w+") as f:
        f.write("file intro.mp3\n")
        for num in str(blockHeight):
            f.write(f"file {num}.mp3\n")
        f.write(f"file last.mp3")
    createSound()
    with open("evidence", "a+") as f:
        f.write(str(datetime.datetime.now()))
        f.write("\n")
    broadcast()

def createSound():
    my_frame = 3
    subprocess.call([
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', 'numbers',
        '-c', 'copy',
        'output.mp3'
    ])
def broadcast():
    subprocess.call([
        'ffmpeg',
        '-i', 'output.mp3', 
        '-f', 'mp3',
        '-method', 'PUT',
        'icecast://source:password@url'
    ])
main()
