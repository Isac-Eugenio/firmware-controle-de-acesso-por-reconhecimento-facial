import platform
import os

class Ping:
    def __init__(self, ip: str):
        self.ip = ip

    def ping(self) -> bool:
        # Define o parâmetro correto baseado no sistema operacional
        param = "-n" if platform.system().lower() == "windows" else "-c"
        
        # Redireciona a saída corretamente para cada SO
        null = "nul" if platform.system().lower() == "windows" else "/dev/null"
        
        # Monta e executa o comando de ping
        command = f"ping {param} 1 {self.ip} > {null} 2>&1"
        response = os.system(command)
        
        return response == 0