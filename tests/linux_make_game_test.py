"""Game-free checks for the 1.1.1 native Linux build-kit path."""

import importlib.util
import os
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import make_game  # noqa: E402


class LinuxBuildKitTests(unittest.TestCase):
    @unittest.skipUnless(sys.platform.startswith("linux"), "Linux-specific build selection")
    def test_linux_runtime_matches_standard_builder(self):
        import build_game

        expected = {p.relative_to(ROOT / "runtime").as_posix() for p in build_game.runtime_sources()}
        selected = {p.relative_to(ROOT / "runtime").as_posix() for p, _ in make_game.runtime_sources()}
        self.assertEqual(expected, selected)
        self.assertIn("platform/linux.c", selected)
        self.assertIn("gfx_window_sdl.c", selected)
        self.assertIn("ui/menu_sdl.cpp", selected)
        self.assertNotIn("platform/win32.c", selected)
        self.assertNotIn("gfx_window_win.c", selected)

    @unittest.skipUnless(sys.platform.startswith("linux"), "Linux-specific build selection")
    def test_elf_output_and_libraries(self):
        self.assertEqual(make_game.EXE_NAME, "ocarina")
        self.assertEqual(make_game.XLATE_NAME, "nx2navi_xlate")
        self.assertIn("-lvulkan", make_game.LINK_LIBS)
        self.assertNotIn("-lvulkan-1", make_game.LINK_LIBS)

    @unittest.skipUnless(sys.platform.startswith("linux"), "Linux-specific build selection")
    def test_clang_from_path(self):
        clang, clangxx, env = make_game.compiler_tools(None)
        self.assertTrue(clang.is_file())
        self.assertTrue(clangxx.is_file())
        self.assertIn("PATH", env)


if __name__ == "__main__":
    unittest.main()
