#!/usr/bin/env python
import os
import sys
from importlib import import_module

if __name__ == "__main__":
    import_module('btcimg.settings')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "btcimg.settings.dev")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
