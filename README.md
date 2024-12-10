## 환경설정(kubernetes, docker가 설치된 환경)
###  NFS 서버 패키지를 설치
```bash
$ sudo apt update
$ sudo apt install nfs-kernel-server
$ sudo apt install nfs-common
```
###  pip 패키지 설치
```bash
$ pip3 install kubernetes dotenv
```
### 1. Get Tango git repository(클러스터링된 모든 Kubentes Node)
### TANGO git 폴더와 ToK8s Tango 같은 path에 다운로드 
```bash

# git clone 다운로드 받기
$ git clone https://github.com/ML-TANGO/TANGO.git
$ git clone https://github.com/ML-TANGO/ToK8s.git

# Git 폴더 확인
$ ls
TANGO         TANGO_kube_yaml


# TANGO 이미지 빌드 & 권한 부여
$ chmod 777 -R TANGO/
$ cd TANGO
$ docker-compose build  

# k8s TANGO 다운확인 & 권한 부여
$ chmod 777 -R TANGO_kube_yaml/
$ cd TANGO_kube_yaml
```

### 2.NFS 설정(Master Node)

```bash
# NFS 폴더 설정
$ vi /etc/exportfs
```


```bash
# NFS 폴더 설정
[path to TANGO root folder PATH (ex /home/test/desktop/TANGO)]  *(rw,async,no_subtree_check,no_auth_nlm,insecure,no_root_squash,nohide,crossmnt)
[path to TANGO_kube_yaml root folder PATH (ex /home/test/desktop/TANGO_kube_yaml)] *(rw,async,no_subtree_check,no_auth_nlm,insecure,no_root_squash,nohide,crossmnt)
```



### 3.kubenetes Port Range 수정(Master Node)
```bash
# 현재 브랜치 확인
$ sudo vi /etc/kubernetes/manifests/kube-apiserver.yaml

```
#### 아래 command 항목중 마지막줄에 --service-node-port-range 값을 8000-34000으로 수정 혹은 추가


```bash
# 현재 브랜치 확인
spec:
  containers:
  - command:
    - kube-apiserver
    - --allow-privileged=true
    - --authorization-mode=Node,RBAC
    - --client-ca-file=/etc/kubernetes/pki/ca.crt
    - --enable-admission-plugins=NodeRestriction
    - --enable-bootstrap-token-auth=true
    - --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
    ....
    - --service-node-port-range=8000-34000     <----추가 or 30000-32150을 수정

```


### 4.Config 수정(Master Node)
```bash
# TANGO 이미지가 설치된 Host IP 입력 
$ vi ToK8sPATH/TANGO_kube_yaml/.env
NFS_IP = Master Node IP

```



## k8skubernets 설치
```bash
$ cd [path to k8s tango]/TANGO_kube_yaml/
$ python3 tango.py
```


### 쿠버네티스 명령어를 통해 각 Pod가 정상적으로 설치 되었는지 확인..
```bash
$ kubectl get pod -ntango

bms-68d9fbcdf6-l8dvs               1/1     Running            0          3d2h
cloud-deploy-79d9c6ccb5-22jv4      1/1     Running            0          3d2h
codegen-74dd865b66-ssdkr           0/1     Running            10         3d2h
labelling-d8579bfbb-8ln95          1/1     Running            0          3d2h
ondevice-85ddc8b6d5-5nlwx          1/1     Running            0          3d2h
postgresql-5556dc59fb-jb2gf        1/1     Running            0          3d2h
projectmanager-7ff49974f4-mqjns    1/1     Running            0          3d2h
yoloe-7685c89cf5-87gwd             1/1     Running            0          3d2h
resnet-566dfc45b5-vjd8k            1/1     Running            0          3d2h
viz2code-7bbbdbb8b8-dwmxd          1/1     Running            0          3d2h

```

### 웹 페이지에서 TANGO PAGE 접속 방법..
<img src="./docs/media/TANGO_web.png" alt="k8s image" width="600px"/>


### 삭제 방법..
```bash
$ kubectl delete namespace  tango
$ kubectl delete kubectl delete pv pvnfs-bms pvnfs-cloud-deploy  pvnfs-code-gen  pvnfs-labelling-datadb pvnfs-labelling-dataset pvnfs-ondevice-deploy pvnfs-postgresql pvnfs-prm pvnfs-resnet pvnfs-shared  pvnfs-viz2code pvnfs-yoloe


```
