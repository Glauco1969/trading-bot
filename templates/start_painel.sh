#!/data/data/com.termux/files/usr/bin/bash
# ===========================================
# 🚀 Script de inicialização do painel Flask
# Autor: Glauco (Traidbolt)
# ===========================================

echo "🔍 Verificando ambiente Python..."

# Cria venv se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python -m venv venv
fi

# Ativa o ambiente virtual
source venv/bin/activate

# Instala dependências se necessário
if [ -f "requirements.txt" ]; then
    echo "📦 Instalando dependências..."
    pip install -r requirements.txt
else
    echo "⚠️  Nenhum requirements.txt encontrado, instalando Flask básico..."
    pip install flask
fi

# Obtém IP local
IP=$(ip addr show wlan0 | grep 'inet ' | awk '{print $2}' | cut -d'/' -f1)

# Inicia o Flask
echo "✅ Ambiente pronto!"
echo "🌐 Acesse em: http://$IP:5000"
echo "🚀 Iniciando painel Flask..."
sleep 2

# Detecta automaticamente o arquivo principal
if [ -f "app.py" ]; then
    python app.py
elif [ -f "main.py" ]; then
    python main.py
else
    echo "❌ Nenhum arquivo Flask encontrado (app.py ou main.py)."
fi
