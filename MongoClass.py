import pymongo
import pandas as pd
import copy
import numpy as np
import json
from Analytics import Analytics
import datetime
import time


class Mongoc:

    def __init__(self, db_name):
        client = pymongo.MongoClient('127.0.0.1:27017')
        db = client[db_name]
        self.db = db
        self.pod_collection = self.db.pod
        self.node_collection = self.db.node

    def get_collection(self, specifier, grace=False):
        if specifier == 'node':
            if grace:
                return self.ngrace
            return self.node_collection
        if grace:
            return self.pgrace
        return self.pod_collection

    def update_collection(self, myjson, specifier):
        if type(myjson) is not str:
            myjson = json.dumps(myjson)
        data = json.loads(myjson)
        collection = self.get_collection(specifier)
        for key in data['items']:
            name = key['containers'][0]['name']
            cpu = float((key['containers'][0]['usage']['cpu'])[:-1])
            mem = float((key['containers'][0]['usage']['memory'])[:-2])
            timestamp = 'date'
            record = collection.find_one({'name': name})
            if record is None:
                if specifier == 'node':
                    self.add_node(name=name, timestamp=timestamp, cpu=cpu, mem=mem)
                else:
                    self.add_pod(name=name, timestamp=timestamp, cpu=cpu, mem=mem)
            else:
                collection.update_one({'name': name}, {'$push': {'timestamp': timestamp, 'cpu': cpu, 'mem': mem}})

    def get_data(self, specifier, name, data, timestamp=0, all=False):
        collection = self.get_collection(specifier)
        record = collection.find_one({'name': name}, {'_id': 0, data: 1, 'timestamp': 1})
        record = list(record.values())
        if (timestamp == 0 and not all) or data == 'timestamp':
            if data == 'timestamp':
                return record[0][-1]
            return record[1][-1]  # latest
        if all or data == 'timestamp':
            if data == 'timestamp':
                return record[0]
            return record[1]
        try:
            index = record[0].index(timestamp)
        except Exception:
            print('A prediction is needed for your timeStamp')
        else:
            return record[1][index]

    def set_node_for_pod(self, pod_name, new_node):
        self.pod_collection.update_one({'name': pod_name}, {'$set': {'node': new_node}})

    def get_node_from_pod(self, pod_name):
        return list(self.pod_collection.find_one({'name': pod_name}, {'node': 1, '_id': 0}).values())[0]

    def get_pods_on_node(self, node_name):
        return list(self.node_collection.find_one({'name': node_name}, {'pods': 1, '_id': 0}).values())[0]

    def add_pods_to_node(self, pods, node_name):
        self.node_collection.update_one({'name': node_name}, {'$push': {'pods': pods}})
        self.update_node_apps(node_name=node_name)
        self.update_usage(node_name=node_name, pods=pods)

    def remove_pods_form_node(self, pods, node_name):
        pods_on = self.get_pods_on_node(node_name)
        for pod in pods:
            pods_on.remove(pod)
        self.node_collection.update_one({'name': node_name}, {'$set': {'pods': pods_on}})
        self.update_node_apps(node_name=node_name)
        self.update_usage(node_name=node_name, pods=pods)

    def add_pods_in_cluster(self, pods, pod_name):
        self.pod_collection.update_one({'name': pod_name}, {'$push': {'cluster': pods}})

    def get_pods_in_cluster(self, pod_name):
        return list(self.pod_collection.find_one({'name': pod_name}, {'cluster': 1, '_id': 0}).values())[0]

    def remove_pods_from_cluster(self, pods, pod_name):
        pods_on = self.get_pods_in_cluster(pod_name)
        for pod in pods:
            pods_on.remove(pod)
        self.pod_collection.update_one({'name': pod_name}, {'$set': {'cluster': pods_on}})

    def get_df(self, name, specifier):

        timestamps = self.get_data(name=name, data='timestamp', specifier=specifier, all=True)
        cpu = self.get_data(name=name, data='cpu', specifier=specifier, all=True)
        memory = self.get_data(name=name, data='mem', specifier=specifier, all=True)
        data = {'time': timestamps, 'cpu': cpu, 'memory': memory}
        df = pd.DataFrame(data=data)
        return df

    def add_pod(self, name, timestamp, cpu, mem):
        self.pod_collection.insert({'name': name, 'timestamp': [timestamp], 'cpu': [float(cpu)], 'mem': [float(mem)],
                                    'cluster': [], 'node': '', 'app': '', 'wc_pred': 0, 'wm_pred': 0, 'grace': True})

    def add_node(self, name, timestamp, cpu, mem):
        self.node_collection.insert({'name': name, 'timestamp': [timestamp], 'cpu': [float(cpu)], 'mem': [float(mem)],
                                     'pods': [], 'ratio': {'mem': 0, 'cpu': 1}, 'app': [],
                                     'wc_pred': 0, 'wm_pred': 0, 'limit': 0, 'request': 0,
                                     'cpu_to_use': 0, 'mem_to_use': 0, 'familyType': 'no_family', 'grace': True})

    def get_app(self, name, specifier):
        collection = self.get_collection(specifier)
        return list(collection.find_one({'name': name}, {'_id': 0, 'app': 1}).values())[0]

    def update_node_apps(self, node_name):
        pods_on = self.get_pods_on_node(node_name)
        apps = []
        for pod in pods_on:
            app = list(self.pod_collection.find_one({'name': pod}, {'_id': 0, 'app': 1}).values())[0]
            apps.append(app)
        self.node_collection.update_one({'name': node_name}, {'$set': {'app': apps}})

    def get_all(self, specifier, cpu_bar, mem_bar, less=False, more=False):  # getting all docs by criteria
        collection = self.get_collection(specifier)
        # Getting all the names if cursor type
        names = collection.find({}, {'_id': 0, 'name': 1})
        fits = []  # List for all the names how fit the criteria
        for name in names:
            # Extracting from cursor
            actual_name = list(name.values())[0][0]
            # Getting the data for each name(pod or node)
            cpu = self.get_data(specifier, actual_name, 'cpu', all=True)
            memory = self.get_data(specifier, actual_name, 'mem', all=True)
            # calculating means and checking if there gt or lt the bars
            if less and (np.mean(cpu) < cpu_bar and np.mean(memory) < mem_bar):
                fits.append(actual_name)
            elif more and (np.mean(cpu) >= cpu_bar and np.mean(memory) >= mem_bar):
                fits.append(actual_name)
        return fits

    # after the pred
    def grace(self,name, specifier):
        wishing_date = datetime.datetime.now() + datetime.timedelta(days=7)
        timestamp = time.mktime(datetime.datetime.strptime(wishing_date, "%d/%m/%Y").timetuple())
        analyzer = Analytics(self)
        cpu_pred = analyzer.predict(name,specifier,'cpu', timestamp)
        mem_pred = analyzer.predict(name,specifier,'mem', timestamp)
        collection = self.get_collection(specifier)
        record = collection.find_one({'name':name}, {'_id': 0, 'wc_pred': 1, 'wm_pred': 1, 'grace': 1})
        # if True,
        if (cpu_pred >= 0.95 * record['wc_pred'] or mem_pred >= 0.95 * record['wm_pred']) and record['grace']:
            collection.update_one({'name': name}, {'$set': {'gerce': False, 'wc_pred': cpu_pred, 'wm_pred': mem_pred}})
            self.move(name, specifier)
            # put node/pod on grace time until next week
        elif cpu_pred > 1.1 * record['wc_pred'] or mem_pred > 1.1 * record['wm_pred']:
            collection.update_one({'name': name}, {'$set': {'gerce': True, 'wc_pred': cpu_pred, 'wm_pred': mem_pred}})
        else:
            collection.update_one({'name': name}, {'$set': {'wc_pred': cpu_pred, 'wm_pred': mem_pred}})

    def move(self,name,specifier):
        pass

    def set_ratio(self, node_name, new_ratio):
        pass

    def get_ratio(self, node_name):
        pass

    def set_famliy(self, node_name, new_family):
        pass

    def get_famliy(self):
        pass

    def set_limit(self, node_name, new_lim):
        pass

    def get_limit(self, node_name):
        pass

    def set_request(self, node_name, new_rec):
        pass

    def get_request(self, node_name):
        pass

    def update_usage(self, node_name, pods): # current node's usage - pod's mean usage * every pod added.after analytic
        pass





















