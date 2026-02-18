"""
Интерфейс командной строки (CLI) для Bonk.

Предоставляет удобный способ использования конвертера из терминала.
"""

import click
from pathlib import Path
from .converter import AudioToMidiConverter


@click.group()
def cli():
    """Bonk - преобразование аудиофайлов в MIDI (нотную запись)."""
    pass


@cli.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
@click.option(
    "--sr",
    default=22050,
    type=int,
    help="Частота дискретизации в Гц (по умолчанию 22050)",
)
@click.option(
    "--hop-length",
    default=512,
    type=int,
    help="Количество отсчётов между кадрами (по умолчанию 512)",
)
@click.option(
    "--min-duration",
    default=0.1,
    type=float,
    help="Минимальная длительность ноты в секундах (по умолчанию 0.1)",
)
@click.option(
    "--tempo", default=120, type=int, help="Темп в BPM (по умолчанию 120)"
)
@click.option(
    "--format",
    default="midi",
    type=click.Choice(["midi", "musicxml", "pdf"], case_sensitive=False),
    help="Формат выходного файла (по умолчанию midi)",
)
@click.option(
    "--quiet",
    is_flag=True,
    help="Не выводить информацию о процессе",
)
def convert(
    input_path: str,
    output_path: str,
    sr: int,
    hop_length: int,
    min_duration: float,
    tempo: int,
    format: str,
    quiet: bool,
):
    """
    Преобразовать аудиофайл в MIDI, MusicXML или PDF.

    Поддерживаемые форматы ввода: MP3, WAV, OGG, FLAC и др.
    
    Поддерживаемые форматы вывода:
    - midi: MIDI файл (можно открыть в DAW)
    - musicxml: Нотная партитура (MuseScore, Finale, Sibelius)
    - pdf: PDF документ с нотной партитурой

    Примеры:
        bonk convert song.mp3 output.mid
        bonk convert audio.wav music.musicxml
        bonk convert song.mp3 score.pdf --tempo 140
    """
    try:
        converter = AudioToMidiConverter(sr=sr, hop_length=hop_length)
        converter.convert(
            input_path,
            output_path,
            min_duration=min_duration,
            tempo=tempo,
            format=format,
            verbose=not quiet,
        )
    except Exception as e:
        click.echo(f"❌ Ошибка: {e}", err=True)
        raise click.Exit(1)


@cli.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.option(
    "--sr",
    default=22050,
    type=int,
    help="Частота дискретизации в Гц",
)
def info(input_path: str, sr: int):
    """Получить информацию об аудиофайле."""
    try:
        from .audio_processor import AudioProcessor

        processor = AudioProcessor(sr=sr)
        y, sr_loaded = processor.load_audio(input_path)

        click.echo(f"📂 Файл: {input_path}")
        click.echo(f"⏱️  Длительность: {len(y) / sr_loaded:.2f} сек")
        click.echo(f"🔊 Частота дискретизации: {sr_loaded} Гц")
        click.echo(f"📊 Количество отсчётов: {len(y)}")

    except Exception as e:
        click.echo(f"❌ Ошибка: {e}", err=True)
        raise click.Exit(1)


if __name__ == "__main__":
    cli()
