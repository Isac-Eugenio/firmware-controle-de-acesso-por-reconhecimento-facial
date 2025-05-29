import platform
import subprocess

class PingService:
    def __init__(self, ip: str):
        self.ip = ip

    def ping(self) -> bool:
        # Define o parâmetro correto baseado no sistema operacional
        param = "-n" if platform.system().lower() == "windows" else "-c"
        
        # Monta o comando de ping de forma segura com subprocess
        command = ["ping", param, "1", self.ip]
        
        try:
            # Executa o comando e aguarda a conclusão
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Verifica o código de retorno para determinar se o ping foi bem-sucedido
            return result.returncode == 0
        
        except Exception as e:
            print(f"Erro ao tentar realizar o ping: {e}")
            return False
