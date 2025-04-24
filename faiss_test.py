# Integración básica de EmbeddingsGenerator y FAISSManager

from src.embeddings.embeddings_generator import EmbeddingsGenerator
from src.faiss.faiss_manager import FAISSManager

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown

# 1. Inicializa el generador y el manager
emb_gen = EmbeddingsGenerator()
faiss_mgr = FAISSManager(dimension=emb_gen.get_dimension())

# 2. Prepara textos y genera embeddings
texts = [
    "La inteligencia artificial es fascinante.",
    "La carpintería requiere precisión.",
    "Los modelos de lenguaje procesan texto."
]
embeddings = emb_gen.generate(texts)  # shape: (3, 384)

# 3. Añade los embeddings al índice FAISS
faiss_mgr.add_embeddings(embeddings, texts)

# 4. Consulta: genera embedding y busca similares
query = "¿Qué es la inteligencia artificial?"
query_emb = emb_gen.generate([query])
resultados = faiss_mgr.search(query_emb, k=2)

console = Console()

# Mostrar la consulta
console.print(Panel.fit(f"[bold cyan]Consulta:[/bold cyan] {query}", title="🔎 Consulta FAISS"))

# Mostrar resultados en tabla
table = Table(title="Resultados más similares", show_lines=True)
table.add_column("Texto", style="magenta")
table.add_column("Distancia", style="green")

for texto, distancia in resultados:
    table.add_row(texto, f"{distancia:.4f}")

console.print(table)