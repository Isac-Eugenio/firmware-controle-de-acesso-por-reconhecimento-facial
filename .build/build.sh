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

# Função para rodar comando com spinner
run_spinner() {
    log "$1"
    bash -c "$1" >>"$LOGFILE" 2>>"$ERRORLOG" &
    pid=$!
    spinner $pid
    wait $pid
    status=$?
    if [ $status -ne 0 ]; then
        error "Falha ao executar: $1"
        exit 1
    fi
}

log "Iniciando instalação de dependências do sistema..."

run_spinner "sudo apt update"
run_spinner "sudo apt upgrade -y"
run_spinner "sudo apt install -y python3-venv"
run_spinner "sudo apt install -y build-essential cmake python3-dev python3-pip libopenblas-dev libboost-all-dev libx11-dev libjpeg-dev libpng-dev"

log "Criando ambiente virtual..."
run_spinner "python3 -m venv .venv"

log "Atualizando pip dentro do ambiente virtual..."
run_spinner "source .venv/bin/activate && pip install --upgrade pip"

log "⚙️ Instalando dependências Python (compilação do dlib pode demorar alguns minutos)..."
# Rodando pip install com source no subshell para garantir venv ativado
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
