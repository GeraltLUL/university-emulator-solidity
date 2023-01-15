import web3
import json
import hashlib


class University:
    admin = None
    contract_address = None
    ganache_address = '127.0.0.1'
    ganache_port = '7545'
    ganache_url = f'HTTP://{ganache_address}:{ganache_port}'
    w3 = web3.Web3(web3.HTTPProvider(ganache_url))
    contract = None

    def __init__(self, contract_address):
        self.contract_address = contract_address
        with open("abi.json", "r") as file:
            abi = json.load(file)
            self.contract = self.w3.eth.contract(address=contract_address, abi=abi)
        self.admin = web3.Web3.toChecksumAddress(self.get_admin_address())

    # def get_admin_addresses(self):
    #    return self.contract.functions.getAdminAddress(0).call()

    def get_admin_address(self):
        return self.contract.functions.getAdminAddress().call()

    def get_accounts(self):
        return self.w3.eth.accounts

    def add_student(self, addr, name, id, group, password):
        if web3.Web3.isChecksumAddress(addr):
            print('addr is ok')
            addr = web3.Web3.toChecksumAddress(addr)
            id = int(id) + 1

            salt = '123qwe'
            password = password + salt
            hashed = hashlib.md5(password.encode()).hexdigest()
            print(password, hashed)
            print(id)
            if addr in self.get_accounts():
                print("kavo")
                tx = self.contract.functions.addStudent(addr, name, id, group, hashed).transact(
                    {'from': self.admin})
                self.w3.eth.waitForTransactionReceipt(tx)
                print("SUCCESS")
                return True
        print("WRONGGG")
        return False

    def add_professor(self, addr, name, id, password):
        if web3.Web3.isChecksumAddress(addr):
            id = int(id) + 1
            addr = web3.Web3.toChecksumAddress(addr)

            salt = '123qwe'
            password = password + salt
            hashed = hashlib.md5(password.encode()).hexdigest()

            if addr in self.get_accounts():
                tx = self.contract.functions.addProfessor(addr, name, id, hashed).transact(
                    {'from': self.admin})
                self.w3.eth.waitForTransactionReceipt(tx)
                return True

        return False

    # def add_admin(self, addr):
    #     if web3.Web3.isChecksumAddress(addr):
    #         addr = web3.Web3.toChecksumAddress(addr)
    #         if addr in self.get_accounts():
    #             tx = self.contract.functions.addAdmin(addr).transact(
    #                 {'from': self.admin})
    #             self.w3.eth.waitForTransactionReceipt(tx)
    #             return True
    #
    #     return False

    def try_login(self, addr, password):
        if web3.Web3.isChecksumAddress(addr):
            addr = web3.Web3.toChecksumAddress(addr)
            salt = '123qwe'
            password = password + salt
            hashed = hashlib.md5(password.encode()).hexdigest()
            system_password = self.get_hashed_password(addr)
            print(hashed)
            print(system_password)

            if addr in self.get_accounts() and hashed == system_password:
                return True

        return False

    def add_exam(self, grade, addr, name):
        if web3.Web3.isChecksumAddress(addr):
            grade = int(grade)
            addr = web3.Web3.toChecksumAddress(addr)
            if addr in self.get_accounts():
                tx = self.contract.functions.addExam(grade, addr, name).transact(
                    {'from': self.admin})
                self.w3.eth.waitForTransactionReceipt(tx)
                return True

        return False

    def get_students_count(self):
        return self.contract.functions.getStudentsCount().call()

    def get_professors_count(self):
        return self.contract.functions.getProfessorsCount().call()

    def get_hashed_password(self, addr):
        if web3.Web3.isChecksumAddress(addr):
            return self.contract.functions.getHashedPassword(addr).call()

    def is_user_admin(self, addr):
        if web3.Web3.isChecksumAddress(addr) and addr in self.get_accounts():
            addr = web3.Web3.toChecksumAddress(addr)

            return self.contract.functions.isUserAdmin().call({'from': addr})

        return False

    def is_user_student(self, addr):
        if web3.Web3.isChecksumAddress(addr) and addr in self.get_accounts():
            addr = web3.Web3.toChecksumAddress(addr)

            return self.contract.functions.isUserStudent(addr).call()

        return False

    def get_exams(self):
        return self.contract.functions.getExams().call()

