import sys
import os
os.system(f"\"{sys.executable}\" -m pip install windows-curses")
import curses
import json
import random
import threading
import pygame


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from interface.ui import (UI, COR_DANO, COR_CURA, COR_TEXTO, COR_ITEM,
                           COR_EXP, COR_INIMIGO, COR_DESTAQUE, COR_VIDA)
CAMINHO_BASE  = os.path.dirname(os.path.abspath(__file__))
CAMINHO_SAVE  = os.path.join(CAMINHO_BASE, "save.json")
CAMINHO_MUSICA = os.path.join(CAMINHO_BASE, "musica", "tema.ogg")
# Música
def iniciar_musica():
    print("\n[Som] Tentando iniciar a música...")
    try:
        # 1. Garante que o SDL converse com o servidor de som correto do Arch (PipeWire/PulseAudio)
        os.environ['SDL_AUDIODRIVER'] = 'pulse'
        
        # 2. Configura a amostragem antes de iniciar para evitar conflito com o terminal
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        
        # 3. Carrega e toca
        pygame.mixer.music.load(CAMINHO_MUSICA)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)
        print("[Som] Sucesso! Música enviada para o servidor de áudio.")
    except Exception as erro:
        # Se falhar, isso aqui vai te dizer EXATAMENTE o motivo no terminal
        print(f"\n[ERRO DE ÁUDIO CRÍTICO]: {erro}\n")
def parar_musica():
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()
    except Exception:
        pass
# Dados
def carregar_dados():
    caminho_json = os.path.join(CAMINHO_BASE, "dados.json")
    with open(caminho_json, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)
def salvar_jogo(estado):
    with open(CAMINHO_SAVE, "w", encoding="utf-8") as arquivo:
        json.dump(estado, arquivo, indent=4, ensure_ascii=False)
def carregar_jogo():
    if not os.path.exists(CAMINHO_SAVE):
        return None
    try:
        with open(CAMINHO_SAVE, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except Exception:
        return None
# Estado inicial
def novo_jogo(dados):
    dados_lvl1 = dados["dados de interação"]["jogador"][0]
    pocao_inicial = next(
        (p for p in dados["dados de interação"]["poção"] if p["nome"] == "Poção de Cura Média"),
        None
    )
    return {
        "jogador": {
            "lvl":         1,
            "vida max":    dados_lvl1["vida"],
            "vida atual":  dados_lvl1["vida"],
            "força":       dados_lvl1["força"],
            "defesa base": dados_lvl1["defesa"],
            "exp":         0,
            "arma":        dados["dados de interação"]["armas"][0],
            "armadura":    dados["dados de interação"]["armaduras"][0],
            "inventario":  [pocao_inicial] if pocao_inicial else [],
        },
        "sala atual":       1,
        "sala totais":      20,
        "tesouro coletado": [],
    }
# Masmorra
def gerar_sala(estado, dados):
    sala_atual    = estado["sala atual"]
    salas_totais  = estado["sala totais"]

    if sala_atual == salas_totais:
        dragao = dados["dados de interação"]["monstros"][-1]
        return {"tipo": "combate", "conteudo": dict(dragao)}
    progresso = sala_atual / salas_totais
    if   progresso <= 0.15: nivel_monstro = 0
    elif progresso <= 0.35: nivel_monstro = 1
    elif progresso <= 0.50: nivel_monstro = 2
    elif progresso <= 0.60: nivel_monstro = 3
    else:                   nivel_monstro = 4
    disponiveis = [m for m in dados["dados de interação"]["monstros"]
                   if m["lvl"] == nivel_monstro and m["lvl"] < 5]
    if not disponiveis:
        disponiveis = [dados["dados de interação"]["monstros"][0]]
    return {"tipo": "combate", "conteudo": dict(random.choice(disponiveis))}
# Combate
def rodar_combate(ui, estado, dados_monstro, dados):
    jogador = estado["jogador"]
    monstro = dict(dados_monstro)
    monstro["vida_max"] = monstro["vida"]
    registro = []
    def adicionar_registro(mensagem, cor=COR_TEXTO):
        registro.append((mensagem, cor))
    adicionar_registro(f"Um(a) {monstro['nome']} emerge das sombras!", COR_INIMIGO)
    while jogador["vida atual"] > 0 and monstro["vida"] > 0:
        ui.tela_combate(jogador, monstro, registro)
        curses.echo()
        curses.curs_set(1)
        try:
            acao = ui.tela.getstr(ui.altura - 2, 13, 3).decode("utf-8").strip()
        except Exception:
            acao = ""
        curses.noecho()
        curses.curs_set(0)
        if acao == "1":
            dano_jogador = jogador["força"] + jogador["arma"]["ataque"]
            monstro["vida"] -= dano_jogador
            adicionar_registro(f"Você causou {dano_jogador} de dano em {monstro['nome']}!", COR_DANO)
            if monstro["vida"] <= 0:
                adicionar_registro(f"{monstro['nome']} foi derrotado!", COR_DESTAQUE)
                ui.tela_combate(jogador, monstro, registro)
                processar_vitoria(ui, jogador, monstro["exp"], dados)
                return True
            defesa_total = jogador["defesa base"] + jogador["armadura"]["defesa"]
            dano_monstro = max(1, monstro["ataque"] - defesa_total)
            jogador["vida atual"] -= dano_monstro
            adicionar_registro(f"{monstro['nome']} te causou {dano_monstro} de dano!", COR_VIDA)
        elif acao == "2":
            pocoes_disponiveis = [i for i in jogador["inventario"] if "cura" in i]
            if not pocoes_disponiveis:
                adicionar_registro("Você não tem poções!", COR_INIMIGO)
                continue
            resultado = tela_escolher_pocao(ui, pocoes_disponiveis)
            if resultado:
                pocao_escolhida, _ = resultado
                jogador["vida atual"] = min(jogador["vida max"],
                                            jogador["vida atual"] + pocao_escolhida["cura"])
                jogador["inventario"].remove(pocao_escolhida)
                adicionar_registro(
                    f"Você usou {pocao_escolhida['nome']} e recuperou {pocao_escolhida['cura']} HP!",
                    COR_CURA)
                defesa_total = jogador["defesa base"] + jogador["armadura"]["defesa"]
                dano_monstro = max(1, monstro["ataque"] - defesa_total)
                jogador["vida atual"] -= dano_monstro
                adicionar_registro(f"{monstro['nome']} te causou {dano_monstro} de dano!", COR_VIDA)
        else:
            adicionar_registro("Ação inválida!", COR_INIMIGO)
    return jogador["vida atual"] > 0
def tela_escolher_pocao(ui, pocoes):
    altura_tela  = ui.altura
    largura_tela = ui.largura
    larg_caixa   = 40
    col_caixa    = (largura_tela - larg_caixa) // 2
    linha_caixa  = altura_tela // 2 - len(pocoes) // 2 - 3

    ui.caixa(linha_caixa, col_caixa, len(pocoes) + 5, larg_caixa)
    ui.titulo_decorado(linha_caixa + 1, "POÇÕES", largura=largura_tela)

    for i, pocao in enumerate(pocoes):
        ui.escrever(linha_caixa + 3 + i, col_caixa + 3,
                    f"[{i+1}] {pocao['nome']} (+{pocao['cura']} HP)", COR_CURA)
    ui.escrever(linha_caixa + len(pocoes) + 3, col_caixa + 3, "[0] Cancelar", COR_ITEM)
    ui.escrever(altura_tela - 2, 3, "Escolha: ", COR_EXP, negrito=True)
    ui.atualizar()
    curses.echo()
    curses.curs_set(1)
    try:
        escolha = ui.tela.getstr(altura_tela - 2, 12, 3).decode("utf-8").strip()
    except Exception:
        escolha = "0"
    curses.noecho()
    curses.curs_set(0)
    if escolha == "0":
        return None
    if escolha.isdigit() and 0 < int(escolha) <= len(pocoes):
        indice = int(escolha) - 1
        return pocoes[indice], indice
    return None
def processar_vitoria(ui, jogador, exp_ganho, dados):
    jogador["exp"] += exp_ganho
    mensagens = [f"Você ganhou {exp_ganho} EXP!"]
    proximo_nivel = jogador["lvl"] + 1
    for dados_nivel in dados["dados de interação"]["jogador"]:
        if dados_nivel["lvl"] == proximo_nivel:
            if jogador["exp"] >= dados_nivel["exp necessario"]:
                jogador["lvl"]        = proximo_nivel
                jogador["vida max"]   = dados_nivel["vida"]
                jogador["vida atual"] = dados_nivel["vida"]
                jogador["força"]      = dados_nivel["força"]
                jogador["defesa base"] = dados_nivel["defesa"]
                mensagens.append(f"✦ NÍVEL {proximo_nivel} ALCANÇADO! ✦")
            break
    ui.tela_mensagem("VITÓRIA", mensagens, COR_EXP)
def sortear_item(ui, estado, dados):
    jogador = estado["jogador"]
    sala_atual = estado["sala atual"]
    item_sorteado = None
    poções_possiveis = dados["dados de interação"]["poção"]
    poções_filtradas = [p for p in poções_possiveis if p.get("raridade", 1) <= sala_atual]
    itens_filtrados = []
    if random.random() < 0.80:
        categoria = random.choices(["armas", "armaduras", "poção"], weights = [37, 38, 25], k = 1)[0]
        itens_possiveis = dados["dados de interação"][categoria]
        if categoria in ("armas", "armaduras"):
            itens_sala = [i for i in itens_possiveis if i.get("raridade", 1) <= sala_atual]
            nomes_possuidos = (
            [i["nome"] for i in jogador["inventario"]]
            + [jogador["arma"]["nome"], jogador["armadura"]["nome"]]
            + ["Espada Curta", "Armadura de Couro"]
            )
            itens_filtrados = [i for i in itens_sala if i["nome"] not in nomes_possuidos]
            if itens_filtrados:
                itens_possiveis = itens_filtrados
            else:
                itens_possiveis = poções_filtradas if poções_filtradas else [poções_possiveis[0]]
        else:
            itens_possiveis = poções_filtradas if poções_filtradas else [poções_possiveis[0]]
        item_sorteado = random.choice(itens_possiveis)
    else:
        tesouros = dados["dados de interação"]["tesouros"]
        tesouros_disponiveis = [t for t in tesouros if t["nome"] not in estado["tesouro coletado"] and t.get("raridade", 1) <= sala_atual]
        if tesouros_disponiveis:
            item_sorteado = random.choice(tesouros_disponiveis)
            estado["tesouro coletado"].append(item_sorteado["nome"])
        else:
            if itens_filtrados:
                itens_possiveis = itens_filtrados
            else:
                itens_possiveis = poções_filtradas if poções_filtradas else [poções_possiveis[0]]
            item_sorteado = random.choice(itens_possiveis)
    jogador["inventario"].append(item_sorteado)
    if   "ataque" in item_sorteado: descricao_item = f"+{item_sorteado['ataque']} ATK"
    elif "defesa" in item_sorteado: descricao_item = f"+{item_sorteado['defesa']} DEF"
    else:                           descricao_item = f"+{item_sorteado['cura']} HP"
    ui.tela_mensagem("ITEM ENCONTRADO",
                     ["Você encontrou:", f"  ✦ {item_sorteado['nome']} ({descricao_item})"],
                     COR_ITEM)
# Inventário
def loop_inventario(ui, estado, dados):
    while True:
        jogador   = estado["jogador"]
        inventario = jogador["inventario"]
        ui.tela_inventario(jogador, dados)
        curses.echo()
        curses.curs_set(1)
        try:
            escolha = ui.tela.getstr(ui.altura - 2, 12, 3).decode("utf-8").strip()
        except Exception:
            escolha = "0"
        curses.noecho()
        curses.curs_set(0)
        if escolha == "0":
            return
        if not escolha.isdigit() or not (0 < int(escolha) <= len(inventario)):
            ui.tela_mensagem("AVISO", ["Opção inválida."])
            continue
        item_escolhido = inventario[int(escolha) - 1]
        if "ataque" in item_escolhido:
            arma_atual = jogador["arma"]
            jogador["arma"] = item_escolhido
            inventario.remove(item_escolhido)
            inventario.append(arma_atual)
            ui.tela_mensagem("EQUIPADO", [f"{item_escolhido['nome']} equipado como arma!"], COR_ITEM)
        elif "defesa" in item_escolhido:
            armadura_atual = jogador["armadura"]
            jogador["armadura"] = item_escolhido
            inventario.remove(item_escolhido)
            inventario.append(armadura_atual)
            ui.tela_mensagem("EQUIPADO", [f"{item_escolhido['nome']} equipada como armadura!"], COR_ITEM)
        elif "cura" in item_escolhido:
            if jogador["vida atual"] >= jogador["vida max"]:
                ui.tela_mensagem("AVISO", ["Sua vida já está cheia!"])
            else:
                cura_total = item_escolhido["cura"]
                jogador["vida atual"] = min(jogador["vida max"], jogador["vida atual"] + cura_total)
                inventario.remove(item_escolhido)
                ui.tela_mensagem("CURADO",
                                 [f"Você usou {item_escolhido['nome']}.", f"+{cura_total} HP recuperado!"],
                                 COR_CURA)
# Loops principais
def loop_menu(ui, dados):
    while True:
        ui.tela_menu()
        curses.echo()
        curses.curs_set(1)
        try:
            opcao = ui.tela.getstr(ui.altura - 1, 0, 3).decode("utf-8").strip()
        except Exception:
            opcao = "3"
        curses.noecho()
        curses.curs_set(0)
        if opcao == "1":
            return novo_jogo(dados)
        elif opcao == "2":
            estado_salvo = carregar_jogo()
            if estado_salvo:
                ui.tela_mensagem("JOGO CARREGADO",
                                 ["Save encontrado!", "Bem-vindo de volta, herói."], COR_EXP)
                return estado_salvo
            else:
                ui.tela_mensagem("AVISO", ["Nenhum save encontrado."])
        elif opcao == "3":
            return None
def loop_jogo(ui, estado, dados):
    while estado["sala atual"] <= estado["sala totais"]:
        ui.tela_sala(estado["sala atual"], estado["sala totais"], estado["jogador"])
        curses.echo()
        curses.curs_set(1)
        try:
            opcao = ui.tela.getstr(ui.altura - 2, 12, 3).decode("utf-8").strip()
        except Exception:
            opcao = ""
        curses.noecho()
        curses.curs_set(0)

        if opcao == "1":
            sala = gerar_sala(estado, dados)
            if sala["tipo"] == "combate":
                sobreviveu = rodar_combate(ui, estado, sala["conteudo"], dados)
                if not sobreviveu:
                    ui.tela_fim_de_jogo(vitoria=False)
                    return
                sortear_item(ui, estado, dados)
            estado["sala atual"] += 1
        elif opcao == "2":
            loop_inventario(ui, estado, dados)
        elif opcao == "3":
            salvar_jogo(estado)
            ui.tela_mensagem("SALVO",
                             ["Jogo salvo com sucesso!", "Que as sombras te guardem..."], COR_EXP)
        elif opcao == "4":
            return
    ui.tela_fim_de_jogo(vitoria=True)
# Entrada
def _principal(tela):
    ui    = UI(tela)
    dados = carregar_dados()
    while True:
        estado = loop_menu(ui, dados)
        if estado is None:
            break
        loop_jogo(ui, estado, dados)
def main():
    thread_musica = threading.Thread(target=iniciar_musica, daemon=True)
    thread_musica.start()
    try:
        curses.wrapper(_principal)
    except KeyboardInterrupt:
        print("\nAté a próxima, aventureiro.")
    except curses.error as erro:
        print(f"Erro de terminal: {erro}")
        print("Terminal precisa suportar cores e ter no mínimo 80x24.")
        sys.exit(1)
    finally:
        parar_musica()
if __name__ == "__main__":
    main()
