#!/usr/bin/env bash
# SentinelCloud - iniciador para Linux/macOS. Funciona SEM internet.
# Requer apenas Python 3.10+. Rode no terminal: ./iniciar.sh
# (se nao executar: chmod +x iniciar.sh  ou  bash iniciar.sh)

cd "$(dirname "$0")" || exit 1

PY=""
for cand in python3 python; do
    if command -v "$cand" >/dev/null 2>&1 && \
       "$cand" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
        PY="$cand"; break
    fi
done

if [ -z "$PY" ]; then
    echo "Python 3.10 ou superior nao foi encontrado."
    echo "Instale com o gerenciador de pacotes (ex.: sudo apt install python3)."
    read -r -p "Pressione Enter para fechar..." _
    exit 1
fi

if [ ! -d vendor/boto3 ]; then
    echo "A pasta 'vendor' nao foi encontrada. Extraia o projeto inteiro."
    read -r -p "Pressione Enter para fechar..." _
    exit 1
fi

"$PY" run.py "$@"
if [ -t 0 ]; then echo; read -r -p "Pressione Enter para fechar..." _; fi
