# -*- coding: utf-8 -*-
"""
integration tests for shadow linux
"""

from __future__ import absolute_import, print_function, unicode_literals

import os
import random
import string

import pytest
import salt.modules.linux_shadow
import salt.utils.files
import salt.utils.platform
from salt.ext.six.moves import range
from tests.support.case import ModuleCase
from tests.support.helpers import destructiveTest, flaky
from tests.support.unit import skipIf


@pytest.mark.skip_if_not_root
@skipIf(not salt.utils.platform.is_linux(), "These tests can only be run on linux")
class ShadowModuleTest(ModuleCase):
    """
    Validate the linux shadow system module
    """

    def setUp(self):
        """
        Get current settings
        """
        super(ShadowModuleTest, self).setUp()
        self._no_user = self.__random_string()
        self._password = salt.modules.linux_shadow.gen_password("Password1234")

    def __random_string(self, size=6):
        """
        Generates a random username
        """
        return "tu-" + "".join(
            random.choice(string.ascii_lowercase + string.digits) for x in range(size)
        )

    @destructiveTest
    def test_info(self):
        """
        Test shadow.info
        """
        self.addCleanup(self.run_function, "user.delete", [self._test_user])
        self.run_function("user.add", [self._test_user])

        # Correct Functionality
        ret = self.run_function("shadow.info", [self._test_user])
        self.assertEqual(ret["name"], self._test_user)

        # User does not exist
        ret = self.run_function("shadow.info", [self._no_user])
        self.assertEqual(ret["name"], "")

    @destructiveTest
    def test_del_password(self):
        """
        Test shadow.del_password
        """
        self.addCleanup(self.run_function, "user.delete", [self._test_user])
        self.run_function("user.add", [self._test_user])

        # Correct Functionality
        self.assertTrue(self.run_function("shadow.del_password", [self._test_user]))
        self.assertEqual(
            self.run_function("shadow.info", [self._test_user])["passwd"], ""
        )

        # User does not exist
        self.assertFalse(self.run_function("shadow.del_password", [self._no_user]))

    @destructiveTest
    def test_set_password(self):
        """
        Test shadow.set_password
        """
        self.addCleanup(self.run_function, "user.delete", [self._test_user])
        self.run_function("user.add", [self._test_user])

        # Correct Functionality
        self.assertTrue(
            self.run_function("shadow.set_password", [self._test_user, self._password])
        )

        # User does not exist
        self.assertFalse(
            self.run_function("shadow.set_password", [self._no_user, self._password])
        )

    @destructiveTest
    def test_set_inactdays(self):
        """
        Test shadow.set_inactdays
        """
        self.addCleanup(self.run_function, "user.delete", [self._test_user])
        self.run_function("user.add", [self._test_user])

        # Correct Functionality
        self.assertTrue(
            self.run_function("shadow.set_inactdays", [self._test_user, 12])
        )

        # User does not exist (set_inactdays return None is user does not exist)
        self.assertFalse(self.run_function("shadow.set_inactdays", [self._no_user, 12]))

    @destructiveTest
    def test_set_maxdays(self):
        """
        Test shadow.set_maxdays
        """
        self.addCleanup(self.run_function, "user.delete", [self._test_user])
        self.run_function("user.add", [self._test_user])

        # Correct Functionality
        self.assertTrue(self.run_function("shadow.set_maxdays", [self._test_user, 12]))

        # User does not exist (set_inactdays return None is user does not exist)
        self.assertFalse(self.run_function("shadow.set_maxdays", [self._no_user, 12]))

    @destructiveTest
    def test_set_mindays(self):
        """
        Test shadow.set_mindays
        """
        self.addCleanup(self.run_function, "user.delete", [self._test_user])
        self.run_function("user.add", [self._test_user])

        # Correct Functionality
        self.assertTrue(self.run_function("shadow.set_mindays", [self._test_user, 12]))

        # User does not exist (set_inactdays return None is user does not exist)
        self.assertFalse(self.run_function("shadow.set_mindays", [self._no_user, 12]))

    @flaky
    @destructiveTest
    def test_lock_password(self):
        """
        Test shadow.lock_password
        """
        self.addCleanup(self.run_function, "user.delete", [self._test_user])
        self.run_function("user.add", [self._test_user])
        self.run_function("shadow.set_password", [self._test_user, self._password])

        # Correct Functionality
        self.assertTrue(self.run_function("shadow.lock_password", [self._test_user]))

        # User does not exist (set_inactdays return None is user does not exist)
        self.assertFalse(self.run_function("shadow.lock_password", [self._no_user]))

    @destructiveTest
    def test_unlock_password(self):
        """
        Test shadow.lock_password
        """
        self.addCleanup(self.run_function, "user.delete", [self._test_user])
        self.run_function("user.add", [self._test_user])
        self.run_function("shadow.set_password", [self._test_user, self._password])

        # Correct Functionality
        self.assertTrue(self.run_function("shadow.unlock_password", [self._test_user]))

        # User does not exist (set_inactdays return None is user does not exist)
        self.assertFalse(self.run_function("shadow.unlock_password", [self._no_user]))

    @destructiveTest
    def test_set_warndays(self):
        """
        Test shadow.set_warndays
        """
        self.addCleanup(self.run_function, "user.delete", [self._test_user])
        self.run_function("user.add", [self._test_user])

        # Correct Functionality
        self.assertTrue(self.run_function("shadow.set_warndays", [self._test_user, 12]))

        # User does not exist (set_inactdays return None is user does not exist)
        self.assertFalse(self.run_function("shadow.set_warndays", [self._no_user, 12]))

    @destructiveTest
    def test_set_date(self):
        """
        Test shadow.set_date
        """
        self.addCleanup(self.run_function, "user.delete", [self._test_user])
        self.run_function("user.add", [self._test_user])

        # Correct Functionality
        self.assertTrue(
            self.run_function("shadow.set_date", [self._test_user, "2016-08-19"])
        )

        # User does not exist (set_inactdays return None is user does not exist)
        self.assertFalse(
            self.run_function("shadow.set_date", [self._no_user, "2016-08-19"])
        )

    @destructiveTest
    def test_set_expire(self):
        """
        Test shadow.set_exipre
        """
        self.addCleanup(self.run_function, "user.delete", [self._test_user])
        self.run_function("user.add", [self._test_user])

        # Correct Functionality
        self.assertTrue(
            self.run_function("shadow.set_expire", [self._test_user, "2016-08-25"])
        )

        # User does not exist (set_inactdays return None is user does not exist)
        self.assertFalse(
            self.run_function("shadow.set_expire", [self._no_user, "2016-08-25"])
        )

    @destructiveTest
    def test_set_del_root_password(self):
        """
        Test set/del password for root
        """
        # saving shadow file
        if not os.access("/etc/shadow", os.R_OK | os.W_OK):
            self.skipTest("Could not save initial state of /etc/shadow")

        def restore_shadow_file(contents):
            # restore shadow file
            with salt.utils.files.fopen("/etc/shadow", "w") as wfh:
                wfh.write(contents)

        with salt.utils.files.fopen("/etc/shadow", "r") as rfh:
            contents = rfh.read()
        self.addCleanup(restore_shadow_file, contents)

        # set root password
        self.assertTrue(
            self.run_function("shadow.set_password", ["root", self._password])
        )
        self.assertEqual(
            self.run_function("shadow.info", ["root"])["passwd"], self._password
        )
        # delete root password
        self.assertTrue(self.run_function("shadow.del_password", ["root"]))
        self.assertEqual(self.run_function("shadow.info", ["root"])["passwd"], "")
