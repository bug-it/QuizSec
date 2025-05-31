import csv
import random
import os
import sys
import signal

# Cores ANSI
VERDE = '\033[1;32m'
VERMELHO = '\033[1;31m'
AZUL = '\033[1;34m'
AZUL_CLARO = "\033[96m"
AMARELO = '\033[1;33m'
BRANCO = '\033[1;37m'
ROXO = '\033[1;35m'
RESET = '\033[0m'

banner = f"""{VERMELHO}
         ██████╗ ██╗   ██╗██╗███████╗███████╗███████╗ ██████╗
        ██╔═══██╗██║   ██║██║╚══███╔╝██╔════╝██╔════╝██╔════╝
        ██║   ██║██║   ██║██║  ███╔╝ ███████╗█████╗  ██║
        ██║▄▄ ██║██║   ██║██║ ███╔╝  ╚════██║██╔══╝  ██║
        ╚██████╔╝╚██████╔╝██║███████╗███████║███████╗╚██████╗
         ╚══▀▀═╝  ╚═════╝ ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝
{RESET}"""

def limpar():
    os.system("cls" if os.name == "nt" else "clear")

def carregar_perguntas(nome_arquivo):
    perguntas = []
    try:
        with open(nome_arquivo, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for linha in reader:
                if all(k in linha for k in ['pergunta', 'a', 'b', 'c', 'd', 'correta']):
                    pergunta = linha['pergunta']
                    opcoes = {
                        'A': linha['a'],
                        'B': linha['b'],
                        'C': linha['c'],
                        'D': linha['d']
                    }
                    correta = linha['correta'].strip().upper()
                    if correta in opcoes:
                        perguntas.append((pergunta, opcoes, correta))
        return perguntas
    except FileNotFoundError:
        print(f"{VERMELHO}❌ Arquivo '{nome_arquivo}' não encontrado.{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{VERMELHO}Erro ao ler o arquivo CSV: {e}{RESET}")
        sys.exit(1)

def temporizador(segundos):
    def tempo_esgotado(signum, frame):
        raise TimeoutError
    signal.signal(signal.SIGALRM, tempo_esgotado)
    signal.alarm(segundos)

def mostrar_resultado(nome, acertos, erros, limite, total_csv):
    print(f"\n{BRANCO}+{'=' * 71}+{RESET}")
    print(f"\n{BRANCO}📊 {AZUL}RESULTADO")
    print(f"\n{RESET}( {VERDE}Acertou {acertos} {RESET}/ {VERMELHO}Errou {erros} {RESET}/ {AMARELO}Limite {limite} {RESET}/ {BRANCO}Total {total_csv} {RESET})\n")

    percentual = (acertos / limite) * 100
    if percentual >= 80:
        print(f"{BRANCO}🎉 {VERDE}Excelente, {ROXO}{nome}{VERDE}! Você mandou muito bem!{RESET}")
    elif 50 <= percentual < 80:
        print(f"{BRANCO}👍 {AZUL}Bom trabalho, {ROXO}{nome}{AZUL}! Mas ainda pode melhorar!{RESET}")
    else:
        print(f"{BRANCO}💪 {VERMELHO}Não desanime, {ROXO}{nome}{VERMELHO}! Continue praticando!{RESET}")

    print(f"\n{RESET}Script desenvolvido por: {VERDE}BUG IT{RESET}\n")
    print(f"{BRANCO}+{'=' * 71}+{RESET}\n")

def quiz(perguntas):
    total_csv = len(perguntas)
    limite = min(20, total_csv)
    perguntas = random.sample(perguntas, limite)

    limpar()
    print(f"{BRANCO}+{'=' * 71}+{RESET}")
    print(banner)
    print(f"{BRANCO}+{'=' * 71}+{RESET}\n")

    print(f"{AZUL_CLARO}🌐 {AZUL}Quiz Interativo - {AZUL_CLARO}ISO/IEC 27001{RESET}\n")

    try:
        nome = input(f"{BRANCO}👤 Qual seu nome? {ROXO}").strip()
    except KeyboardInterrupt:
        print(f"\n{VERMELHO}⛔️ Execução interrompida.{RESET}")
        sys.exit(0)

    print(f"\n{VERDE}Olá, {ROXO}{nome}{VERDE}! Vamos começar o desafio!{RESET}")
    try:
        input(f"\n{AZUL}Pressione ENTER para iniciar...{RESET}")
    except KeyboardInterrupt:
        print(f"\n{VERMELHO}⛔️ Execução interrompida.{RESET}")
        sys.exit(0)

    acertos = 0
    erros = 0

    for i, (pergunta, opcoes, correta) in enumerate(perguntas, 1):
        limpar()
        print(f"{BRANCO}+{'=' * 71}+{RESET}")
        print(banner)
        print(f"{BRANCO}+{'=' * 71}+{RESET}\n")
        print(f"{AZUL_CLARO}🌐 {AZUL}Quiz Interativo - {AZUL_CLARO}ISO/IEC 27001{RESET}\n")

        print(f"{BRANCO}💬 PERGUNTA ( {AMARELO}{i}{BRANCO} / {AMARELO}{limite}{BRANCO} ) - ⌛️ Tempo {AMARELO}20s{RESET}\n")
        print(f"{ROXO}📋 {pergunta}{RESET}\n")
        for letra in ['A', 'B', 'C', 'D']:
            print(f"{AMARELO}  {letra}){BRANCO} {opcoes[letra]}{RESET}\n")

        try:
            temporizador(20)
            resposta = input(f"{ROXO}📜 Resposta: {AMARELO}").strip().upper()
            signal.alarm(0)
        except TimeoutError:
            print(f"\n\n{VERMELHO}⏰ Tempo esgotado!{RESET}")
            resposta = ''
        except KeyboardInterrupt:
            print(f"\n\n{VERMELHO}⛔️ Quiz interrompido pelo usuário.{RESET}\n")
            mostrar_resultado(nome, acertos, erros, limite, total_csv)
            sys.exit(0)

        if resposta == correta:
            print(f"\n{VERDE}✔️ Correto!{RESET}")
            acertos += 1
        else:
            print(f"\n{VERMELHO}❌ Errado. {BRANCO}Resposta Correta:{VERDE} {correta}) {opcoes[correta]}{RESET}")
            erros += 1

        if i != limite:
            try:
                input(f"\n{AZUL}Pressione ENTER para continuar...{RESET}")
            except KeyboardInterrupt:
                print(f"\n\n{VERMELHO}⛔️ Quiz interrompido pelo usuário.{RESET}")
                mostrar_resultado(nome, acertos, erros, limite, total_csv)
                sys.exit(0)

    mostrar_resultado(nome, acertos, erros, limite, total_csv)

# Execução principal
if __name__ == "__main__":
    nome_arquivo = "perguntas.csv"
    perguntas = carregar_perguntas(nome_arquivo)
    if perguntas:
        quiz(perguntas)
    else:
        print(f"{VERMELHO}⚠️ Nenhuma pergunta válida foi carregada.{RESET}")
