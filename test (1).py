import unittest
from datetime import datetime
from main import User, DatabaseManager, StudyGroupController, StudyGroupGUI, MessageController

class TestStudyGroupMatrix(unittest.TestCase):
    def setUp(self):
        """Setup shared resources for the test cases."""
        # Create a fresh DatabaseManager instance for each test.
        self.dbmngr = DatabaseManager()
        # Reset DatabaseManager attributes
        self.dbmngr.users = []
        self.dbmngr.studyGroups = []

        self.controller = StudyGroupController(self.dbmngr)
        self.messageController = MessageController(self.dbmngr)
        self.gui = StudyGroupGUI(self.controller, self.messageController)

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

    def test_case_18(self):
        # valid remove user
        group = self.gui.createStudyGroup(
            groupName = "ValidGroup18",
            course = "CS3377",
            location = "ECSW",
            date = datetime.now(),
            maxSize = 6,
            creator = self.valid_user,
        )
        self.assertIsNotNone(group)
        new_user1 = User("newUser1", "newPassword1", "newUser1@example.com")
        self.dbmngr.saveUser(new_user1)
        joined = self.gui.joinStudyGroup(groupID=group.groupID, user=new_user1)
        self.assertTrue(joined)
        self.assertIn(new_user1, group.members)
        print(f"Members before removal: {[member.userName for member in group.members]}")
        print(f"Users study groups before removal:{[group.groupName for group in new_user1.groups]}")
        leave = self.gui.removeFromStudyGroup(groupID = group.groupID, user = new_user1)
        self.assertTrue(leave)
        print(f"Users study groups after removal:{[group.groupName for group in new_user1.groups]}")
        print(f"Members after removal: {[member.userName for member in group.members]}")
        self.assertTrue(all(member.userID != new_user1.userID for member in group.members))



    def test_case_19(self):
        # remove user that is not part of the group
        group = self.gui.createStudyGroup(
                groupName = "ValidGroup19",
            course = "CS2336",
            location = "SCI",
            date = datetime.now(),
            maxSize = 4,
            creator = self.valid_user,
        )
        self.assertIsNotNone(group)
        new_user2 = User("newUser2", "newPassword2", "newUser2@example.com")
        self.dbmngr.saveUser(new_user2)
        leave = self.gui.removeFromStudyGroup(groupID = group.groupID, user = new_user2)
        self.assertFalse(leave)

    def test_case_20(self):
        # removing user = empty group -- dont let them leave
        group = self.gui.createStudyGroup(
            groupName = "ValidGroup20",
            course = "CS2336",
            location = "SCI",
            date = datetime.now(),
            maxSize = 4,
            creator = self.valid_user,
        )
        self.assertIsNotNone(group)
        leave = self.gui.removeFromStudyGroup(groupID = group.groupID, user = self.valid_user)
        self.assertFalse(leave)
        self.assertGreater(len(group.members), 0)
        self.assertIn(self.valid_user, group.members)

    def test_case_21(self):
    # remove invalid user
        group = self.gui.createStudyGroup(
            groupName = "ValidGroup21",
            course = "CS2336",
            location = "SCI",
            date = datetime.now(),
            maxSize = 4,
            creator = self.valid_user,
        )
        self.assertIsNotNone(group)
        with self.assertRaises(ValueError):
            new_user3 = User("", "newPassword3", "newUser3@example.com")
            self.dbmngr.saveUser(new_user3)
            leave = self.gui.removeFromStudyGroup(groupID = group.groupID, user = new_user3)
            self.assertFalse(leave)

    def test_case_22(self):
    # valid message between user and user
        new_user4 = User("newUser4", "newPassword4", "newUser4@example.com")
        self.dbmngr.saveUser(new_user4)
        new_user5 = User("newUser5", "newPassword5", "newUser5@example.com")
        self.dbmngr.saveUser(new_user5)
        send = self.gui.sendDirectMessage(new_user4, new_user5 , "hi newUser5")
        self.assertTrue(send)
        receive = self.gui.getMessage(new_user5)
        self.assertIsNotNone(receive)

    def test_case_23(self):
    # invalid sender
        new_user7 = User("newUser7", "newPassword7", "newUser7@example.com")
        self.dbmngr.saveUser(new_user7)
        with self.assertRaises(ValueError):
            new_user6 = User(" ", "newPassword6", "newUser6@example.com")
            self.dbmngr.saveUser(new_user6)
            send = self.gui.sendDirectMessage(new_user6, new_user7, "hi newUser7")
            self.assertFalse(send)
            receive = self.gui.getMessage(new_user7)
            self.assertIsNone(receive)

    def test_case_24(self):
    # invalid message
        new_user8 = User("newUser8", "newPassword8", "newUser8@example.com")
        self.dbmngr.saveUser(new_user8)
        new_user9 = User("newUser9", "newPassword9", "newUser9@example.com")
        self.dbmngr.saveUser(new_user9)
        send = self.gui.sendDirectMessage(new_user8, new_user9, " ")
        self.assertFalse(send)
        receive = self.gui.getMessage(new_user9)
        self.assertEqual(len(receive), 0, "Expected no messages to be received by new_user9")

    def test_case_25(self):
    # invalid recipient
        new_user10 = User("newUser10", "newPassword10", "newUser10@example.com")
        self.dbmngr.saveUser(new_user10)
        with self.assertRaises(ValueError):
            new_user11 = User(" ", "newPassword11", "newUser11@example.com")
            self.dbmngr.saveUser(new_user11)
            send = self.gui.sendDirectMessage(new_user10, new_user11, "hi newUser11")
            self.assertFalse(send)
            receive = self.gui.getMessage(new_user11)
            self.assertIsNone(receive)

    def test_case_26(self):
    # valid group messaging
        group = self.gui.createStudyGroup(
            groupName = "ValidGroup26",
            course = "CS3377",
            location = "SCI",
            date = datetime.now(),
            maxSize = 4,
            creator = self.valid_user,
        )
        new_user12 = User("newUser12", "newPassword12", "newUser12@example.com")
        self.dbmngr.saveUser(new_user12)
        new_user13 = User("newUser13", "newPassword13", "newUser13@example.com")
        self.dbmngr.saveUser(new_user13)
        joined = self.gui.joinStudyGroup(groupID=group.groupID, user=new_user12)
        self.assertTrue(joined)
        joined2 = self.gui.joinStudyGroup(groupID=group.groupID, user=new_user13)
        self.assertTrue(joined2)
        send = self.gui.sendGroupMessage(self.valid_user, group, "hi buds")
        self.assertTrue(send)
        receive = self.gui.getMessage(new_user12)
        self.assertIsNotNone(receive)
        receive2 = self.gui.getMessage(new_user13)
        self.assertIsNotNone(receive2)

    def test_case_27(self):
    # invalid group messaging : member not part of group
        group = self.gui.createStudyGroup(
            groupName = "ValidGroup27",
            course = "CS4347",
            location = "Library",
            date = datetime.now(),
            maxSize = 4,
            creator = self.valid_user,
        )
        new_user12 = User("newUser12", "newPassword12", "newUser12@example.com")
        self.dbmngr.saveUser(new_user12)
        new_user13 = User("newUser13", "newPassword13", "newUser13@example.com")
        self.dbmngr.saveUser(new_user13)
        joined = self.gui.joinStudyGroup(groupID=group.groupID, user=new_user12)
        self.assertTrue(joined)
        joined2 = self.gui.joinStudyGroup(groupID=group.groupID, user=new_user13)
        self.assertTrue(joined2)
        send = self.gui.sendGroupMessage(self.valid_user, group, "hi buds")
        self.assertTrue(send)
        receive = self.gui.getMessage(new_user12)
        self.assertIsNotNone(receive)
        receive2 = self.gui.getMessage(new_user13)
        self.assertIsNotNone(receive2)

    def test_case_28(self):
        # invalid group messaging -- invalid message
        group = self.gui.createStudyGroup(
            groupName = "ValidGroup28",
            course = "CS3354",
            location = "Library",
            date = datetime.now(),
            maxSize = 4,
            creator = self.valid_user,
        )
        new_user14 = User("newUser14", "newPassword14", "newUser14@example.com")
        self.dbmngr.saveUser(new_user14)
        new_user15 = User("newUser15", "newPassword15", "newUser15@example.com")
        self.dbmngr.saveUser(new_user15)
        joined = self.gui.joinStudyGroup(groupID=group.groupID, user=new_user14)
        self.assertTrue(joined)
        joined2 = self.gui.joinStudyGroup(groupID=group.groupID, user=new_user15)
        self.assertTrue(joined2)
        send = self.gui.sendGroupMessage(new_user14, group, " ")
        self.assertFalse(send)
        receive = self.gui.getMessage(new_user15)
        self.assertEqual(len(receive), 0, "Expected no messages to be received by new_user15")

    def test_case_29(self):
        # invalid group testing: invalid recipient
        group = self.gui.createStudyGroup(
            groupName = "ValidGroup29",
            course = "CS3354",
            location = "Library",
            date = datetime.now(),
            maxSize = 4,
            creator = self.valid_user,
        )
        new_user16 = User("newUser16", "newPassword16", "newUser16@example.com")
        self.dbmngr.saveUser(new_user16)
        with self.assertRaises(ValueError):
            new_user17 = User(" ", "newPassword17", "newUser17@example.com")
            self.dbmngr.saveUser(new_user17)
            joined = self.gui.joinStudyGroup(groupID=group.groupID, user=new_user16)
            self.assertTrue(joined)
            joined2 = self.gui.joinStudyGroup(groupID=group.groupID, user=new_user17)
            self.assertTrue(joined2)
            send = self.gui.sendGroupMessage(new_user16, group, "hello group")
            self.assertFalse(send)
            receive = self.gui.getMessage(new_user17)
            self.assertEqual(len(receive), 0, "Expected no messages to be received by new_user17")

    def test_case_30(self):
        # invalid group testing: invalid sender
        group = self.gui.createStudyGroup(
            groupName = "ValidGroup30",
            course = "CS3377",
            location = "Library",
            date = datetime.now(),
            maxSize = 4,
            creator = self.valid_user,
        )
        new_user19 = User("newUser19", "newPassword19", "newUser19@example.com")
        self.dbmngr.saveUser(new_user19)
        with self.assertRaises(ValueError):
            new_user18 = User(" ", "newPassword18", "newUser17@example.com")
            self.dbmngr.saveUser(new_user18)
            joined = self.gui.joinStudyGroup(groupID=group.groupID, user=new_user18)
            self.assertTrue(joined)
            joined2 = self.gui.joinStudyGroup(groupID=group.groupID, user=new_user19)
            self.assertTrue(joined2)
            send = self.gui.sendGroupMessage(new_user18, group, "hello group")
            self.assertFalse(send)
            receive = self.gui.getMessage(new_user19)
            self.assertEqual(len(receive), 0, "Expected no messages to be received by new_user19")


if __name__ == "__main__":
    unittest.main()