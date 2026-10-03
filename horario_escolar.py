# /// script
# dependencies = ["marimo"]
# requires-python = ">=3.14"
# ///

import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    #TP1.1
            Vou começar por criar uma função capaz de ler os ficheiros na pasta dados.
    """)
    return


@app.cell
def _():
    import pandas as pd


    return (pd,)


@app.cell
def _(Bool):
    from dataclasses import dataclass

    #fácil compreensão
    @dataclass
    class Disciplina:
        nome: str
        prof: str
        carga: int
        duplo: bool
        sala: None | str


    #Representa quando um professor não pode dar aula. Preciso converter o dia para uma posição na lista para depois por a hora-1 como posição da sublista. Pode também ser None no caso do professor estar sempre disponivél.
    @dataclass
    class Disponibilidade:
        prof: str
        horas: list[list[Bool]]

    #esp = se é especial ou não
    @dataclass
    class Sala:
        nome: str
        esp: Bool
        quantidade: int

    @dataclass
    class Turma:
        nome: str



    return Disciplina, Disponibilidade, Sala, Turma, dataclass


@app.cell
def _(Sala, pd):
    def carregar_salas() -> list[Sala]:
        c=pd.read_csv("dados/salas.csv")
        salas = []
        for _, row in c.iterrows():
            sala = Sala(
                nome=row["sala"],
                esp=row["tipo"] == "especial",
                quantidade=int(row["quantidade"])
            )
            salas.append(sala)
        return salas

    return (carregar_salas,)


@app.cell
def _(Disponibilidade, pd):
    def dia_int(n)->int:
        match n:
            case "Seg":
                a=0
            case "Ter":
                a=1
            case "Qua":
                a=2
            case "Qui":
                a=3
            case "Sex":
                a=4
        return a

    def carregar_disponibilidade_excessoes() -> list[Disponibilidade]:
        b=pd.read_csv("dados/disponibilidade_excecoes.csv")

        x = Disponibilidade(
            prof=b.loc[0,"professor"],
            horas=[[True,True,True,True,True],[True,True,True,True,True],[True,True,True,True,True],[True,True,True,True,True],[True,True,True,True,True]]
        )

        valor = []
        for _, row in b.iterrows():
            if row["professor"]==x.prof:
                x.horas[dia_int(row["dia"])][int(row["periodo"])-1] = False
            else:
                valor.append(x)
                x = Disponibilidade(
                prof=row["professor"],
                horas=[[True,True,True,True,True],[True,True,True,True,True],[True,True,True,True,True],[True,True,True,True,True],[True,True,True,True,True]]
                )
                x.horas[dia_int(row["dia"])][int(row["periodo"])-1] = False
        valor.append(x)
        return valor

    return (carregar_disponibilidade_excessoes,)


@app.cell
def _(Turma, pd):
    def carregar_turmas() -> list[Turma]:
        d=pd.read_csv("dados/turmas.csv")
        valor = []
        for _, row in d.iterrows():
            x=Turma(nome = row["turma"])
    
            valor.append(x)
        return valor


    return (carregar_turmas,)


@app.cell
def _(Disciplina, pd):
    def carregar_disciplinas() -> list[Disciplina]:
        a=pd.read_csv("dados/disciplinas.csv")
        valor = []
        for _, row in a.iterrows():
            x=Disciplina(
                nome=row["disciplina"],
                prof=row["professor"],
                carga=int(row["carga_semanal"]),
                duplo=row["duplo_periodo"]=="sim",
                sala= None if pd.isna(row["sala_especial"]) else row["sala_especial"],
            )
            valor.append(x)
        return valor
    cena_da_disciplina = carregar_disciplinas()
    print(cena_da_disciplina)
    return (carregar_disciplinas,)


@app.cell
def _(carregar_turmas):
    def _():
        teste=carregar_turmas()
        return print(teste)


    _()
    return


@app.cell
def _(carregar_disciplinas):
    def _():
        teste=carregar_disciplinas()
        return print(teste)


    _()
    return


@app.cell
def _(carregar_disponibilidade_excessoes):
    def _():
        teste=carregar_disponibilidade_excessoes()
        return print(teste)


    _()
    return


@app.cell
def _(carregar_salas):
    def _():
        teste=carregar_salas()
        return print(teste)


    _()
    return


@app.cell
def _(
    carregar_disciplinas,
    carregar_disponibilidade_excessoes,
    carregar_salas,
    carregar_turmas,
):
    todas_as_disciplinas = carregar_disciplinas()
    todas_as_excessoes = carregar_disponibilidade_excessoes()
    todas_as_salas = carregar_salas()
    todas_as_turmas = carregar_turmas()
    return (todas_as_disciplinas,)


@app.cell
def _(Turma, dataclass):
    @dataclass
    class Aula:
        disciplina: str
        prof: str
        sala: None | str


    @dataclass
    class Horário:
        aulas: list[list[Aula]]
        turma: Turma

    return


@app.cell
def _():
    #from ortools.sat.python import cp_model
    #model = cp_model.CpModel()
    return


@app.cell
def _(Disciplina, todas_as_disciplinas):
    def ve_se_tem_outra_disciplina_com_o_mesmo_professor(a,disciplinas) -> bool:
        for b in disciplinas:
            if a.prof == b.prof and a.nome != b.nome:
                return True
        return False

    #dá uma lista de int que dão as prioridades na marcação de aulas
    def define_prioridade(disciplinas)-> list[int]:
        valor = []

        #a é do tipo da disciplina
        for a in disciplinas:
            prioridade = 0
            prioridade += a.carga
            if a.duplo:
                prioridade += 10
            if a.sala != None:
                prioridade += 10
            if ve_se_tem_outra_disciplina_com_o_mesmo_professor(a,disciplinas):
                prioridade+=12
            valor.append(prioridade)
        return valor

    def ordena(disciplinas,a) -> list[Disciplina]:
        return [d for _, d in sorted(zip(a, disciplinas), key=lambda x: x[0], reverse=True)]
        
        
    
    a = define_prioridade(todas_as_disciplinas)
    print (a)
    bruh = ordena(todas_as_disciplinas,a)
    print(bruh)
    a=define_prioridade(bruh)
    print(a)
        
    return


if __name__ == "__main__":
    app.run()
