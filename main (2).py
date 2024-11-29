from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass
from uuid import uuid4
@dataclass
class User:
    def __init__(self, name, password, email, study_group=None):
        if not name or not isinstance(name, str) or not name.strip():
            raise ValueError("Invalid username: Username cannot be empty or None.")

        if not password or not isinstance(password, str) or not password.strip():
            raise ValueError("Invalid password: Password cannot be empty or None.")

        if not email or not isinstance(email, str) or not email.strip():
            raise ValueError("Invalid email: Email cannot be empty or None.")

        self.userID = str(uuid4())
        self.userName = name
        self.password = password
        self.email = email
        self.groups = study_group if study_group is not None else []

    def addToStudyGroup(self, studyGroup: "StudyGroup") -> bool:
        if studyGroup not in self.groups:
            self.groups.append(studyGroup)
            return True
        return False

    def removeStudyGroup(self, studyGroup: "StudyGroup") -> bool:
        memberIndex = next((i for i, group in enumerate(self.groups) if group.groupID == studyGroup.groupID), None)
    #    if memberIndex is not None:
     #       self.groups.pop(memberIndex)
      #      return True
      #  return False
        if studyGroup in self.groups:
            self.groups.pop(memberIndex)
            return True
        return False

class StudyGroup:
    def __init__(self, groupName: Optional[str], course: Optional[str], location: Optional[str], date: Optional[datetime], maxSize: int):
        dbManager = DatabaseManager()

        # Validate group name
        if not groupName or not groupName.strip():
            print("Error: Group name cannot be empty.")
            self.is_valid = False
            return

        if any(group.groupName == groupName for group in dbManager.studyGroups):
            print(f"Error: Group name '{groupName}' already exists.")
            self.is_valid = False
            return

        # Validate course
        if not course or not course.strip():
            print("Error: Course name cannot be empty.")
            self.is_valid = False
            return

        if course.strip() not in dbManager.getValidCourses():
            print(f"Error: Invalid course: {course}. Valid courses are {', '.join(dbManager.getValidCourses())}.")
            self.is_valid = False
            return

        # Validate location
        if not location or not location.strip():
            print("Error: Location cannot be empty.")
            self.is_valid = False
            return

        if location.strip() not in dbManager.getValidLocations():
            print(f"Error: Invalid location: {location}. Valid locations are {', '.join(dbManager.getValidLocations())}.")
            self.is_valid = False
            return

        # Validate date
        if not isinstance(date, datetime):
            print("Error: Invalid date. Date must be a datetime object.")
            self.is_valid = False
            return

        # Validate max size
        if maxSize <= 0:
            print("Error: Invalid max size. The size of the group must be greater than 0.")
            self.is_valid = False
            return

        # All validations passed
        self.is_valid = True
        self.groupName = groupName
        self.groupID = str(uuid4())
        self.course = course
        self.location = location
        self.date = date
        self.maxSize = maxSize
        self.members: List[User] = []

    def addMember(self, user: User) -> bool:
        if not self.is_valid:
            print(f"Error: Cannot add member to invalid group {self.groupName}.")
            return False

        if any(member.userID == user.userID for member in self.members):
            print(f"{user.userName} is already a member of the group {self.groupName}.")
            return False

        if len(self.members) >= self.maxSize:
            print(f"{self.groupName} is full. Cannot add {user.userName}.")
            return False

        self.members.append(user)
        user.addToStudyGroup(self)
        return True

    def removeMember(self, user: User) -> bool:
        if not self.is_valid:
            print(f"Error: Cannot remove member from an invalid group {self.groupName}.")
            return False

        memberIndex = next((i for i, member in enumerate(self.members) if member.userID == user.userID), None)

        if memberIndex is None:
            print(f"{user.userName} is not a member of the group {self.groupName}.")
            return False

        if len(self.members) == 1:
            print(f"{self.groupName} will be empty. Cannot remove {user.userName}.")
            return False

        print(f"Removing {user.userName} with ID {user.userID} from {self.groupName}.")
        removed_user = self.members.pop(memberIndex)
        print(f"Removed user: {removed_user.userName}.")

        user.removeStudyGroup(self)

        return True

class Message:
    def __init__(self, sender, recipient, content, group=None):
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.timestamp = datetime.now()
        self.group = group  # Optional - For group messages

    def __str__(self):
        if self.group:
            return f"[{self.timestamp}] {self.sender} -> Group '{self.group}': {self.content}"
        return f"[{self.timestamp}] {self.sender} -> {self.recipient}: {self.content}"


class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.users: List[User] = []
            self.studyGroups: List[StudyGroup] = []
            self.userCredentials = {}
            self.validCourses = [
                "ECS1100", "CS1200", "CS2305", "CS2336", "CS2340", "CS3162", "CS3341", "CS3354", "CS3377", "ECS2390",
                "CS4141", "CS4337", "CS4341", "CS4347", "CS4348", "CS4349", "CS4384", "CS4485", "CS4365", "CS4375"
            ]
            self.validLocations = ["SCI", "SLC", "JO", "GR", "Library", "FO", "ECSW", "ECSS", "ECSN", "JSOM"]
            self.messages: List[Message] = []

    def getValidCourses(self) -> List[str]:
        return self.validCourses

    def getValidLocations(self) -> List[str]:
        return self.validLocations

    def saveUser(self, user: User) -> bool:
        if user not in self.users:
            self.users.append(user)
            self.userCredentials[user.userName] = {
                "password": user.password,
                "email": user.email,
            }
            return True
        return False

    def saveStudyGroup(self, studyGroup: StudyGroup) -> bool:
        if studyGroup not in self.studyGroups:
            self.studyGroups.append(studyGroup)
            return True
        return False

    def getStudyGroup(self, groupID: str) -> Optional[StudyGroup]:
        return next((group for group in self.studyGroups if group.groupID == groupID), None)

    def saveMessage(self, sender: User, message: Message) -> bool:
        if not sender or not message:
            print("Sender and message must be valid.")
            return False
        try:
            self.messages.append(message)
            print("Message saved.")
            return True
        except Exception as e:
            print(f"Error saving message: {e}")
            return False

    def getMessagesForUser(self, user: User) -> List[Message]:
        user_messages = [msg for msg in self.messages if msg.recipient == user.userName]
        group_messages = [
            msg for msg in self.messages
            if msg.group and any(group.groupName == msg.group for group in user.groups)
        ]
        return user_messages + group_messages


class StudyGroupController:
    def __init__(self, dbManager: DatabaseManager):
        self.dbManager = dbManager

    def createStudyGroup(self, groupName: str, course: str, location: str, date: datetime, maxSize: int, creator: User) -> Optional[StudyGroup]:
        studyGroup = StudyGroup(groupName, course, location, date, maxSize)
        if studyGroup.is_valid:
            studyGroup.addMember(creator)
            self.dbManager.saveStudyGroup(studyGroup)
            print(f"Study group '{groupName}' created successfully.")
            return studyGroup
        else:
            print(f"Failed to create study group '{groupName}'.")
            return None

    def joinStudyGroup(self, groupID: str, user: User) -> bool:
        studyGroup = self.dbManager.getStudyGroup(groupID)
        if studyGroup and studyGroup.is_valid:
            return studyGroup.addMember(user)
        else:
            print(f"Study group {groupID} not found or invalid.")
            return False

    def removeFromStudyGroup(self, groupID: str, user: User) -> bool:
        studyGroup = self.dbManager.getStudyGroup(groupID)
        if studyGroup and studyGroup.is_valid:
            return studyGroup.removeMember(user)
        else:
            print(f"Study group {groupID} not found or invalid.")
            return False


class MessageController:
    def __init__(self, dbManager: DatabaseManager):
        self.dbManager = dbManager

    def sendMessage(self, sender: User, recipient: User, content: str) -> bool:
        if not sender or not recipient or not content.strip():
            print("Error: Sender, recipient, and message content must be valid.")
            return False
        message = Message(sender.userName, recipient.userName, content)
        return self.dbManager.saveMessage(sender, message)

    def getMessage(self, recipient: User) -> List[Message]:
        return self.dbManager.getMessagesForUser(recipient)
    # return [message for message in self.dbManager.messages if message.recipient == recipient.userName]

    def sendGroupMessage(self, sender: User, group: StudyGroup, content: str) -> bool:
        if sender not in group.members:
            print("Error: Sender must be a member of the group.")
            return False
        if not content.strip():
            print("Message content must be valid")
            return False
        group_message = Message(sender.userName, None, content, group=group.groupName)
        if self.dbManager.saveMessage(sender, group_message):
            print(f"Group message sent to '{group.groupName}' by {sender.userName}.")
            return True
        else:
            print("Error: Failed to save group message.")
            return False


class StudyGroupGUI:
    def __init__(self, controller: StudyGroupController, messageController: MessageController):
        self.controller = controller
        self.messageController = messageController

    def createStudyGroup(self, groupName: str, course: str, location: str, date: datetime, maxSize: int, creator: User) -> Optional[StudyGroup]:
        return self.controller.createStudyGroup(groupName, course, location, date, maxSize, creator)

    def joinStudyGroup(self, groupID: str, user: User) -> bool:
        return self.controller.joinStudyGroup(groupID, user)

    def sendDirectMessage(self, sender: User, recipient: User, content: str) -> bool:
        return self.messageController.sendMessage(sender, recipient, content)

    def sendGroupMessage(self, sender: User, group: StudyGroup, content: str) -> bool:
        return self.messageController.sendGroupMessage(sender, group, content)

    def getMessage(self, recipient: User) -> List[Message]:
        return self.messageController.getMessage(recipient)

    def removeFromStudyGroup(self, groupID: str, user: User) -> bool:
        return self.controller.removeFromStudyGroup(groupID, user)


def main():

    print("\n \n now in main")
    user1 = User("testUser1", "testPassword1", "testUser1@exampleEmail.com")
    user2 = User("testUser2", "testPassword2", "testUser2@exampleEmail.com")
    user3 = User("testUser3", "testPassword3", "testUser3@exampleEmail.com")
    user4 = User("testUser4", "testPassword4", "testUser4@exampleEmail.com")
    user5 = User("testUser5", "testPassword5", "testUser5@exampleEmail.com")


    dbmngr = DatabaseManager()
    dbmngr.saveUser(user1)
    dbmngr.saveUser(user2)
    dbmngr.saveUser(user3)
    dbmngr.saveUser(user4)
    dbmngr.saveUser(user5)

    controller = StudyGroupController(dbmngr)
    messageController= MessageController(dbmngr)
    gui = StudyGroupGUI(controller, messageController)

    groupName = "groupName1"
    course = "CS3377"
    location = "ECSW"
    date = datetime.now()
    maxSize = 10
    creator = user1

    testGroup = gui.createStudyGroup(
        groupName, course, location, date, maxSize, creator
    )
    testGroup2 = gui.createStudyGroup(
        "groupName2", "CS4337", "ECSS", datetime.now(), 10, user2
    )
    testGroup3 = gui.createStudyGroup(
        "groupName3", "", "ECSS", datetime.now(), 10, user2
    )
    testGroup4 = gui.createStudyGroup(
        "groupName4", "CS4337", " ", datetime.now(), 10, user2
    )
    testGroup5 = gui.createStudyGroup(
        "groupName5", "CS4337", "ECSS", datetime.now(), 0, user2
    )
    gui.joinStudyGroup(testGroup.groupID, user2)
    gui.joinStudyGroup(testGroup.groupID, user4)
    gui.joinStudyGroup(testGroup.groupID, user5)
    gui.joinStudyGroup(testGroup2.groupID, user3)
    gui.joinStudyGroup(testGroup2.groupID, user5)
    gui.joinStudyGroup(testGroup2.groupID, user4)

    print(f"User 5 groups: {[group.groupName for group in user5.groups]}")


    print("Members of the study group:")
    for member in testGroup.members:
        print(member.userName)
    print("---------")
    print("Members of the second study group:")
    for member in testGroup2.members:
        print(member.userName)

    gui.sendDirectMessage(user1, user2, "hi")
    gui.sendDirectMessage(user1, user2, "hi again")
    messagesForUser2 = gui.getMessage(user2)
    print("\nMessages for User2:")
    for msg in messagesForUser2:
        print(msg)
    print("End of messages for User2")

    gui.sendGroupMessage(user3, testGroup2, "hi group")
    gui.sendGroupMessage(user2, testGroup, "hi gang")
    messagesForUser5 = gui.getMessage(user5)
    print("\nMessages for User5:")
    for msg in messagesForUser5:
        print(msg)

    print("\n")
    gui.removeFromStudyGroup(testGroup2.groupID, user5)

    print("\nAll messages in the database:")
    for msg in dbmngr.messages:
        print(msg)

if __name__ == "__main__":
    main()

