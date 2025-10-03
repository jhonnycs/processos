#!/bin/bash

VENV_DIR="venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Criando virtual environment..."
    python3 -m venv $VENV_DIR
else
    echo "Virtual environment já existe."
fi

source "$VENV_DIR/bin/activate"

echo "Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt


echo "Setup concluído! Ative o venv com: source $VENV_DIR/bin/activate"