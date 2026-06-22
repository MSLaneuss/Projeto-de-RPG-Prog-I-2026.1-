import json
import os
import random

with open("dados.json", "r", encoding = "utf-8") as arquivos:
    dados= json.load(arquivos)
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")
def menu():
    while True:
        limpar_tela()
        print("=" * 60)
        print("Masmorra em Python".center(60))
        print("=" * 60)
        print("[1] - Novo Jogo".center(60))
        print("[2] - Carregar Jogo".center(60))
        print("[3] - Sair".center(60))
        print("=" * 60)
        opção_m = input("Escolha sua opção: ").strip()
        if opção_m == "1":
            return novo_jogo()
        elif opção_m == "2":
            dados_carregados = carregar()
            if dados_carregados:
                return dados_carregados
        elif opção_m == "3":
            exit()
def novo_jogo():
    limpar_tela()
    lvl_1 = dados["dados de interação"]["jogador"][0]
    lista_poções = dados["dados de interação"]["poção"]
    poção_media = None
    for p in lista_poções:
        if p["nome"] == "Poção de Cura Média":
                poção_media = p
                break
    inventario_inicial = [poção_media] if poção_media else []
    estado_jogo = {
        "jogador": {
            "lvl": 1,
            "vida max": lvl_1["vida"],
            "vida atual": lvl_1["vida"],
            "força": lvl_1["força"],
            "defesa base": lvl_1["defesa"],
            "exp": 0,
            "arma": dados["dados de interação"]["armas"][0],
            "armadura": dados["dados de interação"]["armaduras"][0],
            "inventario": inventario_inicial
         },
        "sala atual": 1,
        "sala totais": 20,
        "tesouro coletado": []
    }
    return estado_jogo
def salvar(estado_jogo):
    with open("save.json", "w", encoding = "utf-8") as salvo:
        json.dump(estado_jogo, salvo, indent = 4, ensure_ascii = False)
        print("Jogo Salvo!".center(60))
        input("Pressione Enter para continuar...".center(60))
def carregar():
    if not os.path.exists("save.json"):
        print("Nenhum Save encontrado.".center(60))
        input("Pressione Enter para continuar...".center(60))
        return None
    try:
        with open("save.json", "r", encoding="utf-8") as salvo:
            save_carregado = json.load(salvo)
            print("Jogo Carregado!".center(60))
            input("Pressione Enter para continuar...".center(60))
            return save_carregado
    except Exception as motivo:
        print(f"Erro ao ler o save: {motivo}".center(60))
        input("Pressione Enter para continuar...".center(60))
        return None
def gerar_masmorra(estado_jogo):
    sala_atual = estado_jogo["sala atual"]
    salas_totais = estado_jogo["sala totais"]
    if sala_atual == salas_totais:
        dragão = dados["dados de interação"]["monstros"][-1]
        return{"tipo": "combate", "conteudo": dict(dragão)}
    progresso = sala_atual / salas_totais
    if progresso <= 0.15:
        lvl_max = 0
    elif progresso > 0.15 and progresso <= 0.35:
        lvl_max = 1
    elif progresso > 0.35 and progresso <= 0.50:
        lvl_max = 2
    elif progresso > 0.50 and progresso <= 0.60:
        lvl_max = 3
    else:
        lvl_max = 4
    monstro_disponivel = [m for m in dados["dados de interação"]["monstros"] if m["lvl"] == lvl_max and m["lvl"] < 5]
    if not monstro_disponivel:
        monstro_disponivel = [dados["dados de interação"]["monstros"][0]]
    monstro_sorteado = random.choice(monstro_disponivel)
    return {"tipo": "combate", "conteudo": dict(monstro_sorteado)}
def combate(estado_jogo, monstro):
    limpar_tela()
    jogador = estado_jogo["jogador"]
    print(f"Um(a) {monstro["nome"]} apareceu!")
    while jogador["vida atual"] > 0 and monstro["vida"] > 0:
        print("=" * 60)
        print(f"Sua Vida: {jogador["vida atual"]}/{jogador["vida max"]}".center(60))
        print(f"Vida do(a) {monstro["nome"]}: {monstro["vida"]}".center(60))
        print("[1] - Atacar".center(60))
        print("[2] - Usar Poção".center(60))
        print("=" * 60)
        ação = input("O que irá fazer? ".center(60)).strip()
        if ação == "1":
            limpar_tela()
            dano_jogador = jogador["força"] + jogador["arma"]["ataque"]
            monstro["vida"] -= dano_jogador
            print(f"Você causou {dano_jogador} de dano no {monstro["nome"]}!")
            if monstro["vida"] <= 0:
                print(f"Você Matou o(a) {monstro["nome"]}!")
                vitoria(jogador, monstro["exp"])
                break
            defesa_total = jogador["defesa base"] + jogador["armadura"]["defesa"]
            dano_monstro = max(1, monstro["ataque"] - defesa_total)
            jogador["vida atual"] -= dano_monstro
            print(f"{monstro["nome"]} te causou {dano_monstro} de dano!")
        elif ação == "2":
            poções_disponiveis = [i for i in jogador["inventario"] if "cura" in i]
            if not poções_disponiveis:
                print("Você não tem poções de cura no iventário.".center(60))
                continue
            limpar_tela()
            print("=" * 60)
            print("Poções".center(60))
            print("=" * 60)
            for i, poção in enumerate(poções_disponiveis):
                print(f"{i + 1}. {poção["nome"]} (+{poção["cura"]} de Vida)")
            print("=" * 60)
            print("0 para voltar".center(60))
            print("=" * 60) 
            curar = input("Escolha a poção (ou digite 0 para voltar): ".center(60)).strip()
            if curar == "0":
                limpar_tela()
                print("Ação cancelada".center(60))
                continue
            if curar.isdigit() and 0 < int(curar) <= len(poções_disponiveis):
                limpar_tela()
                poção_escolhida = poções_disponiveis[int(curar) -1]
                jogador["vida atual"] += poção_escolhida["cura"]
                if jogador["vida atual"] > jogador["vida max"]:
                    jogador["vida atual"] = jogador["vida max"]
                print(f"Você usou {poção_escolhida["nome"]} e recuperou {poção_escolhida["cura"]} de Vida!")
                jogador["inventario"].remove(poção_escolhida)
                defesa_total = jogador["defesa base"] + jogador["armadura"]["defesa"]
                dano_monstro = max(1, monstro["ataque"] - defesa_total)
                jogador["vida atual"] -= dano_monstro
                print(f"{monstro["nome"]} te causou {dano_monstro} de dano!")
            else:
                limpar_tela()
                print("Ação invalida".center(60))
                continue
        else:
            limpar_tela()
            print("Opção inválida!".center(60))
            continue
    return jogador["vida atual"] > 0
def vitoria(jogador, exp_ganho):
    jogador["exp"] += exp_ganho
    print(f"Você ganhou {exp_ganho} de Exp!".center(60))
    proximo_lvl = jogador["lvl"] + 1
    for lvl in dados["dados de interação"]["jogador"]:
        if lvl["lvl"] == proximo_lvl:
            if jogador["exp"] >= lvl["exp necessario"]:
                jogador["lvl"] = proximo_lvl
                jogador["vida max"] = lvl["vida"]
                jogador["vida atual"] = lvl["vida"]
                jogador["força"] = lvl["força"]
                jogador["defesa base"] = lvl["defesa"]
                print(f"Nível {proximo_lvl} adiquirido!".center(60))
            break
def inventario(estado_jogo):
    jogador = estado_jogo["jogador"]
    while True:
        if jogador["lvl"] < len(dados["dados de interação"]["jogador"]):
            proximo_lvl = dados["dados de interação"]["jogador"][jogador["lvl"]]
            exp_precisa = proximo_lvl["exp necessario"]
        else:
            exp_precisa = "Max"
        limpar_tela()
        print("=" * 60)
        print(f"Lvl: {jogador["lvl"]}".center(60))
        print(f"Exp: {jogador["exp"]}/{exp_precisa}".center(60))
        print(f"Vida atual: {jogador["vida atual"]}/{jogador["vida max"]}".center(60))
        print(f"Força: {jogador["força"]}".center(60))
        print(f"Defesa: {jogador["defesa base"]}".center(60))
        print(f"Arma equipada: {jogador["arma"]["nome"]} (+{jogador["arma"]["ataque"]} Atk)".center(60))
        print(f"Armadura equipada: {jogador["armadura"]["nome"]} (+{jogador["armadura"]["defesa"]} Def)".center(60))
        print("=" * 60)
        print("Mochila".center(60))
        print("=" * 60)
        if not jogador["inventario"]:
            print("Mochila vazia".center(60))
            print("=" * 60)
            print("0 para voltar".center(60))
            opção_i = input("Escolha uma ação: ".center(60)).strip()
            if opção_i == "0":
                return
            continue
        for i, item in enumerate(jogador["inventario"]):
            if "ataque" in item:
                texto_item = f"{i + 1}. {item["nome"]} 3(Arma: +{item["ataque"]} Atk)"
            elif "defesa" in item:
                texto_item = f"{i + 1}. {item["nome"]} (Armadura: +{item["defesa"]} Def)"
            elif "cura" in item:
                texto_item = f"{i + 1}. {item["nome"]} (Poção: +{item["cura"]} Vida)"
            print(texto_item.center(60))
        print("=" * 60)
        print("0 para voltar".center(60))
        escolha = input("Escolha o item:".center(60)).strip()
        if escolha == "0":
            return
        if escolha.isdigit() and 0 < int(escolha) <= len(jogador["inventario"]):
            item_escolhido = jogador["inventario"][int(escolha) -1]
            if "ataque" in item_escolhido:
                arma_antiga = jogador["arma"]
                jogador["arma"] = item_escolhido
                jogador["inventario"].remove(item_escolhido)
                jogador["inventario"].append(arma_antiga)
                print(f"{item_escolhido["nome"]} equipado!".center(60))
                input("Pressione Enter para continuar...".center(60))
            elif "defesa" in item_escolhido:
                armadura_antiga = jogador["armadura"]
                jogador["armadura"] = item_escolhido
                jogador["inventario"].remove(item_escolhido)
                jogador["inventario"].append(armadura_antiga)
                print(f"{item_escolhido["nome"]} equipado!".center(60))
                input("Pressione Enter para continuar...".center(60))
            elif "cura" in item_escolhido:
                if jogador["vida atual"] >= jogador["vida max"]:
                    print("Vida cheia!".center(60))
                else:
                    jogador["vida atual"] += item_escolhido["cura"]
                    if jogador["vida atual"] > jogador["vida max"]:
                        jogador["vida atual"] = jogador["vida max"]
                    print(f"{item_escolhido["nome"]} usada!")
                    input("Pressione Enter para continuar...".center(60))
                    jogador["inventario"].remove(item_escolhido)
        else:
            print("Opção inválida".center(60))
            input("Pressione Enter para continuar...".center(60))
def jogo():
    estado_jogo = menu()
    item_dropado = None
    if estado_jogo is None:
        return
    while estado_jogo["sala atual"] <= estado_jogo["sala totais"]:
        limpar_tela()
        print("=" * 60)
        print(f"Sala {estado_jogo["sala atual"]}/{estado_jogo["sala totais"]}".center(60))
        print("=" * 60)
        print("[1] - Avançar para a próxima sala".center(60))
        print("[2] - Abrir inventário".center(60))
        print("[3] - Salvar jogo".center(60))
        print("[4] - Voltar ao Menu principal".center(60))
        print("=" * 60)
        opção_j = input("O que irá fazer? ").strip()
        if opção_j == "1":
            sala = gerar_masmorra(estado_jogo)
            if sala["tipo"] == "combate":
                vivo = combate(estado_jogo, sala["conteudo"])
                if not vivo:
                    print("Você morreu! Fim...".center(60))
                    input("Pressione Enter para continuar...".center(60))
                    return
                if estado_jogo["sala atual"] <= estado_jogo["sala totais"]:
                    if random.random() < 0.80:
                        categoria = random.choice(["armas", "armaduras", "poção"])
                        itens_possiveis = dados["dados de interação"][categoria]
                        if categoria in ["armas", "armaduras"]:
                            sala_atual = estado_jogo["sala atual"]
                            itens_sala = [i for i in itens_possiveis if i.get("raridade", 1) <= sala_atual]
                            itens_adquiridos = [i["nome"] for i in estado_jogo["jogador"]["inventario"]]
                            itens_adquiridos.append(estado_jogo["jogador"]["arma"]["nome"])
                            itens_adquiridos.append(estado_jogo["jogador"]["armadura"]["nome"])
                            itens_adquiridos.extend(["Espada Curta", "Armadura de Couro"])
                            itens_filtrados = [i for i in itens_possiveis if i["nome"] not in itens_adquiridos]
                            if itens_filtrados:
                                itens_possiveis = itens_filtrados
                            elif itens_sala:
                                itens_possiveis = itens_sala
                            else:
                                itens_possiveis = dados["dados de interação"]["poção"]
                        if itens_possiveis:
                            item_dropado = random.choice(itens_possiveis)
                        else:
                            itens_possiveis = dados["dados de interação"]["poção"]
                            item_dropado = random.choice(itens_possiveis)
                    else:
                        tesouros = dados["dados de interação"]["tesouros"]
                        tesouro_disponivel = [t for t in tesouros if t["nome"] not in estado_jogo["tesouro coletado"] and t.get("raridade", 1) <= sala_atual]
                        if tesouro_disponivel:
                            item_dropado = random.choice(tesouro_disponivel)
                            estado_jogo["tesouro coletado"].append(item_dropado["nome"])
                        else:
                            itens_possiveis = dados["dados de interação"]["poção"]
                            item_dropado = random.choice(itens_possiveis)
                    if item_dropado:
                        estado_jogo["jogador"]["inventario"].append(item_dropado)
                        print(f"Você encontrou: {item_dropado["nome"]}!".center(60))
                        input("Pressione Enter para continuar...".center(60))
                    print("=" * 60)
            estado_jogo["sala atual"] += 1
        elif opção_j == "2":
            inventario(estado_jogo)
            continue
        elif opção_j == "3":
            salvar(estado_jogo)
            continue
        elif opção_j == "4":
            return
    limpar_tela()
    print("=" * 60)
    print("Masmorra Concluída!".center(60))
    print("=" * 60)