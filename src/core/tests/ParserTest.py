import unittest

from src.settings import OSU_FOLDER
from src.core.osu_worker.osu_db import find_local_beatmap_files_by_md5


class ParserTest(unittest.TestCase):
    def test_find_local_beatmap_files_by_md5(self):
        md5 = "06b536749d5a59536983854be90504ee"
        beatmap_file_paths_dict = find_local_beatmap_files_by_md5(OSU_FOLDER, [md5])
        self.assertTrue("1011011 nekodex - new beginnings" in beatmap_file_paths_dict[md5])
