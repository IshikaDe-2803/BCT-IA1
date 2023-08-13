pragma solidity ^0.5.0;

pragma experimental ABIEncoderV2;

contract Notes {

  uint public noteCount = 0;

  struct Note {
    uint id;
    string title;
    string content;
    uint256 timestamp;
    bool publicNote;
  }

  Note[] public allnotes;
  mapping(uint => Note) public listNotes;

  constructor() public {
    createNote("Title", "Content", true);
  }

  event NoteCreated(
    uint id,
    string title,
    string content,
    uint256 timestamp,
    bool publicNote
  );

  event NoteDeleted(
    uint id
  );

  function createNote(string memory _title, string memory _content, bool _publicNote) public {
    noteCount ++;
    Note memory newNote = Note(noteCount, _title, _content, now, _publicNote);
    listNotes[noteCount] = newNote;
    allnotes.push(newNote);
    emit NoteCreated(noteCount, _title, _content, now, _publicNote);
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

  function getAllNotes() external view returns (Note[] memory) {
    return allnotes;
  }

  function getNotes(uint id) external view returns (Note memory) {
    return listNotes[id];
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
