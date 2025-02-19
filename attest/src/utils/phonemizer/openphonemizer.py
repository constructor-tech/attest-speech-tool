# ATTEST: an Analytics Tool for the Testing and Evaluation of Speech Technologies
#
# Copyright (C) 2024 Constructor Technology AG
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see: <http://www.gnu.org/licenses/>.
#

from typing import List
from openphonemizer import OpenPhonemizer as BaseOpenPhonemizer

from attest.src.settings import get_settings
from attest.src.model import Project
from attest.src.utils.caching_utils import CacheHandler
from attest.src.utils.caching_validators import validate_matching_to_project_size
from attest.src.utils.performance_tracker import PerformanceTracker
from .phonemizer import Phonemizer


_phonemizer = None


def get_openphonemizer():
    global _phonemizer
    if _phonemizer is None:
        _phonemizer = OpenPhonemizer()

    return _phonemizer


settings = get_settings()


class OpenPhonemizer(Phonemizer):

    def __init__(self):
        self.model = None

    def load_model(self):
        if self.model is None:
            tracker = PerformanceTracker(name="Loading openphonemizer model", start=True)
            self.model = BaseOpenPhonemizer()
            tracker.end()

    @CacheHandler(
        cache_path_template=f"{settings.CACHE_DIR}/${{1.name}}/g2p/openphonemizer/phonemes.txt",
        method="txt",
        validator=validate_matching_to_project_size,
    )
    def phonemize_project(self, project: Project):
        self.load_model()

        tracker = PerformanceTracker(name="Phonemizing texts using openphonemizer", start=True)
        phonemes = [self.model(text) for text in project.texts]
        tracker.end()

        return phonemes

    @CacheHandler(
        cache_path_template=f"{settings.CACHE_DIR}/${{2}}",
        method="txt",
        validator=validate_matching_to_project_size,
    )
    def phonemize_many(self, texts: List[str], cache_path: str):
        self.load_model()

        tracker = PerformanceTracker(name="Phonemizing texts using openphonemizer", start=True)
        phonemes = [self.model(text) for text in texts]
        tracker.end()

        return phonemes
