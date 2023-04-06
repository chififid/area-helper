import unittest

from src.core.settings import core_settings
from src.core.tests.helpers import init_osu_db
from src.core.osu_worker.osu_db import find_local_beatmap_files_by_md5


class ParserTest(unittest.TestCase):
    def test_find_local_beatmap_files_by_md5(self):
        init_osu_db()

        md5 = "06b536749d5a59536983854be90504ee"
        beatmap_file_paths_dict = find_local_beatmap_files_by_md5(core_settings.OSU_FOLDER, [md5])
        self.assertTrue("1011011 nekodex - new beginnings" in beatmap_file_paths_dict[md5])
