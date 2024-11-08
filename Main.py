from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass
from uuid import uuid4

@dataclass
class User:
    def __init__(self, name, password, email, study_group=None):
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


class StudyGroup:
    def __init__(self, groupName: str, course: str, location: str, date: datetime, maxSize: int):
        dbManager = DatabaseManager()

        if not groupName.strip():
            print("Error: Group name cannot be empty.")
            self.is_valid = False
            return

        if any(group.groupName == groupName for group in dbManager.studyGroups):
            print(f"Error: Group name '{groupName}' already exists.")
            self.is_valid = False
            return

        if not course.strip():
            print("Error: Course name cannot be empty.")
            self.is_valid = False
            return

        if course.strip() not in dbManager.getValidCourses():
            print(f"Error: Invalid course: {course}. Valid courses are {', '.join(dbManager.getValidCourses())}.")
            self.is_valid = False
            return

        if not location.strip():
            print("Error: Location cannot be empty.")
            self.is_valid = False
            return

        if location.strip() not in dbManager.getValidLocations():
            print(f"Error: Invalid location: {location}. Valid locations are {', '.join(dbManager.getValidLocations())}.")
            self.is_valid = False
            return

        if maxSize <= 0:
            print("Error: Invalid max size. The size of the group must be greater than 0.")
            self.is_valid = False
            return

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
            self.validCourses = ["ECS1100","CS1200","CS2305","CS2336","CS2340","CS3162","CS3341","CS3354","CS3377","ECS2390","CS4141","CS4337","CS4341","CS4347","CS4348","CS4349","CS4384","CS4485","CS4365","CS4375",]
            self.validLocations = ["SCI","SLC","JO","GR","Library","FO","ECSW","ECSS","ECSN","JSOM",]

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


class StudyGroupController:
    def __init__(self, dbManager: DatabaseManager):
        self.dbManager = dbManager

    def createStudyGroup(
        self, groupName: str, course: str, location: str, date: datetime, maxSize: int, creator: User, ) -> Optional[StudyGroup]:
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


class StudyGroupGUI:
    def __init__(self, controller: StudyGroupController):
        self.controller = controller

    def createStudyGroup(self, groupName: str, course: str, location: str, date: datetime, maxSize: int, creator: User,) -> Optional[StudyGroup]:
        studyGroup = self.controller.createStudyGroup(
            groupName, course, location, date, maxSize, creator
        )
        return studyGroup

    def joinStudyGroup(self, groupID: str, user: User) -> bool:
        return self.controller.joinStudyGroup(groupID, user)


def main():
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
    gui = StudyGroupGUI(controller)

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

    print("Members of the study group:")
    for member in testGroup.members:
        print(member.userName)
    print("---------")
    print("Members of the second study group:")
    for member in testGroup2.members:
        print(member.userName)


if __name__ == "__main__":
    main()
