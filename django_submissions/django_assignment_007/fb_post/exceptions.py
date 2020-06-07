class Error(Exception):
    pass

class InvalidUserException(Error):
    pass

class InvalidGroupNameException(Error):
    pass

class InvalidMemberException(Error):
    pass

class InvalidGroupException(Error):
    pass

class UserNotInGroupException(Error):
    pass

class UserIsNotAdminException(Error):
    pass

class MemberNotInGroupException(Error):
    pass

class InvalidPostContent(Error):
    pass