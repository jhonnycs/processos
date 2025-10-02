#!/bin/bash
python3 -m venv venv

# Ativar venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Rodar o script principal
python main.py