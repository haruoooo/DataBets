import subprocess

def rodar_processos():
    subprocess.Popen(["python", "backend/server.py"])

if __name__ == "__main__":
    rodar_processos()
