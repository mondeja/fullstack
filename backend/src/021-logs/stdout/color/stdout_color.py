#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

import colorama
colorama.init(autoreset=True)

DEFAULT_FORMAT = "%(asctime)s %(levelname)-8s %(name)s:%(lineno)d: %(message)s"
DEFAULT_FORMATTER = logging.Formatter(DEFAULT_FORMAT)

class ColorizingStreamHandler(logging.StreamHandler):
    """Colorear las salidas del logging por consola"""
    color_map = {           # Mapa de colores personalizable:
        logging.DEBUG: colorama.Style.DIM + colorama.Fore.CYAN,
        logging.WARNING: colorama.Back.YELLOW + colorama.Fore.RED,
        logging.ERROR: colorama.Fore.YELLOW + colorama.Back.RED,
        logging.CRITICAL: colorama.Back.RED + colorama.Fore.WHITE +  colorama.Style.BRIGHT,
    }

    def __init__(self, stream=sys.stdout, color_map=None):
        logging.StreamHandler.__init__(self,
                                       colorama.AnsiToWin32(stream).stream)
        if color_map:
            self.color_map = color_map

    @property
    def is_tty(self):
        isatty = getattr(self.stream, 'isatty', None)
        return isatty and isatty()

    def format(self, record):
        message = logging.StreamHandler.format(self, record)
        if self.is_tty:
            # Don't colorize a traceback
            parts = message.split('\n', 1)
            parts[0] = self.colorize(parts[0], record)
            message = '\n'.join(parts)
        return message

    def colorize(self, message, record):
        try:
            return (self.color_map[record.levelno] + message)
        except KeyError:
            return message


def createLogger(name, level=logging.INFO, handler=ColorizingStreamHandler(),
                 propagate=True):
    """Devuelve un logger con nombre, nivel y manejador provistos."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler.setFormatter(DEFAULT_FORMATTER)
    logger.addHandler(handler)
    logger.propagate = propagate
    return logger
