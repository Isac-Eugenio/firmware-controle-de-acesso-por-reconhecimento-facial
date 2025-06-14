#!/bin/bash
set +m  # Desliga mensagens de job control tipo '[1]+ Done'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOGFILE="$SCRIPT_DIR/build.log"
ERRORLOG="$SCRIPT_DIR/build_error.log"

# Limpa logs anteriores
> "$LOGFILE"
> "$ERRORLOG"

# Cores
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
NC="\033[0m" # No Color

# Função de log
log() {
    echo -e "${YELLOW}[LOG]${NC} $1" | tee -a "$LOGFILE"
}

# Função de erro
error() {
    echo -e "${RED}[ERRO]${NC} $1" | tee -a "$ERRORLOG" >&2
}

# Função de execução com log
run() {
    log "$1"
    bash -c "$1" >>"$LOGFILE" 2>>"$ERRORLOG"
    if [ $? -ne 0 ]; then
        error "Falha ao executar: $1"
        exit 1
    fi
}

# Spinner para loading visual
spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    echo -n " "
    while kill -0 $pid 2>/dev/null; do
        local temp=${spinstr#?}
        printf "\b%c" "$spinstr"
        spinstr=$temp${spinstr%"$temp"}
        sleep $delay
    done
    printf "\b"
}

log "Iniciando instalação de dependências do sistema..."
run "sudo apt update"
run "sudo apt upgrade -y"
run "sudo apt install python3-venv"
run "sudo apt install -y build-essential cmake python3-dev python3-pip libopenblas-dev libboost-all-dev libx11-dev libjpeg-dev libpng-dev"

log "Criando ambiente virtual..."
run "python3 -m venv .venv"
run "source .venv/bin/activate && pip install --upgrade pip"

log "⚙️ Instalando dependências Python (compilação do dlib pode demorar alguns minutos)..."

# Instalação com spinner e saída oculta na tela, mas salva logs
bash -c "source .venv/bin/activate && pip install -r requirements.txt" >>"$LOGFILE" 2>>"$ERRORLOG" &
pid=$!
spinner $pid
wait $pid
status=$?
if [ $status -ne 0 ]; then
    error "Falha ao instalar requirements.txt (provavelmente na compilação do dlib)"
    exit 1
fi

log "Build concluído com sucesso!"
echo -e "${GREEN}[✓] Ambiente configurado com sucesso!${NC}"
