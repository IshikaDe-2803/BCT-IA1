pragma solidity ^0.5.0;

pragma experimental ABIEncoderV2;

contract Notes {

    uint public noteCount = 0;
    uint public userCount = 0;

    struct User {
        uint id;
        string username;
        string password;
    }

    struct Note {
        uint id;
        string title;
        string content;
        uint256 timestamp;
        bool publicNote;
        User user;
    }

    User[] public allUsers;
    Note[] public allnotes;
    mapping(uint => Note) public listNotes;

    event NoteCreated(
        uint id,
        string title,
        string content,
        uint256 timestamp,
        bool publicNote,
        User user
    );

    event NoteDeleted(uint id);
    event UserCreated(uint id, string username);

    mapping(string => uint) private emailToUserId;

    function createUser(string memory _username, string memory _password) public {
        userCount++;
        User memory newUser = User(userCount, _username, _password);
        allUsers.push(newUser);
        emailToUserId[_username] = userCount; // Store the mapping
        emit UserCreated(userCount, _username);
    }

    function getUserIdByEmail(string memory _email) public view returns (uint) {
        return emailToUserId[_email];
    }


    function createNote(
        string memory _title,
        string memory _content,
        bool _publicNote,
        uint _userId
    ) public {
        noteCount++;
        User memory noteUser = allUsers[_userId - 1];
        Note memory newNote = Note(
            noteCount,
            _title,
            _content,
            now,
            _publicNote,
            noteUser
        );
        listNotes[noteCount] = newNote;
        allnotes.push(newNote);
        emit NoteCreated(
            noteCount,
            _title,
            _content,
            now,
            _publicNote,
            noteUser
        );
    }

    

    function deleteNote(uint256 id) public {
        for (uint256 i = id - 1; i < noteCount - 1; i++) {
            allnotes[i] = allnotes[i + 1];
            listNotes[i] = allnotes[i + 1];
        }
        allnotes.pop();
        delete listNotes[noteCount - 1];
        noteCount--;
        emit NoteDeleted(id);
    }

    function getUserNotes(uint _userId) external view returns (Note[] memory) {
    uint256 userNoteCount = 0;

    for (uint256 i = 0; i < allnotes.length; i++) {
        if (allnotes[i].user.id == _userId) {
            userNoteCount++;
        }
    }

    Note[] memory notes = new Note[](userNoteCount);
    uint256 index = 0;

    for (uint256 i = 0; i < allnotes.length; i++) {
        if (allnotes[i].user.id == _userId) {
            notes[index] = allnotes[i];
            index++;
        }
    }

    return notes;
}

    function getAllUsers() external view returns (User[] memory) {
        return allUsers;
    }

    function getAllNotes() external view returns (Note[] memory) {
        return allnotes;
    }

    function getNotes(uint id) external view returns (Note memory) {
        return listNotes[id];
    }

    function getUsers(uint _userId) external view returns (uint, string memory, string memory) {
        require(_userId > 0 && _userId <= userCount, "Invalid user ID");
        User memory user = allUsers[_userId - 1];
        return (user.id, user.username, user.password);
    }

    function getPublicNotes() external view returns (Note[] memory) {
        uint256 publicCount = 0;

        for (uint256 i = 0; i < allnotes.length; i++) {
            if (allnotes[i].publicNote == true) {
                publicCount++;
            }
        }

        Note[] memory publicNotes = new Note[](publicCount);
        uint256 index = 0;

        for (uint256 i = 0; i < allnotes.length; i++) {
            if (allnotes[i].publicNote == true) {
                publicNotes[index] = allnotes[i];
                index++;
            }
        }

        return publicNotes;
    }
}