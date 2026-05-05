import sys

def setup_encoding():
    """Ensure standard output and error use UTF-8 encoding."""
    # Use reconfigure if available (Python 3.7+)
    if hasattr(sys.stdout, 'reconfigure'):
        if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
            sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, 'reconfigure'):
        if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
            sys.stderr.reconfigure(encoding="utf-8")
