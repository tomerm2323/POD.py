from MongoClass import Mongoc
import pymongo
import pandas as pd
import copy

from Analytics import Analytics
import json



def print_hi(name):

    client = pymongo.MongoClient('127.0.0.1:27017')

    db = client['servers']
    coll = db.pod

    rec = {
        "time":['someTime'],
        'cpu':[4],
        'mem':[2],
        'p':[coll.find_one({'cpu':[4]}),coll.find_one({'cpu':[4]})]
    }

    coll.insert_one(rec)
    coll.update_one({'cpu':4},{'$push':{'p':coll.find_one({'cpu':[4]})}})















if __name__ == '__main__':
    metric = """{
  "kind": "PodMetricsList",
  "apiVersion": "metrics.k8s.io/v1beta1",
  "metadata": {
    "selfLink": "/apis/metrics.k8s.io/v1beta1/pods"
  },
  "items": [
    {
      "metadata": {
        "name": "pingpongapi-depl-b4d46759d-wgs2d",
        "namespace": "default",
        "selfLink": "/apis/metrics.k8s.io/v1beta1/namespaces/default/pods/pingpongapi-depl-b4d46759d-wgs2d",
        "creationTimestamp": "2021-09-16T23:19:01Z"
      },
      "timestamp": "2021-09-16T23:18:45Z",
      "window": "30s",
      "containers": [
        {
          "name": "neosec-grpc-sniffer",
          "usage": {
            "cpu": "4383939n",
            "memory": "24796Ki"
          }
        },
        {
          "name": "pingpongapi",
          "usage": {
            "cpu": "385770n",
            "memory": "2628Ki"
          }
        }
      ]
    },
    {
      "metadata": {
        "name": "coredns-74ff55c5b-8zzlj",
        "namespace": "kube-system",
        "selfLink": "/apis/metrics.k8s.io/v1beta1/namespaces/kube-system/pods/coredns-74ff55c5b-8zzlj",
        "creationTimestamp": "2021-09-16T23:19:01Z"
      },
      "timestamp": "2021-09-16T23:18:39Z",
      "window": "30s",
      "containers": [
        {
          "name": "coredns",
          "usage": {
            "cpu": "15630861n",
            "memory": "13964Ki"
          }
        }
      ]
    },
    {
      "metadata": {
        "name": "etcd-minikube",
        "namespace": "kube-system",
        "selfLink": "/apis/metrics.k8s.io/v1beta1/namespaces/kube-system/pods/etcd-minikube",
        "creationTimestamp": "2021-09-16T23:19:01Z"
      },
      "timestamp": "2021-09-16T23:18:44Z",
      "window": "30s",
      "containers": [
        {
          "name": "etcd",
          "usage": {
            "cpu": "43068696n",
            "memory": "56088Ki"
          }
        }
      ]
    },
    {
      "metadata": {
        "name": "kube-apiserver-minikube",
        "namespace": "kube-system",
        "selfLink": "/apis/metrics.k8s.io/v1beta1/namespaces/kube-system/pods/kube-apiserver-minikube",
        "creationTimestamp": "2021-09-16T23:19:01Z"
      },
      "timestamp": "2021-09-16T23:18:49Z",
      "window": "30s",
      "containers": [
        {
          "name": "kube-apiserver",
          "usage": {
            "cpu": "153788877n",
            "memory": "286808Ki"
          }
        }
      ]
    },
    {
      "metadata": {
        "name": "kube-controller-manager-minikube",
        "namespace": "kube-system",
        "selfLink": "/apis/metrics.k8s.io/v1beta1/namespaces/kube-system/pods/kube-controller-manager-minikube",
        "creationTimestamp": "2021-09-16T23:19:01Z"
      },
      "timestamp": "2021-09-16T23:18:44Z",
      "window": "30s",
      "containers": [
        {
          "name": "kube-controller-manager",
          "usage": {
            "cpu": "67851140n",
            "memory": "55132Ki"
          }
        }
      ]
    },
    {
      "metadata": {
        "name": "kube-proxy-qc4sh",
        "namespace": "kube-system",
        "selfLink": "/apis/metrics.k8s.io/v1beta1/namespaces/kube-system/pods/kube-proxy-qc4sh",
        "creationTimestamp": "2021-09-16T23:19:01Z"
      },
      "timestamp": "2021-09-16T23:18:48Z",
      "window": "30s",
      "containers": [
        {
          "name": "kube-proxy",
          "usage": {
            "cpu": "325673n",
            "memory": "11940Ki"
          }
        }
      ]
    },
    {
      "metadata": {
        "name": "kube-scheduler-minikube",
        "namespace": "kube-system",
        "selfLink": "/apis/metrics.k8s.io/v1beta1/namespaces/kube-system/pods/kube-scheduler-minikube",
        "creationTimestamp": "2021-09-16T23:19:01Z"
      },
      "timestamp": "2021-09-16T23:18:38Z",
      "window": "30s",
      "containers": [
        {
          "name": "kube-scheduler",
          "usage": {
            "cpu": "7078323n",
            "memory": "19776Ki"
          }
        }
      ]
    },
    {
      "metadata": {
        "name": "metrics-server-7894db45f8-dgsvq",
        "namespace": "kube-system",
        "selfLink": "/apis/metrics.k8s.io/v1beta1/namespaces/kube-system/pods/metrics-server-7894db45f8-dgsvq",
        "creationTimestamp": "2021-09-16T23:19:01Z"
      },
      "timestamp": "2021-09-16T23:18:42Z",
      "window": "30s",
      "containers": [
        {
          "name": "metrics-server",
          "usage": {
            "cpu": "9322647n",
            "memory": "21204Ki"
          }
        }
      ]
    },
    {
      "metadata": {
        "name": "storage-provisioner",
        "namespace": "kube-system",
        "selfLink": "/apis/metrics.k8s.io/v1beta1/namespaces/kube-system/pods/storage-provisioner",
        "creationTimestamp": "2021-09-16T23:19:01Z"
      },
      "timestamp": "2021-09-16T23:18:36Z",
      "window": "30s",
      "containers": [
        {
          "name": "storage-provisioner",
          "usage": {
            "cpu": "4195786n",
            "memory": "11812Ki"
          }
        }
      ]
    },
    {
      "metadata": {
        "name": "neoagent-collector-deployment-6d9cd44b87-bzgl4",
        "namespace": "neoagent",
        "selfLink": "/apis/metrics.k8s.io/v1beta1/namespaces/neoagent/pods/neoagent-collector-deployment-6d9cd44b87-bzgl4",
        "creationTimestamp": "2021-09-16T23:19:01Z"
      },
      "timestamp": "2021-09-16T23:18:39Z",
      "window": "30s",
      "containers": [
        {
          "name": "neoagent-collector",
          "usage": {
            "cpu": "14164010n",
            "memory": "191128Ki"
          }
        }
      ]
    },
    {
      "metadata": {
        "name": "neoagent-collector-5b87f8546-jjgdc",
        "namespace": "neosec",
        "selfLink": "/apis/metrics.k8s.io/v1beta1/namespaces/neosec/pods/neoagent-collector-5b87f8546-jjgdc",
        "creationTimestamp": "2021-09-16T23:19:01Z"
      },
      "timestamp": "2021-09-16T23:18:47Z",
      "window": "30s",
      "containers": [
        {
          "name": "neoagent-collector",
          "usage": {
            "cpu": "11176381n",
            "memory": "611180Ki"
          }
        }
      ]
    }
  ]
}
"""


    # mydb = Mongoc('placeless')
    # mydb.update_collection(metric,'pod')
    # mydb.update_collection(metric, 'node')
    # an = Analytics(mydb)
    # print(an.get_peak('neosec-grpc-sniffer','node','mem'))
    # print(an.fit_data(name='neosec-grpc-sniffer',specifier='node',data='cpu',models=[an.linear,an.sqr,an.cube,an.sin,an.log]))
    #metric = json.dumps(metric)

    #data = json.loads(metric)
    #for key in data['items']:
     #   print(float(key['containers'][0]['usage']['memory'][:-2]))

        #name = list(list(full_data[3])[0].values())[0]
        #cpu = list(list(list(full_data[3])[0].values())[1].values())[0][:-1]
        #mem = list(list(list(full_data[3])[0].values())[1].values())[1][:-2]
        #timestamp = list(key.items())[1][1]
        #record = collection.find_one({'name': name})













