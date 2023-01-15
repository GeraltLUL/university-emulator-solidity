pragma solidity 0.8.0;

contract University {

    struct Student {
        address addr;
        string name;
        uint id;
        string group;
        string password;
    }

    struct Professor {
        address addr;
        string name;
        uint id;
        string password;
    }

    struct Exam {
        uint grade;
        address studentAddr;
        string examName;
    }

    address private admin;
    address[] public students_addrs;
    address[] public professors_addrs;
    mapping(address => Student) public students;
    mapping(address => Professor) public professors;
    Exam[] public exams;

    constructor() {
        admin = msg.sender;
    }

    modifier onlyAdmin {
        require(msg.sender == admin);
        _;
    }

    function addStudent(address _addr, string memory _name, uint _id, string memory _group, string memory _password) public onlyAdmin {
        require(_addr != address(0), "Wrong address");
        require(students[_addr].addr == address(0), "Stundent with such id is already exists");
        students[_addr] = Student(_addr, _name, _id, _group, _password);
        students_addrs.push(_addr);
    }

    function addProfessor(address _addr, string memory _name, uint _id, string memory _password) public onlyAdmin {
        require(_addr != address(0), "Wrong address");
        require(professors[_addr].addr == address(0), "Professor with such id is already exists");
        professors[_addr] = Professor(_addr, _name, _id, _password);
        professors_addrs.push(_addr);
    }

    function addExam(uint _grade, address _studentAddr, string memory _name) public onlyAdmin {
        require(students[_studentAddr].addr != address(0), "Such student id does not exists");
        exams.push(Exam(_grade, students[_studentAddr].addr, _name));
    }

    function getAdminAddress() public view returns(address) {
        return admin;
    }

    function getHashedPassword(address _addr) public view returns(string memory) {
        require(students[_addr].addr != address(0) || professors[_addr].addr != address(0), "Wrong address");
        if(students[_addr].addr != address(0)) {
            return students[_addr].password;
        }
        else {
            return professors[_addr].password;
        }
    }

    function getStudentsCount() public view returns(uint) {
        return students_addrs.length;
    }

    function getProfessorsCount() public view returns(uint) {
        return professors_addrs.length;
    }

    function getExams() public view returns(Exam[] memory) {
        return exams;
    }

    function isUserAdmin() public view returns(bool) {
        bool res = false;

        if (msg.sender == admin){
            res = true;
        }

        return res;
    }

    function isUserStudent(address _addr) public view returns(bool) {
        if (students[_addr].addr != address(0)) {
            return true;
        }
        else {
            return false;
        }
    }
}