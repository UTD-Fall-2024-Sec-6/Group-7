import unittest
from datetime import datetime
from Main import User, DatabaseManager, StudyGroupController, StudyGroupGUI

class TestStudyGroupMatrix(unittest.TestCase):
    def setUp(self):
        """Setup shared resources for the test cases."""
        # Create a fresh DatabaseManager instance for each test.
        self.dbmngr = DatabaseManager()
        # Reset DatabaseManager attributes
        self.dbmngr.users = []
        self.dbmngr.studyGroups = []

        self.controller = StudyGroupController(self.dbmngr)
        self.gui = StudyGroupGUI(self.controller)

        # Sample valid user
        self.valid_user = User("validUser", "validPassword", "validUser@example.com")
        self.dbmngr.saveUser(self.valid_user)

    def test_case_1(self):
        """Valid inputs for study group creation."""
        group = self.gui.createStudyGroup(
            groupName="ValidGroup1",  # Unique group name
            course="CS3377",
            location="ECSW",
            date=datetime.now(),
            maxSize=5,
            creator=self.valid_user,
        )
        self.assertIsNotNone(group)
        self.assertEqual(group.groupName, "ValidGroup1")

    def test_case_2(self):
        """Invalid username."""
        with self.assertRaises(ValueError):
            User("", "validPassword", "validUser@example.com")

    def test_case_3(self):
        """Invalid password."""
        with self.assertRaises(ValueError):
            User("validUser", "", "validUser@example.com")

    def test_case_4(self):
        """Invalid email."""
        with self.assertRaises(ValueError):
            User("validUser", "validPassword", "")

    def test_case_5(self):
        """Invalid group name."""
        group = self.gui.createStudyGroup(
            groupName="",  # Invalid group name
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
            groupName="ValidGroup6",  # Unique group name
            course="INVALID_COURSE",  # Invalid course
            location="ECSW",
            date=datetime.now(),
            maxSize=5,
            creator=self.valid_user,
        )
        self.assertIsNone(group)

    def test_case_7(self):
        """Invalid location."""
        group = self.gui.createStudyGroup(
            groupName="ValidGroup7",  # Unique group name
            course="CS3377",
            location="INVALID_LOCATION",  # Invalid location
            date=datetime.now(),
            maxSize=5,
            creator=self.valid_user,
        )
        self.assertIsNone(group)

    def test_case_8(self):
        """Invalid date - None provided."""
        group = self.gui.createStudyGroup(
            groupName="ValidGroup8",  # Unique group name
            course="CS3377",
            location="ECSW",
            date=None,  # Invalid date (None)
            maxSize=5,
            creator=self.valid_user,
        )
        self.assertIsNone(group)

    def test_case_9(self):
        """Exceptional username."""
        with self.assertRaises(ValueError):
            User(None, "validPassword", "validUser@example.com")

    def test_case_10(self):
        """Exceptional password."""
        with self.assertRaises(ValueError):
            User("validUser", None, "validUser@example.com")

    def test_case_11(self):
        """Exceptional email."""
        with self.assertRaises(ValueError):
            User("validUser", "validPassword", None)

    def test_case_12(self):
        """Exceptional group name - None provided."""
        group = self.gui.createStudyGroup(
            groupName=None,  # Invalid group name (None)
            course="CS3377",
            location="ECSW",
            date=datetime.now(),
            maxSize=5,
            creator=self.valid_user,
        )
        self.assertIsNone(group)

    def test_case_13(self):
        """Exceptional course - None provided."""
        group = self.gui.createStudyGroup(
            groupName="ValidGroup13",  # Unique group name
            course=None,  # Invalid course (None)
            location="ECSW",
            date=datetime.now(),
            maxSize=5,
            creator=self.valid_user,
        )
        self.assertIsNone(group)

    def test_case_14(self):
        """Exceptional date - Invalid format."""
        group = self.gui.createStudyGroup(
            groupName="ValidGroup14",  # Unique group name
            course="CS3377",
            location="ECSW",
            date="Invalid Date Format",  # Invalid date format (should be datetime)
            maxSize=5,
            creator=self.valid_user,
        )
        self.assertIsNone(group)

    def test_case_15(self):
        """Exceptional maxSize - negative value."""
        group = self.gui.createStudyGroup(
            groupName="ValidGroup15",  # Unique group name
            course="CS3377",
            location="ECSW",
            date=datetime.now(),
            maxSize=-1,  # Invalid max size
            creator=self.valid_user,
        )
        self.assertIsNone(group)

    def test_case_16(self):
        """Exceptional location - None provided."""
        group = self.gui.createStudyGroup(
            groupName="ValidGroup16",  # Unique group name
            course="CS3377",
            location=None,  # Invalid location (None)
            date=datetime.now(),
            maxSize=5,
            creator=self.valid_user,
        )
        self.assertIsNone(group)

    def test_case_17(self):
        """Valid group creation and join operation."""
        group = self.gui.createStudyGroup(
            groupName="ValidGroup17",
            course="CS3377",
            location="ECSW",
            date=datetime.now(),
            maxSize=5,
            creator=self.valid_user,
        )
        self.assertIsNotNone(group)
        # Adding a new user to a valid group
        new_user = User("newUser", "newPassword", "newUser@example.com")
        self.dbmngr.saveUser(new_user)
        joined = self.gui.joinStudyGroup(groupID=group.groupID, user=new_user)
        self.assertTrue(joined)
        self.assertIn(new_user, group.members)

if __name__ == "__main__":
    unittest.main()
