"""Roda os 3 casos de teste e grava um log de cada um na pasta logs/.

Uso: python testar_casos.py
"""
from cadeia_backup import gerar_plano

CASOS = [
    {"serie": 8, "tema": "Equações do 1º grau", "duracao": 50, "perfil": "turma regular"},
    {"serie": 6, "tema": "Adição e subtração de frações", "duracao": 50, "perfil": "turma com dificuldade em frações"},
    {"serie": 9, "tema": "Teorema de Pitágoras", "duracao": 100, "perfil": "turma regular, aula dupla"},
]

for numero, caso in enumerate(CASOS, 1):
    print(f"\n=== Caso {numero}: {caso['serie']}º ano, {caso['tema']} ({caso['duracao']} min) ===")
    resultado = gerar_plano(**caso, ao_avancar=lambda texto: print("  -", texto))
    print("  Candidatas:", ", ".join(resultado["candidatas"]))
    for h in resultado["habilidades"]:
        print(f"  Habilidade: {h['codigo']} ({h['tipo']})")
    for v in resultado["verificacoes_codigo"]:
        print(f"  [{v['resultado']}] {v['pergunta']} {v['detalhe']}")
    print("  Log:", resultado["arquivo_log"])
