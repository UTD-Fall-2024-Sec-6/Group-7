import unittest
from datetime import datetime

class TestStudyGroupMatrix(unittest.TestCase):
    def setUp(self):
        """Setup shared resources for the test cases."""
        self.dbmngr = DatabaseManager()
        self.controller = StudyGroupController(self.dbmngr)
        self.gui = StudyGroupGUI(self.controller)

        # Sample valid user
        self.valid_user = User("validUser", "validPassword", "validUser@example.com")
        self.dbmngr.saveUser(self.valid_user)

    def test_case_1(self):
        """Valid inputs for study group creation."""
        group = self.gui.createStudyGroup(
            groupName="ValidGroup",
            course="CS3377",
            location="ECSW",
            date=datetime.now(),
            maxSize=5,
            creator=self.valid_user,
        )
        self.assertIsNotNone(group)
        self.assertEqual(group.groupName, "ValidGroup")

    def test_case_2(self):
        """Invalid username."""
        invalid_user = User("", "validPassword", "validUser@example.com")
        self.dbmngr.saveUser(invalid_user)
        group = self.gui.createStudyGroup(
            groupName="ValidGroup",
            course="CS3377",
            location="ECSW",
            date=datetime.now(),
            maxSize=5,
            creator=invalid_user,
        )
        self.assertIsNone(group)

    def test_case_3(self):
        """Invalid password."""
        invalid_user = User("validUser", "", "validUser@example.com")
        self.dbmngr.saveUser(invalid_user)
        group = self.gui.createStudyGroup(
            groupName="ValidGroup",
            course="CS3377",
            location="ECSW",
            date=datetime.now(),
            maxSize=5,
            creator=invalid_user,
        )
        self.assertIsNone(group)

    def test_case_4(self):
        """Invalid email."""
        invalid_user = User("validUser", "validPassword", "")
        self.dbmngr.saveUser(invalid_user)
        group = self.gui.createStudyGroup(
            groupName="ValidGroup",
            course="CS3377",
            location="ECSW",
            date=datetime.now(),
            maxSize=5,
            creator=invalid_user,
        )
        self.assertIsNone(group)

    def test_case_5(self):
        """Invalid group name."""
        group = self.gui.createStudyGroup(
            groupName="",
            course="CS3377",
            location="ECSW",
            date=datetime.now(),
            maxSize=5,
            creator=self.valid_user,
        )
        self.assertIsNone(group)

    def test_case_6(self):
        """Invalid course."""
        group = self.gui.createStudyGroup(
            groupName="ValidGroup",
            course="INVALID_COURSE",
            location="ECSW",
            date=datetime.now(),
            maxSize=5,
            creator=self.valid_user,
        )
        self.assertIsNone(group)

    def test_case_7(self):
        """Invalid location."""
        group = self.gui.createStudyGroup(
            groupName="ValidGroup",
            course="CS3377",
            location="INVALID_LOCATION",
            date=datetime.now(),
            maxSize=5,
            creator=self.valid_user,
        )
        self.assertIsNone(group)

    def test_case_8(self):
        """Invalid date."""
        group = self.gui.createStudyGroup(
            groupName="ValidGroup",
            course="CS3377",
            location="ECSW",
            date=None,  # Invalid date
            maxSize=5,
            creator=self.valid_user,
        )
        self.assertIsNone(group)

    def test_case_9(self):
        """Invalid date."""
        group = self.gui.createStudyGroup(
            groupName="ValidGroup",
            course="CS3377",
            location="ECSW",
            date=None,  # Invalid date
            maxSize=5,
            creator=self.valid_user,
        )
        self.assertIsNone(group)

    def test_case_10(self):
        """Exceptional username."""
        exceptional_user = User(None, "validPassword", "validUser@example.com")
        self.dbmngr.saveUser(exceptional_user)
        group = self.gui.createStudyGroup(
            groupName="ValidGroup",
            course="CS3377",
            location="ECSW",
            date=datetime.now(),
            maxSize=5,
            creator=exceptional_user,
        )
        self.assertIsNone(group)

    def test_case_11(self):
        """Exceptional password."""
        exceptional_user = User("validUser", None, "validUser@example.com")
        self.dbmngr.saveUser(exceptional_user)
        group = self.gui.createStudyGroup(
            groupName="ValidGroup",
            course="CS3377",
            location="ECSW",
            date=datetime.now(),
            maxSize=5,
            creator=exceptional_user,
        )
        self.assertIsNone(group)

    def test_case_12(self):
        """Exceptional email."""
        exceptional_user = User("validUser", "validPassword", None)
        self.dbmngr.saveUser(exceptional_user)
        group = self.gui.createStudyGroup(
            groupName="ValidGroup",
            course="CS3377",
            location="ECSW",
            date=datetime.now(),
            maxSize=5,
            creator=exceptional_user,
        )
        self.assertIsNone(group)

    def test_case_13(self):
        """Exceptional group name."""
        group = self.gui.createStudyGroup(
            groupName=None,  # Exceptional value
            course="CS3377",
            location="ECSW",
            date=datetime.now(),
            maxSize=5,
            creator=self.valid_user,
        )
        self.assertIsNone(group)

    def test_case_14(self):
        """Exceptional course."""
        group = self.gui.createStudyGroup(
            groupName="ValidGroup",
            course=None,  # Exceptional value
            location="ECSW",
            date=datetime.now(),
            maxSize=5,
            creator=self.valid_user,
        )
        self.assertIsNone(group)

    def test_case_15(self):
        """Exceptional group size."""
        group = self.gui.createStudyGroup(
            groupName="ValidGroup",
            course="CS3377",
            location="ECSW",
            date=datetime.now(),
            maxSize=-1,  # Exceptional value
            creator=self.valid_user,
        )
        self.assertIsNone(group)

    def test_case_16(self):
        """Exceptional location."""
        group = self.gui.createStudyGroup(
            groupName="ValidGroup",
            course="CS3377",
            location=None,  # Exceptional value
            date=datetime.now(),
            maxSize=5,
            creator=self.valid_user,
        )
        self.assertIsNone(group)

    def test_case_17(self):
        """Exceptional date."""
        group = self.gui.createStudyGroup(
            groupName="ValidGroup",
            course="CS3377",
            location="ECSW",
            date="Invalid Date Format",  # Exceptional value
            maxSize=5,
            creator=self.valid_user,
        )
        self.assertIsNone(group)


if __name__ == "__main__":
    unittest.main()
