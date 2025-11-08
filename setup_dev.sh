
#!/data/data/com.termux/files/usr/bin/bash
# ==========================================
# 🚀 Setup completo do ambiente Dev no Android (Termux)
# Autor: Glauco (Traidbolt)
# ==========================================

echo "🔍 Atualizando pacotes..."
pkg update -y && pkg upgrade -y

echo "📦 Instalando pacotes essenciais..."
pkg install git python nodejs npm wget curl openssh clang make build-essential -y

echo "🐍 Instalando dependências Python..."
pip install --upgrade pip
pip install flask jupyter pandas numpy requests python-dotenv rich

echo "📦 Instalando dependências Node.js..."
npm install -g yarn nodemon live-server code-server

echo "🎨 Instalando Tailwind CSS..."
npm install -D tailwindcss

echo "🔧 Configurando Git..."
git config --global user.name "Glauco"
git config --global user.email "glaferu604@gmail.com"

echo "🧰 Instalando utilitários extras..."
pkg install tmux htop nano vim tree -y

echo "⚙️ Criando pasta de trabalho..."
mkdir -p ~/projetos
cd ~/projetos

echo "🧠 Criando script de inicialização do VSCode Web..."
cat << 'EOF' > start_vscode.sh
#!/data/data/com.termux/files/usr/bin/bash
echo "🚀 Iniciando Visual Studio Code Web (code-server)..."
code-server --host 0.0.0.0 --port 8080
EOF
chmod +x start_vscode.sh

echo "✅ Instalação concluída!"
echo "Para iniciar o VSCode Web, execute:"
echo "-------------------------------------"
echo "cd ~/projetos && ./start_vscode.sh"
echo "-------------------------------------"
echo "🌐 Depois abra no navegador: http://127.0.0.1:8080"
