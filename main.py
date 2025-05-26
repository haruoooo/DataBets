import subprocess

def rodar_server():
    subprocess.run(["python", "backend/server.py"])

if __name__ == "__main__":
    rodar_server()
