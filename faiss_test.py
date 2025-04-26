# Integración básica de EmbeddingsGenerator y FAISSManager

from src.embeddings import EmbeddingsGenerator
from src.faiss import FAISSManager

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import os
from pathlib import Path

def main():
    # Inicializa el generador y el manager
    emb_gen = EmbeddingsGenerator()
    faiss_index_path = Path(__file__).parent / "data" / "faiss_test_index"
    faiss_mgr = FAISSManager(dimension=emb_gen.get_dimension())

    # Intentar cargar el índice si existe
    if (faiss_index_path.with_suffix(".index").exists() and
        faiss_index_path.with_suffix(".texts.pkl").exists()):
        faiss_mgr.load(str(faiss_index_path))
        print("Índice FAISS cargado desde disco.")
    else:
        print("No existe índice FAISS persistente. Se creará uno nuevo.")
        # Prepara textos y genera embeddings
        texts = [
            "La inteligencia artificial es fascinante.",
            "La carpintería requiere precisión.",
            "Los modelos de lenguaje procesan texto."
        ]
        embeddings = emb_gen.generate(texts)
        faiss_mgr.add_embeddings(embeddings, texts)
        faiss_mgr.save(str(faiss_index_path))
        print("Índice FAISS guardado en disco.")

    # Consulta: genera embedding y busca similares
    query = "¿Qué es la inteligencia artificial?"
    query_emb = emb_gen.generate([query])
    resultados = faiss_mgr.search(query_emb, k=2)

    console = Console()
    console.print(Panel.fit(f"[bold cyan]Consulta:[/bold cyan] {query}", title="🔎 Consulta FAISS"))
    table = Table(title="Resultados más similares", show_lines=True)
    table.add_column("Texto", style="magenta")
    table.add_column("Distancia", style="green")
    for texto, distancia in resultados:
        table.add_row(texto, f"{distancia:.4f}")
    console.print(table)

if __name__ == "__main__":
    main()