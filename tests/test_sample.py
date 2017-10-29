# -*- coding: utf-8 -*-

# This file is a part of software developed by Unirobot Inc.
# Copyright 2017 Unirobot Inc. All Rights Reserved.
# The source code in this file is the property of Unirobot Inc.,
# and may not be copied, distributed, modified or sold except under a
# licence expressly granted by Unirobot Inc. to do so.
# ==============================================================================
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re
import unittest

from model.models import Preference


class TestSample(unittest.TestCase):

    def test_prere(self):
        obj = Preference("a", "b")
        self.assertEqual(obj.preferenceType, "a")
        word = "abc  de   aa  "
        result = word.replace("  ", "■")
        self.assertEqual(result, "abc■de■ aa■")
        result = re.sub(" +", "■", word)
        self.assertEqual(result, "abc■de■aa■")

