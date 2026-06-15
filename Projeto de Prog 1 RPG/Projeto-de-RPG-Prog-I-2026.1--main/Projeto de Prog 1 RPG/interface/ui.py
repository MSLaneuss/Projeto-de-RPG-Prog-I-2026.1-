import curses
import time

COR_TITULO   = 1
COR_BORDA    = 2
COR_TEXTO    = 3
COR_OPCAO    = 4
COR_VIDA     = 5
COR_VIDA_OK  = 6
COR_DANO     = 7
COR_CURA     = 8
COR_EXP      = 9
COR_ITEM     = 10
COR_INIMIGO  = 11
COR_SOMBRA   = 12
COR_DESTAQUE = 13


def inicializar_cores():
    curses.start_color()
    curses.use_default_colors()

    if curses.can_change_color() and curses.COLORS >= 256:
        curses.init_color(100, 800, 650,   0)
        curses.init_color(101, 400, 400, 450)
        curses.init_color(102, 850, 830, 800)
        curses.init_color(103, 600, 200, 700)
        curses.init_color(104, 750, 100, 100)
        curses.init_color(105, 150, 700, 200)
        curses.init_color(106, 250, 250, 280)

        curses.init_pair(COR_TITULO,   100, -1)
        curses.init_pair(COR_BORDA,    101, -1)
        curses.init_pair(COR_TEXTO,    102, -1)
        curses.init_pair(COR_OPCAO,    103, -1)
        curses.init_pair(COR_VIDA,     104, -1)
        curses.init_pair(COR_VIDA_OK,  105, -1)
        curses.init_pair(COR_DANO,     curses.COLOR_RED,    -1)
        curses.init_pair(COR_CURA,     curses.COLOR_GREEN,  -1)
        curses.init_pair(COR_EXP,      curses.COLOR_CYAN,   -1)
        curses.init_pair(COR_ITEM,     curses.COLOR_YELLOW, -1)
        curses.init_pair(COR_INIMIGO,  104, -1)
        curses.init_pair(COR_SOMBRA,   106, -1)
        curses.init_pair(COR_DESTAQUE, curses.COLOR_WHITE,  -1)
    else:
        curses.init_pair(COR_TITULO,   curses.COLOR_YELLOW,  -1)
        curses.init_pair(COR_BORDA,    curses.COLOR_WHITE,   -1)
        curses.init_pair(COR_TEXTO,    curses.COLOR_WHITE,   -1)
        curses.init_pair(COR_OPCAO,    curses.COLOR_MAGENTA, -1)
        curses.init_pair(COR_VIDA,     curses.COLOR_RED,     -1)
        curses.init_pair(COR_VIDA_OK,  curses.COLOR_GREEN,   -1)
        curses.init_pair(COR_DANO,     curses.COLOR_RED,     -1)
        curses.init_pair(COR_CURA,     curses.COLOR_GREEN,   -1)
        curses.init_pair(COR_EXP,      curses.COLOR_CYAN,    -1)
        curses.init_pair(COR_ITEM,     curses.COLOR_YELLOW,  -1)
        curses.init_pair(COR_INIMIGO,  curses.COLOR_RED,     -1)
        curses.init_pair(COR_SOMBRA,   curses.COLOR_BLACK,   -1)
        curses.init_pair(COR_DESTAQUE, curses.COLOR_WHITE,   -1)


class UI:
    def __init__(self, tela):
        self.tela = tela
        curses.curs_set(0)
        self.tela.keypad(True)
        inicializar_cores()
        self.tela.clear()
        self.altura, self.largura = self.tela.getmaxyx()

    def cor(self, par, negrito=False):
        atributo = curses.color_pair(par)
        if negrito:
            atributo |= curses.A_BOLD
        return atributo

    def escrever(self, linha, coluna, texto, par=COR_TEXTO, negrito=False, centralizar=False, largura=None):
        try:
            if centralizar:
                larg = largura or self.largura
                coluna = max(0, (larg - len(texto)) // 2)
            self.tela.addstr(linha, coluna, texto, self.cor(par, negrito))
        except curses.error:
            pass

    def limpar(self):
        self.tela.clear()

    def atualizar(self):
        self.tela.refresh()

    def caixa(self, linha_ini, coluna_ini, altura, largura):
        try:
            self.tela.addstr(linha_ini, coluna_ini,
                "╔" + "═" * (largura - 2) + "╗", self.cor(COR_BORDA))
            for i in range(1, altura - 1):
                self.tela.addstr(linha_ini + i, coluna_ini, "║", self.cor(COR_BORDA))
                self.tela.addstr(linha_ini + i, coluna_ini + largura - 1, "║", self.cor(COR_BORDA))
            self.tela.addstr(linha_ini + altura - 1, coluna_ini,
                "╚" + "═" * (largura - 2) + "╝", self.cor(COR_BORDA))
        except curses.error:
            pass

    def barra_vida(self, linha, coluna, vida_atual, vida_maxima, largura=20):
        proporcao  = vida_atual / vida_maxima if vida_maxima > 0 else 0
        preenchido = int(proporcao * largura)
        vazio      = largura - preenchido

        if proporcao > 0.5:
            cor_barra = COR_VIDA_OK
        elif proporcao > 0.25:
            cor_barra = COR_EXP
        else:
            cor_barra = COR_VIDA

        try:
            self.tela.addstr(linha, coluna,                        "[",               self.cor(COR_BORDA))
            self.tela.addstr(linha, coluna + 1,                    "█" * preenchido,  self.cor(cor_barra, negrito=True))
            self.tela.addstr(linha, coluna + 1 + preenchido,       "░" * vazio,       self.cor(COR_SOMBRA))
            self.tela.addstr(linha, coluna + 1 + largura,          "]",               self.cor(COR_BORDA))
        except curses.error:
            pass

    def titulo_decorado(self, linha, texto, largura=None):
        larg      = largura or self.largura
        ornamento = f"⟨ {texto} ⟩"
        coluna    = (larg - len(ornamento)) // 2
        self.escrever(linha, coluna, ornamento, COR_TITULO, negrito=True)

    def aguardar_enter(self, linha, coluna=None, mensagem="[ Pressione ENTER para continuar ]"):
        if coluna is None:
            coluna = max(0, (self.largura - len(mensagem)) // 2)
        self.escrever(linha, coluna, mensagem, COR_SOMBRA)
        self.tela.refresh()
        while True:
            tecla = self.tela.getch()
            if tecla in (curses.KEY_ENTER, 10, 13):
                break

    def aguardar_tecla(self):
        return self.tela.getch()

    # ASCII

    def tela_menu(self):
        self.limpar()
        altura_tela = self.altura
        largura_tela = self.largura

        arte = [
            r"    ███╗   ███╗ █████╗ ███████╗███╗   ███╗ ██████╗ ██████╗ ██████╗  █████╗ ",
            r"    ████╗ ████║██╔══██╗██╔════╝████╗ ████║██╔═══██╗██╔══██╗██╔══██╗██╔══██╗",
            r"    ██╔████╔██║███████║███████╗██╔████╔██║██║   ██║██████╔╝██████╔╝███████║",
            r"    ██║╚██╔╝██║██╔══██║╚════██║██║╚██╔╝██║██║   ██║██╔══██╗██╔══██╗██╔══██║",
            r"    ██║ ╚═╝ ██║██║  ██║███████║██║ ╚═╝ ██║╚██████╔╝██║  ██║██║  ██║██║  ██║",
            r"    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝",
        ]
        subtitulo = "~ Das Profundezas da Masmorra ~"

        linha_arte = max(1, (altura_tela - 20) // 2 - 2)
        for i, linha in enumerate(arte):
            coluna_arte = max(0, (largura_tela - len(linha)) // 2)
            try:
                self.tela.addstr(linha_arte + i, coluna_arte, linha, self.cor(COR_TITULO, negrito=True))
            except curses.error:
                pass

        linha_sub = linha_arte + len(arte) + 1
        self.escrever(linha_sub, 0, subtitulo, COR_SOMBRA, centralizar=True, largura=largura_tela)

        opcoes      = [("1", "Novo Jogo"), ("2", "Carregar Jogo"), ("3", "Sair")]
        larg_caixa  = 30
        col_caixa   = (largura_tela - larg_caixa) // 2
        linha_caixa = linha_sub + 3

        self.caixa(linha_caixa, col_caixa, len(opcoes) + 4, larg_caixa)
        self.titulo_decorado(linha_caixa + 1, "MENU", largura=largura_tela)

        for i, (numero, texto) in enumerate(opcoes):
            entrada = f"  [{numero}]  {texto}"
            self.escrever(linha_caixa + 3 + i,
                          col_caixa + (larg_caixa - len(entrada)) // 2,
                          entrada, COR_OPCAO, negrito=True)

        rodape = "✦ ── ── ── ── ── ── ── ── ── ── ── ── ✦"
        self.escrever(altura_tela - 2, 0, rodape, COR_SOMBRA, centralizar=True, largura=largura_tela)
        self.atualizar()

    def tela_sala(self, sala_atual, salas_totais, jogador):
        self.limpar()
        altura_tela  = self.altura
        largura_tela = self.largura

        self.caixa(0, 1, 3, largura_tela - 2)
        titulo = f"MASMORRA  —  SALA {sala_atual} / {salas_totais}"
        self.titulo_decorado(1, titulo, largura=largura_tela)

        larg_status = 32
        self.caixa(3, 1, 10, larg_status)
        self.titulo_decorado(4, "HERÓI", largura=larg_status + 2)

        nivel        = jogador["lvl"]
        vida_atual   = jogador["vida atual"]
        vida_maxima  = jogador["vida max"]
        forca        = jogador["força"]
        defesa_total = jogador["defesa base"] + jogador["armadura"]["defesa"]
        nome_arma    = jogador["arma"]["nome"]
        nome_armad   = jogador["armadura"]["nome"]

        self.escrever(6,  3, f"  Nível  : {nivel}",                         COR_EXP,  negrito=True)
        self.escrever(7,  3, f"  Força  : {forca}   Defesa: {defesa_total}", COR_TEXTO)
        self.escrever(8,  3,  "  Vida   :",                                  COR_TEXTO)
        self.barra_vida(8, 13, vida_atual, vida_maxima, largura=14)
        self.escrever(9,  3, f"  {vida_atual}/{vida_maxima}",
                      COR_VIDA if vida_atual < vida_maxima // 2 else COR_VIDA_OK)
        self.escrever(10, 3, f"  ⚔  {nome_arma[:22]}",  COR_ITEM)
        self.escrever(11, 3, f"  🛡  {nome_armad[:20]}", COR_ITEM)

        larg_mapa  = largura_tela - larg_status - 4
        col_mapa   = larg_status + 2
        self.caixa(3, col_mapa, 10, larg_mapa)
        self.titulo_decorado(4, "MASMORRA", largura=col_mapa * 2 + larg_mapa)

        progresso      = sala_atual / salas_totais
        blocos         = int(progresso * (larg_mapa - 6))
        barra_progresso = "█" * blocos + "░" * (larg_mapa - 6 - blocos)
        self.escrever(6, col_mapa + 2, f"Prog: [{barra_progresso}]", COR_EXP)

        qtd_itens = len(jogador["inventario"])
        self.escrever(8, col_mapa + 2, f"  Mochila: {qtd_itens} item(s)", COR_ITEM)
        self.escrever(9, col_mapa + 2, f"  EXP: {jogador['exp']}",        COR_EXP)

        linha_acoes = 13
        self.caixa(linha_acoes, 1, 8, largura_tela - 2)
        self.titulo_decorado(linha_acoes + 1, "AÇÕES", largura=largura_tela)

        acoes = [
            ("[1]", "Avançar para a próxima sala"),
            ("[2]", "Abrir inventário"),
            ("[3]", "Salvar jogo"),
            ("[4]", "Voltar ao menu principal"),
        ]
        for i, (tecla, descricao) in enumerate(acoes):
            self.escrever(linha_acoes + 3 + i, 4, tecla,     COR_OPCAO, negrito=True)
            self.escrever(linha_acoes + 3 + i, 9, descricao, COR_TEXTO)

        self.escrever(altura_tela - 2, 3, "Escolha: ", COR_OPCAO, negrito=True)
        self.atualizar()

    def tela_combate(self, jogador, monstro, registro=None):
        self.limpar()
        altura_tela  = self.altura
        largura_tela = self.largura

        self.caixa(0, 1, 3, largura_tela - 2)
        self.titulo_decorado(1, "⚔  COMBATE  ⚔", largura=largura_tela)

        metade = (largura_tela - 3) // 2

        self.caixa(3, 1, 8, metade)
        self.titulo_decorado(4, "HERÓI", largura=metade + 2)

        vida_jogador    = jogador["vida atual"]
        vida_max_jog    = jogador["vida max"]
        ataque_jogador  = jogador["força"] + jogador["arma"]["ataque"]
        defesa_jogador  = jogador["defesa base"] + jogador["armadura"]["defesa"]

        self.escrever(5, 3, f"  Lvl {jogador['lvl']}  ⚔ {ataque_jogador} ATK", COR_TEXTO)
        self.escrever(6, 3, "  Vida: ", COR_TEXTO)
        self.barra_vida(6, 11, vida_jogador, vida_max_jog, largura=metade - 14)
        cor_vida_jog = COR_VIDA if vida_jogador < vida_max_jog // 2 else COR_VIDA_OK
        self.escrever(7, 3, f"  {vida_jogador}/{vida_max_jog} HP", cor_vida_jog, negrito=True)
        self.escrever(8, 3, f"  🛡 DEF: {defesa_jogador}",                       COR_ITEM)
        self.escrever(9, 3, f"  ⚔  {jogador['arma']['nome'][:metade-6]}",        COR_ITEM)

        col_inimigo = metade + 2
        self.caixa(3, col_inimigo, 8, largura_tela - col_inimigo - 1)
        self.titulo_decorado(4, monstro.get("nome", "???"),
                             largura=(col_inimigo * 2 + (largura_tela - col_inimigo - 1)))

        vida_monstro     = monstro.get("vida", 0)
        vida_max_monstro = monstro.get("vida_max", vida_monstro)
        cor_vida_mon     = COR_VIDA if vida_monstro < vida_max_monstro // 2 else COR_INIMIGO

        self.escrever(5, col_inimigo + 2,
                      f"  Lvl {monstro.get('lvl','?')}  ⚔ {monstro.get('ataque','?')} ATK", COR_INIMIGO)
        self.escrever(6, col_inimigo + 2, "  Vida: ", COR_TEXTO)
        self.barra_vida(6, col_inimigo + 10, vida_monstro, vida_max_monstro,
                        largura=largura_tela - col_inimigo - 14)
        self.escrever(7, col_inimigo + 2, f"  {vida_monstro}/{vida_max_monstro} HP",
                      cor_vida_mon, negrito=True)

        linha_log  = 11
        altura_log = altura_tela - linha_log - 6
        self.caixa(linha_log, 1, altura_log, largura_tela - 2)
        self.titulo_decorado(linha_log + 1, "LOG DE BATALHA", largura=largura_tela)

        if registro:
            for i, (mensagem, cor_par) in enumerate(registro[-(altura_log - 4):]):
                self.escrever(linha_log + 3 + i, 3, f"  › {mensagem}"[:largura_tela - 6], cor_par)

        linha_acoes = altura_tela - 5
        self.caixa(linha_acoes, 1, 4, largura_tela - 2)
        for i, acao in enumerate(["[1] Atacar", "[2] Usar Poção"]):
            self.escrever(linha_acoes + 1, 4 + i * 20, acao, COR_OPCAO, negrito=True)

        self.escrever(altura_tela - 2, 3, "Sua ação: ", COR_OPCAO, negrito=True)
        self.atualizar()

    def tela_inventario(self, jogador, dados):
        self.limpar()
        altura_tela  = self.altura
        largura_tela = self.largura

        nivel = jogador["lvl"]
        lista_niveis = dados["dados de interação"]["jogador"]
        if nivel < len(lista_niveis):
            exp_necessaria = lista_niveis[nivel]["exp necessario"]
        else:
            exp_necessaria = "MAX"

        self.caixa(0, 1, 3, largura_tela - 2)
        self.titulo_decorado(1, "INVENTÁRIO", largura=largura_tela)

        larg_status = 35
        self.caixa(3, 1, 10, larg_status)
        self.titulo_decorado(4, "STATUS", largura=larg_status + 2)

        vida_atual  = jogador["vida atual"]
        vida_maxima = jogador["vida max"]
        cor_vida    = COR_VIDA_OK if vida_atual > vida_maxima // 2 else COR_VIDA

        self.escrever(6,  3, f"  Nível  : {nivel}",                                           COR_EXP, negrito=True)
        self.escrever(7,  3, f"  EXP    : {jogador['exp']} / {exp_necessaria}",               COR_EXP)
        self.escrever(8,  3,  "  Vida   :",                                                    COR_TEXTO)
        self.barra_vida(8, 13, vida_atual, vida_maxima, largura=18)
        self.escrever(9,  3, f"  {vida_atual}/{vida_maxima} HP",                               cor_vida)
        self.escrever(10, 3, f"  Força  : {jogador['força']}   Defesa base: {jogador['defesa base']}", COR_TEXTO)
        self.escrever(11, 3, f"  ⚔  {jogador['arma']['nome']} (+{jogador['arma']['ataque']} ATK)",     COR_ITEM)
        self.escrever(12, 3, f"  🛡 {jogador['armadura']['nome']} (+{jogador['armadura']['defesa']} DEF)", COR_ITEM)

        col_mochila  = larg_status + 2
        larg_mochila = largura_tela - col_mochila - 2
        inventario   = jogador["inventario"]
        altura_mochila = max(10, len(inventario) + 6)

        self.caixa(3, col_mochila, altura_mochila, larg_mochila)
        self.titulo_decorado(4, "MOCHILA", largura=col_mochila * 2 + larg_mochila)

        if not inventario:
            self.escrever(6, col_mochila + 2, "  A mochila está vazia...", COR_SOMBRA)
        else:
            for i, item in enumerate(inventario):
                if "ataque" in item:
                    descricao_item = f"⚔  {item['nome']} (+{item['ataque']} ATK)"
                    cor_item       = COR_ITEM
                elif "defesa" in item:
                    descricao_item = f"🛡 {item['nome']} (+{item['defesa']} DEF)"
                    cor_item       = COR_ITEM
                elif "cura" in item:
                    descricao_item = f"⚗  {item['nome']} (+{item['cura']} HP)"
                    cor_item       = COR_CURA
                else:
                    descricao_item = item["nome"]
                    cor_item       = COR_TEXTO
                self.escrever(6 + i, col_mochila + 2,
                              f"  [{i+1}] {descricao_item}"[:larg_mochila - 3], cor_item)

        linha_instrucao = 3 + altura_mochila + 1
        self.escrever(linha_instrucao, 3,
                      "  Escolha o número do item para usar/equipar, ou [0] para voltar:", COR_SOMBRA)

        self.escrever(altura_tela - 2, 3, "Escolha: ", COR_OPCAO, negrito=True)
        self.atualizar()

    def tela_fim_de_jogo(self, vitoria=False):
        self.limpar()
        altura_tela  = self.altura
        largura_tela = self.largura

        if vitoria:
            linhas = [
                "╔═══════════════════════════════════════╗",
                "║   ★  MASMORRA CONCLUÍDA!  ★          ║",
                "║   O herói emergiu vitorioso das       ║",
                "║   profundezas, lendas serão contadas. ║",
                "╚═══════════════════════════════════════╝",
            ]
            cor_tela = COR_TITULO
        else:
            linhas = [
                "╔═══════════════════════════════════════╗",
                "║         ✝  VOCÊ MORREU  ✝            ║",
                "║   As trevas da masmorra reclamaram    ║",
                "║   mais uma alma perdida...            ║",
                "╚═══════════════════════════════════════╝",
            ]
            cor_tela = COR_VIDA

        linha_ini = (altura_tela - len(linhas)) // 2
        for i, linha in enumerate(linhas):
            coluna = (largura_tela - len(linha)) // 2
            try:
                self.tela.addstr(linha_ini + i, coluna, linha, self.cor(cor_tela, negrito=True))
            except curses.error:
                pass

        self.escrever(altura_tela - 3, 0,
                      "[ Pressione qualquer tecla para continuar ]",
                      COR_SOMBRA, centralizar=True, largura=largura_tela)
        self.atualizar()
        self.aguardar_tecla()

    def tela_mensagem(self, titulo, linhas, cor=COR_TEXTO):
        self.limpar()
        altura_tela  = self.altura
        largura_tela = self.largura

        larg_caixa  = min(largura_tela - 4, max(40, max(len(l) for l in linhas) + 6))
        altura_caixa = len(linhas) + 6
        linha_ini   = (altura_tela  - altura_caixa) // 2
        col_ini     = (largura_tela - larg_caixa)   // 2

        self.caixa(linha_ini, col_ini, altura_caixa, larg_caixa)
        self.titulo_decorado(linha_ini + 1, titulo, largura=largura_tela)

        for i, linha in enumerate(linhas):
            self.escrever(linha_ini + 3 + i, col_ini + 3, linha[:larg_caixa - 5], cor)

        self.aguardar_enter(linha_ini + altura_caixa - 1)
        self.atualizar()
