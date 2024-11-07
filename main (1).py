from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass 
from uuid import uuid4


@dataclass
class User:
    def __init__(self, name, password, email, study_group=None):
        self.userName = name
        self.password = password
        self.email = email
        self.groups = study_group if study_group is not None else []
    
    def addToStudyGroup(self, studyGroup: 'StudyGroup') -> bool:
        self.groups.append(studyGroup)
        return True

    
class StudyGroup:
    def __init__ (self, groupName: str, course: str, location: str, date:datetime, maxSize: int ):
        self.groupName = groupName
        self.groupID = str(uuid4())
        self.course = course
        self.location = location
        self.date = date
        self.maxSize = maxSize
        self.members: List[User] = []
        
    def addMember (self, user: User) -> bool:
        if len(self.members) < self.maxSize and user not in self.members:
            self.members.append(user)
            user.addToStudyGroup(self)
            return True
        return False
        
    
class DatabaseManager:
    def __init__(self):
        self.users: List[User] = []
        self.studyGroups: List[StudyGroup] = []
        self.userCredentials = {}
        
    def saveUser(self, user: User) -> bool:
        if user not in self.users:
            self.users.append(user)
            self.userCredentials[user.userName] = user.password
            return True
        return False
        
    def saveStudyGroup(self, studyGroup: StudyGroup) -> bool:
        if studyGroup not in self.studyGroups:
            self.studyGroups.append(studyGroup)
            return True
        return False
        
    def getStudyGroup (self, groupID: str) ->Optional [StudyGroup]:
        return next ((group for group in self.studyGroups if group.groupID == groupID), None)
        
    def authenticateUser(self, userName: str, password: str) -> bool:
        """Authenticating user... checking username and password..."""
        return self.userCredentials.get(userName) == password
    
class StudyGroupController:
    def __init__ (self, dbManager: DatabaseManager):
        self.dbManager = dbManager
        
    def createStudyGroup (self, groupName: str, course: str, location:str, date: datetime,
                        maxSize: int, creator: User) ->Optional[StudyGroup]:
        if maxSize <=0:
            print ("Invalid group size")
            return None
            
        studyGroup = StudyGroup(groupName, course, location, date, maxSize)
        studyGroup.addMember(creator)
        
        if self.dbManager.saveStudyGroup(studyGroup):
            return studyGroup
        return None
        
        
    def joinStudyGroup(self, groupID: str, user: User) -> bool:
        studyGroup = self.dbManager.getStudyGroup(groupID)
        if studyGroup:
            return studyGroup.addMember(user)
        return False
        
        
class StudyGroupGUI:
    def __init__(self, controller: StudyGroupController):
        self.controller = controller
        
    def createStudyGroup(self, groupName:str, course:str, location: str, date: datetime, 
                    maxSize:int, creator:User) -> bool:
                        
        studyGroup = self.controller.createStudyGroup (groupName, course, location, date, maxSize, creator)
        return studyGroup is not None
        
    def joinStudyGroup (self, groupID: str, user: User) ->bool:
        return self.controller.joinStudyGroup(groupID, user)
        
        
class main:
    user1 = User(name="testUser1",password="testPassword1",email="testUser1@exampleEmail.com");
    user2 = User(name="testUser2",password="testPassword2",email="testUser2@exampleEmail.com");

    testGroup = StudyGroup("test study group", "test 101", "Room 5", datetime.now(), 10)
    testGroup.addMember(user1)

    dbmngr = DatabaseManager()
    
    dbmngr.saveUser(user1)
    dbmngr.saveUser(user2)
    
    print(dbmngr.authenticateUser("testUser1", "testPassword1"))
    print(dbmngr.authenticateUser("testUser1", "wrongPassword"))
    

    print(testGroup.members[0].userName)
    print(user1.groups[0].groupName)
    