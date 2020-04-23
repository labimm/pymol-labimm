import subprocess
import sys

import pymol.gui

from .ftmap.core import init_plugin_cli as ftmap_init_plugin_cli
from .ftmap.gui import init_plugin_gui as ftmap_init_plugin_gui
from .prefs import guess_prefs
from .vina import init_plugin as vina_init_plugin


def pip(args):
    process = subprocess.Popen(
        [sys.executable, "-m", "pip", "--disable-pip-version-check"] + args,
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = process.communicate()
    return process, out, err


def init_plugin():
    guess_prefs()

    # FTMap
    ftmap_init_plugin_cli()

    window = pymol.gui.get_qtwindow()
    menu_bar = window.menuBar()
    labimm_menu = menu_bar.addMenu("LaBiMM")

    ftmap_init_plugin_gui(labimm_menu)

    # Vina
    vina_init_plugin(labimm_menu)

    update_action = labimm_menu.addAction("Update...")

    @update_action.triggered.connect
    def triggered():
        proc, out, err = pip(["install", "--upgrade", "pymol-labimm"])
        if out:
            print(out)
        if err:
            print(err)
