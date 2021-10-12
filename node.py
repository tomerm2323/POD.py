import copy
import pymongo

class Node:

    def __init__(self, name, pods_on, db, apps, ratio, request,limit):
        self.name = name
        self.__pods_on = pods_on
        self.__db = db
        self.__apps = apps
        self.ratio = ratio
        self.request = request
        self.limit = limit
        self.weekly_mem_pred = 0
        self.weekly_cpu_pred = 0
        self.cur_mem_usage = 0
        self.cur_cpu_usage = 0
        self.cpu_to_use = 0
        self.mem_to_use = 0


    def add_pod_on(self,pod):
        self.__pods_on.append(pod)

    def remove_pod_on(self,pod):
        self.__pods_on.remove(pod)

    def get_db(self):
        return copy.deepcopy([record for record in self.__db.find({'name' : self.name})][0])

    def get_pods_on(self):
        return copy.deepcopy(self.__pods_on)

    def get_cpu(self,timestamp = 0):
        if timestamp == 0:
            return self.cur_cpu_usage  ##latest
        for record in self.__db.find({'name' : self.name}):
            try:
                index = list(record.values())[1].index(str(timestamp))
            except Exception as e:
                print('A prediction is needed for your timeStamp ')
            else:
                return list(record.values())[2][list(record.values())[1].index(str(timestamp))]

    def get_mem(self,timestamp = 0):
        if timestamp == 0:
            return self.cur_mem_usage  ##latest
        for record in self.__db.find({'name' : self.name}):
            try:
                index = list(record.values())[1].index(str(timestamp))
            except Exception as e:
                print('A prediction is needed for your timeStamp ')
            else:
                return list(record.values())[3][list(record.values())[1].index(str(timestamp))]

    def update_db(self, timestamp, cpu_val, mem_val):
        self.cur_cpu_usage = cpu_val
        self.cur_mem_usage = mem_val
        self.__db.update_one({'name' : self.name},{'$push' : {'time' : timestamp, 'cpu' : cpu_val, 'mem' : mem_val}})

    def change_ratio(self,mem, cpu):
        self.ratio[0] = mem
        self.ratio[1] = cpu

    def set_limit(self,lim):
        self.limit =lim

    def set_request(self,rec):
        self.request = rec

    def get_limit(self):
        return self.limit

    def get_request(self):
        return self.request

    def get_ratio(self):
        return self.ratio

    def get_apps(self):
        return self.__apps

    def add_apps(self,apps = []):
        self.__apps.append(apps)

    def remove_apps(self,apps =[]):
        for app in apps: self.__apps.remove(app)

    def add_pods(self, pods = []):
        self.__pods_on.append(pods)

    def remove_pods(self, pods = []):
        for pod in pods: self.__pods_on.remove(pod)





