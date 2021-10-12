import copy
import pymongo

class Pod:

    def __init__(self, name, cluster, db, node, app):
        self.name = name
        self.__cluster = cluster
        self.__db = db
        self.__node = node
        self.__app = app
        self.weekly_mem_pred = 0
        self.weekly_cpu_pred = 0
        self.cur_mem_usage = 0
        self.cur_cpu_usage = 0


    def add_to_clustr(self,other):
        self.cluster.append(other)

    def remove_from_cluster(self,other):
        self.cluster.remove(other)

    def get_db(self):
        return copy.deepcopy([record for record in self.__db.find({'name' : self.name})][0])

    def get_node(self):
        return copy.deepcopy(self.__node)

    def update_node(self,node_obj):
        self.__node = node_obj

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



