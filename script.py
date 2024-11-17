import requests
from googlesearch import search
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
import time

def main():
    console = Console()

    # Pedir dominio o palabra clave a buscar
    termino = input("Introduce un dominio o palabra clave para buscar (por ejemplo, telcel.com o Telcel): ").strip()

    # Validación de entrada
    if not termino:
        console.print("[red]El término no puede estar vacío. Inténtalo de nuevo.[/red]")
        return

    # Configuración de búsqueda
    limite_busqueda = 300
    resultados_unicos = set()
    resultados_filtrados = []

    console.print("[blue]Iniciando búsqueda en Google...[/blue]")

    # Barra de carga para la búsqueda
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Buscando en Google...", total=limite_busqueda)

        # Realizar búsqueda en Google
        for url in search(termino, num_results=limite_busqueda):
            # Agregar solo URLs únicas
            base_url = url.split('/')[2]
            if base_url not in resultados_unicos:
                resultados_unicos.add(base_url)
                resultados_filtrados.append(url)

            # Actualizar la barra de progreso
            progress.update(task, advance=1)

    # Pausa para cambiar a datos móviles
    console.print("\n[blue]Búsqueda completada. Ahora desconecta el Wi-Fi y activa los datos móviles.[/blue]")
    console.print("[yellow]Presiona Enter cuando hayas cambiado la conexión a datos móviles para continuar...[/yellow]")
    input()  # Esperar a que el usuario haga el cambio de red

    console.print("[blue]Solicitando respuestas HTTP...[/blue]")

    # Animación de carga para solicitudes HTTP
    resultados_respuestas = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Solicitando respuestas...", total=len(resultados_filtrados))

        for url in resultados_filtrados:
            try:
                respuesta = requests.get(url, timeout=5)
                resultados_respuestas.append((url, respuesta.status_code))
            except Exception as e:
                resultados_respuestas.append((url, f"Error: {e}"))

            # Actualizar la barra de progreso
            progress.update(task, advance=1)

    # Mostrar resultados finales
    console.print("\n[green]Resultados obtenidos:[/green]")
    for url, status in resultados_respuestas:
        console.print(f"{url} -> [cyan]{status}[/cyan]")

    console.print("\n[green]¡Búsqueda completada![/green]")

if _name_ == "_main_":
    main()