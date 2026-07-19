"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import sys
from pathlib import Path

# Put both the project root and this src/ directory on sys.path so the import
# below works whether launched as `python -m src.main`, as a plain script, or
# from any working directory — and regardless of whether the module is
# addressed as `src.recommender` or `recommender`.
SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent
for _path in (PROJECT_ROOT, SRC_DIR):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from src.recommender import load_songs, recommend_songs, score_song

WIDTH = 62
TITLE_WIDTH = 40


def _format_profile(user_prefs: dict) -> str:
    """Render the user's preferences as a compact one-line summary."""
    parts = []
    for key, value in user_prefs.items():
        if isinstance(value, (list, tuple)):
            value = ", ".join(map(str, value))
        parts.append(f"{key}={value}")
    return " · ".join(parts)


def _score_bar(score: float, width: int = 10) -> str:
    """A small proportional bar, e.g. ███████░░░ for a score of ~0.7."""
    filled = round(max(0.0, min(1.0, score)) * width)
    return "█" * filled + "░" * (width - filled)


def _truncate(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 1] + "…"


def render_recommendations(recommendations, user_prefs) -> str:
    """Build a clean, ranked terminal layout: title, score, and reasons."""
    lines = [
        "=" * WIDTH,
        "  🎵  Top Music Recommendations",
        f"  for  {_format_profile(user_prefs)}",
        "=" * WIDTH,
    ]

    if not recommendations:
        lines += ["", "  No matching songs found.", ""]
        return "\n".join(lines)

    for rank, (song, score, _explanation) in enumerate(recommendations, start=1):
        # Pull the structured reasons straight from the scorer.
        _score, reasons = score_song(user_prefs, song)

        name = _truncate(f"{song['title']} — {song['artist']}", TITLE_WIDTH)
        lines.append("")
        lines.append(f"  {rank}. {name:<{TITLE_WIDTH}}  {_score_bar(score)} {score:.2f}")

        for i, reason in enumerate(reasons):
            connector = "└─" if i == len(reasons) - 1 else "├─"
            lines.append(f"        {connector} {reason}")

    lines.append("")
    lines.append("=" * WIDTH)
    return "\n".join(lines)


def main() -> None:
    # Resolve the data file relative to the project root, not the current
    # working directory, so the runner works from anywhere.
    songs = load_songs(str(PROJECT_ROOT / "data" / "songs.csv"))

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)
    print(render_recommendations(recommendations, user_prefs))


if __name__ == "__main__":
    main()
