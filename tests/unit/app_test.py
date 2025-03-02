import logging

# import sys
from pathlib import Path

import ipywidgets

# import pytest
import reacton.core

# import solara.server.app
from solara.server import reload
from solara.server.app import AppScript

logger = logging.getLogger("solara.server.app_test")


HERE = Path(__file__).parent
reload.reloader.start()


def test_notebook_element(app_context, no_app_context):
    name = str(HERE / "solara_test_apps" / "notebookapp_element.ipynb")
    app = AppScript(name)
    try:
        with app_context:
            el = app.run()
            assert isinstance(el, reacton.core.Element)
            el2 = app.run()
            assert el is el2
    finally:
        app.close()


def test_notebook_component(app_context, no_app_context):
    name = str(HERE / "solara_test_apps" / "notebookapp_component.ipynb")
    app = AppScript(name)
    try:
        with app_context:
            el = app.run().kwargs["children"][0].component
            assert isinstance(el, reacton.core.Component)
            el2 = app.run().kwargs["children"][0].component
            assert el is el2
    finally:
        app.close()


def test_notebook_widget(app_context, no_app_context):
    name = str(HERE / "solara_test_apps" / "notebookapp_widget.ipynb")
    app = AppScript(name)
    try:
        with app_context:
            widget = app.run()
            assert isinstance(widget, ipywidgets.Button)
            widget2 = app.run()
        assert widget is not widget2
    finally:
        app.close()


# these make other test fail on CI (vaex is used, which causes a blake3 reload, which fails)
# def test_watch_module_reload(tmpdir, app_context, extra_include_path, no_app_context):
#     import ipyvuetify as v

#     with extra_include_path(str(tmpdir)):
#         py_file = tmpdir / "test.py"
#         py_mod_file = tmpdir / "somemod.py"

#         logger.info("writing files")
#         with open(py_mod_file, "w") as f:
#             f.write("import ipyvuetify as v; App = v.Btn.element\n")
#         with open(py_file, "w") as f:
#             f.write("import somemod; app=somemod.App\n")

#         logger.info("wrote files")

#         app = AppScript(f"{py_file}")
#         try:
#             result = app.run()
#             assert "somemod" in sys.modules
#             assert "somemod" in reload.reloader.watched_modules
#             somemod1 = sys.modules["somemod"]
#             assert result().component.widget == v.Btn

#             # change depending module
#             with open(py_mod_file, "w") as f:
#                 f.write("import ipyvuetify as v; App = v.Card.element\n")
#             # wait for the event to trigger
#             reload.reloader.reload_event_next.wait()
#             # assert "somemod" not in sys.modules
#             # breakpoint()
#             result = app.run()
#             assert "somemod" in sys.modules
#             assert result().component.widget == v.Card
#             somemod2 = sys.modules["somemod"]
#             assert somemod1 is not somemod2
#         finally:
#             app.close()
#             if "somemod" in sys.modules:
#                 del sys.modules["somemod"]
#             reload.reloader.watched_modules.remove("somemod")


# def test_script_reload_component(tmpdir, app_context, extra_include_path, no_app_context):
#     import ipyvuetify as v

#     with extra_include_path(str(tmpdir)):
#         py_file = tmpdir / "test.py"

#         logger.info("writing files")
#         with open(py_file, "w") as f:
#             f.write("import reacton.ipyvuetify as v; Page = v.Btn\n")

#         app = AppScript(f"{py_file}")
#         try:
#             result = app.run()
#             assert result().component.widget == v.Btn
#             with open(py_file, "w") as f:
#                 f.write("import reacton.ipyvuetify as v; Page = v.Slider\n")
#             # wait for the event to trigger
#             reload.reloader.reload_event_next.wait()
#             # assert "somemod" not in sys.modules
#             # breakpoint()
#             result = app.run()
#             assert result().component.widget == v.Slider
#         finally:
#             app.close()


# def test_watch_module_import_error(tmpdir, app_context, extra_include_path, no_app_context):
#     import ipyvuetify as v

#     with extra_include_path(str(tmpdir)):
#         py_file = tmpdir / "test.py"
#         py_mod_file = tmpdir / "somemod2.py"

#         logger.info("writing files")
#         with open(py_mod_file, "w") as f:
#             f.write("import ipyvuetify as v; App = v.Btn.element\n")
#         with open(py_file, "w") as f:
#             f.write("import somemod2; app=somemod2.App\n")

#         logger.info("wrote files")

#         app = AppScript(f"{py_file}")
#         try:
#             result = app.run()
#             assert "somemod2" in sys.modules
#             assert "somemod2" in reload.reloader.watched_modules
#             assert result().component.widget == v.Btn

#             # syntax error
#             with open(py_mod_file, "w") as f:
#                 f.write("import ipyvuetify as v; App !%#$@= v.Card.element\n")
#             reload.reloader.reload_event_next.wait()
#             with pytest.raises(SyntaxError):
#                 result = app.run()

#             with open(py_mod_file, "w") as f:
#                 f.write("import ipyvuetify as v; App = v.Card.element\n")
#             reload.reloader.reload_event_next.wait()
#             result = app.run()
#             assert "somemod2" in sys.modules
#             assert result().component.widget == v.Card
#         finally:
#             app.close()
#             del sys.modules["somemod2"]
#             reload.reloader.watched_modules.remove("somemod2")
