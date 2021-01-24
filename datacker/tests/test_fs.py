import os
from pathlib import Path
import tempfile
import unittest

from ..fs import LocalFileSystem


class TestLocalFileSystem(unittest.TestCase):
    def setUp(self):
        self.fs = LocalFileSystem()

    def test_write(self):
        expected = "It works!"
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file = Path(tmp_dir) / "test_write.txt"
            self.fs.write(test_file, expected)
            self.assertTrue(os.path.exists(test_file))
            with open(test_file) as f:
                self.assertEqual(f.read(), expected)

    def test_copy(self):
        expected = "Content to copy"
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file = Path(tmp_dir) / "test_original.txt"
            with open(test_file, "w") as f:
                f.write(expected)
            copy_file = Path(tmp_dir) / "test_copy.txt"
            self.fs.copy(test_file, copy_file)
            self.assertTrue(os.path.exists(copy_file))
            with open(copy_file) as f:
                self.assertEqual(f.read(), expected)

    def test_delete(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_dir = Path(tmp_dir) / "test_dir"
            os.mkdir(test_dir)
            with open(test_dir / "test_file.txt", "w") as f:
                f.write("Content to delete")
            self.fs.delete(test_dir)
            self.assertFalse(os.path.exists(test_dir))

    def test_temporary_directory(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            new_tmp_dir = self.fs.create_temporary_directory(prefix=str(tmp_dir))
            self.assertTrue(os.path.exists(new_tmp_dir))
            self.assertTrue(str(new_tmp_dir).startswith(tmp_dir))
