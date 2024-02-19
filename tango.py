import os
from kubernetes import client, config
from dotenv import load_dotenv

load_dotenv()

# NFS IP
NFS_IP = os.getenv("NFS_IP")

# volume mount path
current_file_path = os.path.abspath(__file__)
tango_root_path = current_file_path.replace("TANGO_kube_yaml/tango.py", "")
tango_path = current_file_path.replace("tango.py", "")

"""
통합shard 메모리 pv,pvc
"""
def create_shared_persistent_volume_object():
    pv = client.V1PersistentVolume(
        api_version="v1",
        kind="PersistentVolume",
        metadata=client.V1ObjectMeta(name="pvnfs-shared", labels={"name": "shared"}),
        spec=client.V1PersistentVolumeSpec(
            capacity={"storage": "10Gi"},
            volume_mode="Filesystem",
            access_modes=["ReadWriteMany"],
            # persistent_volume_reclaim_policy="Recycle",
            mount_options=["hard", "nfsvers=4.1"],
            nfs=client.V1NFSVolumeSource(
                path=f"{tango_path}share",
                server=NFS_IP
            ),
            storage_class_name=""
        )
    )
    return pv

def create_shared_persistent_volume_claim_object():
    pvc = client.V1PersistentVolumeClaim(
        api_version="v1",
        kind="PersistentVolumeClaim",
        metadata=client.V1ObjectMeta(name="pvcnfs-shared"),
        spec=client.V1PersistentVolumeClaimSpec(
            resources=client.V1ResourceRequirements(
                requests={"storage": "10Gi"}
            ),
            volume_mode="Filesystem",
            selector=client.V1LabelSelector(
                match_labels={"name": "shared"}
            ),
            access_modes=["ReadWriteMany"],
            storage_class_name=""
        )
    )
    return pvc



"""postgresssql

"""
def create_postgresql_persistent_volume_claim_object():
    pvc = client.V1PersistentVolumeClaim(
        api_version="v1",
        kind="PersistentVolumeClaim",
        metadata=client.V1ObjectMeta(name="pvcnfs-postgresql"),
        spec=client.V1PersistentVolumeClaimSpec(
            resources=client.V1ResourceRequirements(
                requests={"storage": "6Gi"}
            ),
            volume_mode="Filesystem",
            selector=client.V1LabelSelector(
                match_labels={"name": "pvcnfs-postgresql"}
            ),
            access_modes=["ReadWriteMany"],
            storage_class_name=""
        )
    )
    return pvc

def create_postgresql_persistent_volume_object():
    pv = client.V1PersistentVolume(
        api_version="v1",
        kind="PersistentVolume",
        metadata=client.V1ObjectMeta(name="pvnfs-postgresql", labels={"name": "pvcnfs-postgresql"}),
        spec=client.V1PersistentVolumeSpec(
            capacity={"storage": "6Gi"},
            volume_mode="Filesystem",
            access_modes=["ReadWriteMany"],
            # persistent_volume_reclaim_policy="Recycle",
            mount_options=["hard", "nfsvers=4.1"],            
            nfs=client.V1NFSVolumeSource(
                path=f"{tango_path}share/postgreSQL",
                server=NFS_IP
            ),
            storage_class_name=""
        )
    )
    return pv


"""
projectmanager
"""
def create_projectmanager_persistent_volume_claim_object():
    pvc = client.V1PersistentVolumeClaim(
        api_version="v1",
        kind="PersistentVolumeClaim",
        metadata=client.V1ObjectMeta(name="pvcnfs-prm"),
        spec=client.V1PersistentVolumeClaimSpec(
            resources=client.V1ResourceRequirements(
                requests={"storage": "5Gi"}
            ),
            volume_mode="Filesystem",
            selector=client.V1LabelSelector(
                match_labels={"name": "prm"}
            ),
            access_modes=["ReadWriteMany"],
            storage_class_name=""
        )
    )
    return pvc

def create_projectmanager_persistent_volume_object():
    pv = client.V1PersistentVolume(
        api_version="v1",
        kind="PersistentVolume",
        metadata=client.V1ObjectMeta(
            name="pvnfs-prm",
            labels={"name": "prm"}
        ),
        spec=client.V1PersistentVolumeSpec(
            capacity={"storage": "5Gi"},
            volume_mode="Filesystem",
            access_modes=["ReadWriteMany"],
            # persistent_volume_reclaim_policy="Recycle",
            nfs=client.V1NFSVolumeSource(
                path=f"{tango_root_path}TANGO/project_manager",
                server=NFS_IP
            ),
            storage_class_name=""
        )
    )
    return pv

"""
라벨링
"""
def create_labelling_dataset_persistent_volume_object():
    pv = client.V1PersistentVolume(
        api_version="v1",
        kind="PersistentVolume",
        metadata=client.V1ObjectMeta(name="pvnfs-labelling-dataset", labels={"name": "labelling-dataset"}),
        spec=client.V1PersistentVolumeSpec(
            capacity={"storage": "5Gi"},
            volume_mode="Filesystem",
            access_modes=["ReadWriteMany"],
            nfs=client.V1NFSVolumeSource(
                path=tango_root_path + "TANGO/labelling/dataset",
                server=NFS_IP
            ),
            storage_class_name=""
        )
    )
    return pv

def create_labelling_dataset_persistent_volume_claim_object():
    pvc = client.V1PersistentVolumeClaim(
        api_version="v1",
        kind="PersistentVolumeClaim",
        metadata=client.V1ObjectMeta(name="pvcnfs-labelling-dataset"),
        spec=client.V1PersistentVolumeClaimSpec(
            resources=client.V1ResourceRequirements(
                requests={"storage": "5Gi"}
            ),
            volume_mode="Filesystem",
            selector=client.V1LabelSelector(
                match_labels={"name": "labelling-dataset"}
            ),
            access_modes=["ReadWriteMany"],
            storage_class_name=""
        )
    )
    return pvc

def create_labelling_datadb_persistent_volume_object():
    pv = client.V1PersistentVolume(
        api_version="v1",
        kind="PersistentVolume",
        metadata=client.V1ObjectMeta(name="pvnfs-labelling-datadb", labels={"name": "labelling-datadb"}),
        spec=client.V1PersistentVolumeSpec(
            capacity={"storage": "5Gi"},
            volume_mode="Filesystem",
            access_modes=["ReadWriteMany"],
            nfs=client.V1NFSVolumeSource(
                path=tango_root_path + "TANGO/labelling/datadb",
                server=NFS_IP
            ),
            storage_class_name=""
        )
    )
    return pv

def create_labelling_datadb_persistent_volume_claim_object():
    pvc = client.V1PersistentVolumeClaim(
        api_version="v1",
        kind="PersistentVolumeClaim",
        metadata=client.V1ObjectMeta(name="pvcnfs-labelling-datadb"),
        spec=client.V1PersistentVolumeClaimSpec(
            resources=client.V1ResourceRequirements(
                requests={"storage": "5Gi"}
            ),
            volume_mode="Filesystem",
            selector=client.V1LabelSelector(
                match_labels={"name": "labelling-datadb"}
            ),
            access_modes=["ReadWriteMany"],
            storage_class_name=""
        )
    )
    return pvc


    """
    bms
    """
def create_bms_persistent_volume_object():
    pv = client.V1PersistentVolume(
        api_version="v1",
        kind="PersistentVolume",
        metadata=client.V1ObjectMeta(name="pvnfs-bms", labels={"name": "bms"}),
        spec=client.V1PersistentVolumeSpec(
            capacity={"storage": "5Gi"},
            volume_mode="Filesystem",
            access_modes=["ReadWriteMany"],
            # persistent_volume_reclaim_policy="Recycle",
            nfs=client.V1NFSVolumeSource(
                path=tango_root_path + "TANGO/base_model_select",
                server=NFS_IP
            ),
            storage_class_name=""
        )
    )
    return pv

def create_bms_persistent_volume_claim_object():
    pvc = client.V1PersistentVolumeClaim(
        api_version="v1",
        kind="PersistentVolumeClaim",
        metadata=client.V1ObjectMeta(name="pvcnfs-bms"),
        spec=client.V1PersistentVolumeClaimSpec(
            resources=client.V1ResourceRequirements(
                requests={"storage": "5Gi"}
            ),
            volume_mode="Filesystem",
            selector=client.V1LabelSelector(
                match_labels={"name": "bms"}
            ),
            access_modes=["ReadWriteMany"],
            storage_class_name=""
        )
    )
    return pvc


    """
    yoloe
    """
def create_yoloe_persistent_volume_object():
    pv = client.V1PersistentVolume(
        api_version="v1",
        kind="PersistentVolume",
        metadata=client.V1ObjectMeta(name="pvnfs-yoloe", labels={"name": "yoloe"}),
        spec=client.V1PersistentVolumeSpec(
            capacity={"storage": "5Gi"},
            volume_mode="Filesystem",
            access_modes=["ReadWriteMany"],
            # persistent_volume_reclaim_policy="Recycle",
            nfs=client.V1NFSVolumeSource(
                path=tango_root_path + "TANGO/autonn/YoloE",
                server=NFS_IP
            ),
            storage_class_name=""
        )
    )
    return pv

def create_yoloe_persistent_volume_claim_object():
    pvc = client.V1PersistentVolumeClaim(
        api_version="v1",
        kind="PersistentVolumeClaim",
        metadata=client.V1ObjectMeta(name="pvcnfs-yoloe"),
        spec=client.V1PersistentVolumeClaimSpec(
            resources=client.V1ResourceRequirements(
                requests={"storage": "5Gi"}
            ),
            volume_mode="Filesystem",
            selector=client.V1LabelSelector(
                match_labels={"name": "yoloe"}
            ),
            access_modes=["ReadWriteMany"],
            storage_class_name=""
        )
    )
    return pvc




    """
    resnet
    """
def create_resnet_persistent_volume_object():
    pv = client.V1PersistentVolume(
        api_version="v1",
        kind="PersistentVolume",
        metadata=client.V1ObjectMeta(name="pvnfs-resnet", labels={"name": "resnet"}),
        spec=client.V1PersistentVolumeSpec(
            capacity={"storage": "5Gi"},
            volume_mode="Filesystem",
            access_modes=["ReadWriteMany"],
            # persistent_volume_reclaim_policy="Recycle",
            nfs=client.V1NFSVolumeSource(
                path=tango_root_path + "TANGO/autonn/ResNet",
                server=NFS_IP
            ),
            storage_class_name=""
        )
    )
    return pv

def create_resnet_persistent_volume_claim_object():
    pvc = client.V1PersistentVolumeClaim(
        api_version="v1",
        kind="PersistentVolumeClaim",
        metadata=client.V1ObjectMeta(name="pvcnfs-resnet"),
        spec=client.V1PersistentVolumeClaimSpec(
            resources=client.V1ResourceRequirements(
                requests={"storage": "5Gi"}
            ),
            volume_mode="Filesystem",
            selector=client.V1LabelSelector(
                match_labels={"name": "resnet"}
            ),
            access_modes=["ReadWriteMany"],
            storage_class_name=""
        )
    )
    return pvc


    """
    codegen
    """
def create_code_gen_persistent_volume_object():
    pv = client.V1PersistentVolume(
        api_version="v1",
        kind="PersistentVolume",
        metadata=client.V1ObjectMeta(name="pvnfs-code-gen", labels={"name": "code-gen"}),
        spec=client.V1PersistentVolumeSpec(
            capacity={"storage": "5Gi"},
            volume_mode="Filesystem",
            access_modes=["ReadWriteMany"],
            # persistent_volume_reclaim_policy="Recycle",
            nfs=client.V1NFSVolumeSource(
                path=tango_root_path + "TANGO/deploy_codegen/optimize_codegen",
                server=NFS_IP
            ),
            storage_class_name=""
        )
    )
    return pv

def create_code_gen_persistent_volume_claim_object():
    pvc = client.V1PersistentVolumeClaim(
        api_version="v1",
        kind="PersistentVolumeClaim",
        metadata=client.V1ObjectMeta(name="pvcnfs-code-gen"),
        spec=client.V1PersistentVolumeClaimSpec(
            resources=client.V1ResourceRequirements(
                requests={"storage": "5Gi"}
            ),
            volume_mode="Filesystem",
            selector=client.V1LabelSelector(
                match_labels={"name": "code-gen"}
            ),
            access_modes=["ReadWriteMany"],
            storage_class_name=""
        )
    )
    return pvc

    """
    cloud_deploy
    """
def create_cloud_deploy_persistent_volume_object():
    pv = client.V1PersistentVolume(
        api_version="v1",
        kind="PersistentVolume",
        metadata=client.V1ObjectMeta(name="pvnfs-cloud-deploy", labels={"name": "cloud-deploy"}),
        spec=client.V1PersistentVolumeSpec(
            capacity={"storage": "5Gi"},
            volume_mode="Filesystem",
            access_modes=["ReadWriteMany"],
            # persistent_volume_reclaim_policy="Recycle",
            nfs=client.V1NFSVolumeSource(
                path=tango_root_path + "TANGO/deploy_targets/cloud",
                server=NFS_IP
            ),
            storage_class_name=""
        )
    )
    return pv

def create_cloud_deploy_persistent_volume_claim_object():
    pvc = client.V1PersistentVolumeClaim(
        api_version="v1",
        kind="PersistentVolumeClaim",
        metadata=client.V1ObjectMeta(name="pvcnfs-cloud-deploy"),
        spec=client.V1PersistentVolumeClaimSpec(
            resources=client.V1ResourceRequirements(
                requests={"storage": "5Gi"}
            ),
            volume_mode="Filesystem",
            selector=client.V1LabelSelector(
                match_labels={"name": "cloud-deploy"}
            ),
            access_modes=["ReadWriteMany"],
            storage_class_name=""
        )
    )
    return pvc


    """
    ondevice_deploy
    """
def create_ondevice_deploy_persistent_volume_object():
    pv = client.V1PersistentVolume(
        api_version="v1",
        kind="PersistentVolume",
        metadata=client.V1ObjectMeta(name="pvnfs-ondevice-deploy", labels={"name": "ondevice-deploy"}),
        spec=client.V1PersistentVolumeSpec(
            capacity={"storage": "5Gi"},
            volume_mode="Filesystem",
            access_modes=["ReadWriteMany"],
            # persistent_volume_reclaim_policy="Recycle",
            nfs=client.V1NFSVolumeSource(
                path=tango_root_path + "TANGO/deploy_targets/ondevice",
                server=NFS_IP
            ),
            storage_class_name=""
        )
    )
    return pv

def create_ondevice_deploy_persistent_volume_claim_object():
    pvc = client.V1PersistentVolumeClaim(
        api_version="v1",
        kind="PersistentVolumeClaim",
        metadata=client.V1ObjectMeta(name="pvcnfs-ondevice-deploy"),
        spec=client.V1PersistentVolumeClaimSpec(
            resources=client.V1ResourceRequirements(
                requests={"storage": "5Gi"}
            ),
            volume_mode="Filesystem",
            selector=client.V1LabelSelector(
                match_labels={"name": "ondevice-deploy"}
            ),
            access_modes=["ReadWriteMany"],
            storage_class_name=""
        )
    )
    return pvc


    """
    viz2code
    """
def create_viz2code_persistent_volume_object():
    pv = client.V1PersistentVolume(
        api_version="v1",
        kind="PersistentVolume",
        metadata=client.V1ObjectMeta(name="pvnfs-viz2code", labels={"name": "viz2code"}),
        spec=client.V1PersistentVolumeSpec(
            capacity={"storage": "5Gi"},
            volume_mode="Filesystem",
            access_modes=["ReadWriteMany"],
            # persistent_volume_reclaim_policy="Recycle",
            nfs=client.V1NFSVolumeSource(
                path=tango_root_path + "TANGO/visualization",
                server=NFS_IP
            ),
            storage_class_name=""
        )
    )
    return pv

def create_viz2code_persistent_volume_claim_object():
    pvc = client.V1PersistentVolumeClaim(
        api_version="v1",
        kind="PersistentVolumeClaim",
        metadata=client.V1ObjectMeta(name="pvcnfs-viz2code"),
        spec=client.V1PersistentVolumeClaimSpec(
            resources=client.V1ResourceRequirements(
                requests={"storage": "5Gi"}
            ),
            volume_mode="Filesystem",
            selector=client.V1LabelSelector(
                match_labels={"name": "viz2code"}
            ),
            access_modes=["ReadWriteMany"],
            storage_class_name=""
        )
    )
    return pvc




def create_postgresql_deployment_object():
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name="postgresql"),
        spec=client.V1DeploymentSpec(
            selector=client.V1LabelSelector(
                match_labels={"app": "postgresql"}
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": "postgresql"}),
                spec=client.V1PodSpec(
                    # nodeName="etri-1",
                    containers=[
                        
                        #디비
                        client.V1Container(
                            name="postgresql",
                            image="postgres:15.4",
                            resources=client.V1ResourceRequirements(
                                limits={"memory": "128Mi", "cpu": "500m"}
                            ),
                            volume_mounts=[
                                client.V1VolumeMount(
                                    name="postgresvol",
                                    mount_path="/var/lib/postgresql/data"
                                )
                            ],
                            env=[
                                client.V1EnvVar(name="POSTGRES_NAME", value="postgres"),
                                client.V1EnvVar(name="POSTGRES_USER", value="postgres"),
                                client.V1EnvVar(name="POSTGRES_PASSWORD", value="postgres")
                            ],
                            ports=[client.V1ContainerPort(container_port=5432)]
                            
                        ),                               
                    ],
                    volumes=[
                      
                        #디비
                        client.V1Volume(
                            name="postgresvol",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="pvcnfs-postgresql"
                            )
                        )
                    ]                   

                        
                    
                )
            )
        )
    )
    return deployment



def create_projectmanager_deployment_object():
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name="projectmanager"),
        spec=client.V1DeploymentSpec(
            selector=client.V1LabelSelector(
                match_labels={"app": "projectmanager"}
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": "projectmanager"}),
                spec=client.V1PodSpec(
                    containers=[
                        
                        client.V1Container(
                            name="projectmanager",
                            image="tango_project_manager",
                            image_pull_policy="Never",
                            resources=client.V1ResourceRequirements(
                                limits={"cpu": "1000m", "memory": "2048Mi"}
                            ),
                            volume_mounts=[
                                client.V1VolumeMount(
                                    name="projectmanagervol",
                                    mount_path="/code"
                                ),
                                client.V1VolumeMount(
                                    name="sharedvol",
                                    mount_path="/shared"
                                ),
                                client.V1VolumeMount(
                                    name="dockervol",
                                    mount_path="/var/run/docker.sock"
                                )
                            ],
                            env=[
                                client.V1EnvVar(name="POSTGRES_NAME", value="postgres"),
                                client.V1EnvVar(name="POSTGRES_USER", value="postgres"),
                                client.V1EnvVar(name="POSTGRES_PASSWORD", value="postgres"),
                                client.V1EnvVar(name="postgres-port", value="5432"),
                                client.V1EnvVar(name="POSTGRESQL_SERVICE_IP", value="postgres")
                            ],
                            ports=[client.V1ContainerPort(container_port=8085)],
                            command=["/bin/sh", "-c"],
                            args=[
                                "chmod 777 ./wait_for_postgres.sh && ./wait_for_postgres.sh && python manage.py makemigrations && python manage.py migrate && python manage.py loaddata base_model_data.json &&  python manage.py runserver 0.0.0.0:8085"
                            ]
                            
                        ),                           
                    ],
                    volumes=[
                        client.V1Volume(
                            name="projectmanagervol",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="pvcnfs-prm"
                            )
                        ),
                        client.V1Volume(
                            name="sharedvol",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="pvcnfs-shared"
                            )
                        ),
                         client.V1Volume(
                            name="dockervol",
                            host_path=client.V1HostPathVolumeSource(path="/var/run/docker.sock")
                        ),
                    ]                   

                        
                    
                )
            )
        )
    )
    return deployment



def create_labelling_deployment_object():
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name="labelling"),
        spec=client.V1DeploymentSpec(
            selector=client.V1LabelSelector(
                match_labels={"app": "labelling"}
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": "labelling"}),
                spec=client.V1PodSpec(
                    containers=[
                        #라벨링
                        client.V1Container(
                            name="labelling",
                            image="tango_labelling",
                            image_pull_policy="Never",
                            resources=client.V1ResourceRequirements(
                                limits={"cpu": "500m", "memory": "2048Mi"}
                            ),
                            volume_mounts=[
                                client.V1VolumeMount(
                                    mount_path="/var/appdata",
                                    name="labellingvol"
                                ),
                                client.V1VolumeMount(
                                    mount_path="/var/lib/mysql",
                                    name="labellingvol-2"
                                ),
                                client.V1VolumeMount(
                                    name="sharedvol",
                                    mount_path="/shared"
                                ),
                            ],
                            ports=[
                                client.V1ContainerPort(container_port=80),
                                client.V1ContainerPort(container_port=10236)
                            ]
                            
                        )                      
                    ],
                    volumes=[
                        #라벨링
                        client.V1Volume(
                            name="labellingvol",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="pvcnfs-labelling-dataset"
                            )
                        ),
                        client.V1Volume(
                            name="labellingvol-2",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="pvcnfs-labelling-datadb"
                            )
                        ),
                        client.V1Volume(
                            name="sharedvol",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="pvcnfs-shared"
                            )
                        )
                    ]
                )
            )
        )
    )
    return deployment



def create_bms_deployment_object():
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name="bms"),
        spec=client.V1DeploymentSpec(
            selector=client.V1LabelSelector(
                match_labels={"app": "bms"}
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": "bms"}),
                spec=client.V1PodSpec(
                    # nodeName="etri-1",
                    containers=[
                        #bms
                        client.V1Container(
                            name="bms",
                            image="tango_bms",
                            image_pull_policy="Never",
                            volume_mounts=[
                                client.V1VolumeMount(
                                    mount_path="/source",
                                    name="bmsvol"
                                ),
                                client.V1VolumeMount(
                                    mount_path="/shared",
                                    name="sharedvol"
                                )
                            ],
                            ports=[
                                client.V1ContainerPort(container_port=8081)
                            ],
                            command=["/bin/sh", "-c"],
                            args=[
                                "python manage.py makemigrations &&"
                                "python manage.py migrate --run-syncdb &&"
                                "python manage.py runserver 0.0.0.0:8081"
                            ]
                        )
         
                    ],
                    volumes=[
                        client.V1Volume(
                            name="sharedvol",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="pvcnfs-shared"
                            )
                        ),
                        #bms
                        client.V1Volume(
                            name="bmsvol",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="pvcnfs-bms"
                            )
                        ),
                    ]
                )
            )
        )
    )
    return deployment


def create_yoloe_deployment_object():
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name="yoloe"),
        spec=client.V1DeploymentSpec(
            selector=client.V1LabelSelector(
                match_labels={"app": "yoloe"}
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": "yoloe"}),
                spec=client.V1PodSpec(
                    # nodeName="etri-1",
                    containers=[
                        # yoloE
                        client.V1Container(
                            name="autonn-yoloe",
                            image="tango_autonn_yoloe",
                            image_pull_policy="Never",
                            volume_mounts=[
                                client.V1VolumeMount(
                                    mount_path="/source",
                                    name="yoloevol"
                                ),
                                client.V1VolumeMount(
                                    mount_path="/shared",
                                    name="sharedvol"
                                ),
                                client.V1VolumeMount(
                                    mount_path="/shared/datasets/coco/dataset.yaml",
                                    name="yoloevol-1"
                                    
                                ),
                                client.V1VolumeMount(
                                    mount_path="/shared/datasets/coco",
                                    name="yoloevol-2"
                                )                                
                            ],
                            ports=[
                                client.V1ContainerPort(container_port=8090)
                            ],
                            command=["/bin/sh", "-c"],
                            args=[
                                "python manage.py pretrained_supernet &&"
                                "python manage.py makemigrations &&"
                                "python manage.py migrate &&"
                                "python manage.py runserver 0.0.0.0:8090"
                            ]
                        )
                    ],
                    volumes=[
                        client.V1Volume(
                            name="sharedvol",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="pvcnfs-shared"
                            )
                        ),
                        #yoloe
                        client.V1Volume(
                            name="yoloevol",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="pvcnfs-yoloe"
                            )
                        ),
                        client.V1Volume(
                            name="yoloevol-1",
                            host_path=client.V1HostPathVolumeSource(path=f"{tango_root_path}TANGO/autonn/YoloE/sample_yaml/dataset.yaml")
                            # persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                            #     claim_name="pvcnfs-yoloe-1"
                            # )
                        ),
                        client.V1Volume(
                            name="yoloevol-2",
                            host_path=client.V1HostPathVolumeSource(path=f"{tango_root_path}TANGO/autonn/YoloE/sample_yaml/")
                            # persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                            #     claim_name="pvcnfs-yoloe-2"
                            # )
                        ),
                    ]
                )
            )
        )
    )
    return deployment


def create_resnet_deployment_object():
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name="resnet"),
        spec=client.V1DeploymentSpec(
            selector=client.V1LabelSelector(
                match_labels={"app": "resnet"}
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": "resnet"}),
                spec=client.V1PodSpec(
                    # nodeName="etri-1",
                    containers=[
                        # resnet
                        client.V1Container(
                            name="autonn-resnet",
                            image="tango_autonn_resnet",
                            image_pull_policy="Never",
                            volume_mounts=[
                                client.V1VolumeMount(
                                    mount_path="/source",
                                    name="resnetvol"
                                ),
                                client.V1VolumeMount(
                                    mount_path="/shared",
                                    name="sharedvol"
                                )                  
                            ],
                            ports=[
                                client.V1ContainerPort(container_port=8092)
                            ],
                            command=["/bin/sh", "-c"],
                            args=[
                            "python manage.py makemigrations &&"
                            "python manage.py migrate &&"
                            "python manage.py runserver 0.0.0.0:8092"
                            ]
                        )

                    ],
                    volumes=[
                        client.V1Volume(
                            name="sharedvol",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="pvcnfs-shared"
                            )
                        ),
                     
                        #resnet
                        client.V1Volume(
                            name="resnetvol",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="pvcnfs-resnet"
                            )
                        )
                    ]
                )
            )
        )
    )
    return deployment



def create_codegen_deployment_object():
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name="codegen"),
        spec=client.V1DeploymentSpec(
            selector=client.V1LabelSelector(
                match_labels={"app": "codegen"}
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": "codegen"}),
                spec=client.V1PodSpec(
                    containers=[
 
                        # code_gen
                        client.V1Container(
                            name="codegen",
                            image="tango_code_gen",
                            image_pull_policy="Never",
                            volume_mounts=[
                                client.V1VolumeMount(
                                    mount_path="/source",
                                    name="code-genvol"
                                ),
                                client.V1VolumeMount(
                                    mount_path="/tango",
                                    name="sharedvol"
                                )                  
                            ],
                            ports=[
                                client.V1ContainerPort(container_port=8888)
                            ],
                            command=["/bin/sh", "-c"],
                            args=[
                            "cd /app && python3 code_gen.py"
                            ]
                        ),                

                    ],
                    volumes=[
                        client.V1Volume(
                            name="sharedvol",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="pvcnfs-shared"
                            )
                        ),

                        client.V1Volume(
                            name="code-genvol",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="pvcnfs-code-gen"
                            )
                        ),
                        
                    ]
                )
            )
        )
    )
    return deployment


def create_cloud_deploy_deployment_object():
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name="cloud-deploy"),
        spec=client.V1DeploymentSpec(
            selector=client.V1LabelSelector(
                match_labels={"app": "cloud-deploy"}
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": "cloud-deploy"}),
                spec=client.V1PodSpec(
                    containers=[
                        # cloud_deploy
                        client.V1Container(
                            name="cloud-deploy",
                            image="tango_cloud_deploy",
                            image_pull_policy="Never",
                            volume_mounts=[
                                client.V1VolumeMount(
                                    mount_path="/source",
                                    name="cloud-deployvol"
                                ),
                                client.V1VolumeMount(
                                    mount_path="/shared",
                                    name="sharedvol"
                                ),          
                                client.V1VolumeMount(
                                    mount_path="/var/run/docker.sock",
                                    name="dockervol"
                                )                                                        
                            ],
                            ports=[
                                client.V1ContainerPort(container_port=7007),
                                client.V1ContainerPort(container_port=8080),
                                client.V1ContainerPort(container_port=8890)
                            ],
                            # command=["/bin/sh", "-c"],
                            # args=[
                            # "cd /app && python3 code_gen.py"
                            # ]
                            env=[
                                client.V1EnvVar(name="CLOUD_MANAGER_PORT", value="8088"),
                                client.V1EnvVar(name="GOOGLE_APPLICATION_CREDENTIALS", value="/source/cloud_manager/service-account-file.json"),
                                client.V1EnvVar(name="GCP_REGION", value="northeast3"),
                                client.V1EnvVar(name="GCP_PROJECT_ID", value="tango-project")
                            ]
                        ), 
                    ],
                    volumes=[
                        client.V1Volume(
                            name="sharedvol",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="pvcnfs-shared"
                            )
                        ),
                         client.V1Volume(
                            name="dockervol",
                            host_path=client.V1HostPathVolumeSource(path="/var/run/docker.sock")
                        ),
                    
                        client.V1Volume(
                            name="cloud-deployvol",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="pvcnfs-cloud-deploy"
                            )
                        )                                
                    ]
                )
            )
        )
    )
    return deployment


def create_ondevice_deployment_object():
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name="ondevice"),
        spec=client.V1DeploymentSpec(
            selector=client.V1LabelSelector(
                match_labels={"app": "ondevice"}
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": "ondevice"}),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name="ondevice-deploy",
                            image="tango_ondevice_deploy",
                            image_pull_policy="Never",
                            volume_mounts=[
                                client.V1VolumeMount(
                                    mount_path="/source",
                                    name="ondevice-deployvol"
                                ),
                                client.V1VolumeMount(
                                    mount_path="/shared",
                                    name="sharedvol"
                                )                                            
                            ],
                            ports=[
                                client.V1ContainerPort(container_port=8891)
                            ],
                            command=["/bin/sh", "-c"],
                            args=[
                            "cd /app && python3 ondevice_deploy.py"
                            ]
                        ),                  

                    ],
                    volumes=[
                        client.V1Volume(
                            name="sharedvol",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="pvcnfs-shared"
                            )
                        ),
                        client.V1Volume(
                            name="ondevice-deployvol",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="pvcnfs-ondevice-deploy"
                            )
                        ),

                        
                    ]
                )
            )
        )
    )
    return deployment



def create_viz2code_deployment_object():
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name="viz2code"),
        spec=client.V1DeploymentSpec(
            selector=client.V1LabelSelector(
                match_labels={"app": "viz2code"}
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": "viz2code"}),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name="viz2code",
                            image="tango_viz2code",
                            image_pull_policy="Never",
                            volume_mounts=[
                                client.V1VolumeMount(
                                    mount_path="/source",
                                    name="viz2codevol"
                                ),
                                client.V1VolumeMount(
                                    mount_path="/shared",
                                    name="sharedvol"
                                )                                            
                            ],
                            ports=[
                                client.V1ContainerPort(container_port=8091)
                            ],
                            command=["/bin/sh", "-c"],
                            args=[
                            "cd /visualization/frontend &&"
                            "npm run build &&"
                            "cd .. &&"
                            "python manage.py makemigrations &&"
                            "python manage.py migrate &&"
                            "python manage.py runserver react 0.0.0.0:8091"
                            ]
                        ),                                                                                       
                                                
                                                
                    ],
                    volumes=[
                        client.V1Volume(
                            name="sharedvol",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="pvcnfs-shared"
                            )
                        ),
                        client.V1Volume(
                            name="viz2codevol",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="pvcnfs-viz2code"
                            )
                        ),                        
                    ]
                )
            )
        )
    )
    return deployment





def create_postgresservice_service_object():
    service = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name="postgresql"),
        spec=client.V1ServiceSpec(
            selector={"app": "postgresql"},
            ports=[client.V1ServicePort(name="postgres-port", port=5432, target_port=5432)]
        )
    )
    return service





def create_projectmanager_service_object():
    service = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name="projectmanager"),
        spec=client.V1ServiceSpec(
            type="NodePort",
            ports=[
                # client.V1ServicePort(port=8085, target_port=8085, node_port=8085)
                client.V1ServicePort(port=8085, target_port=8085, node_port=8085)
            ],
            selector={"app": "projectmanager"}
        )
    )
    return service

"""
labelling
"""

def create_labelling_service_object():
    service = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name="labelling"),
        spec=client.V1ServiceSpec(
            type="NodePort",
            ports=[
                client.V1ServicePort(name="labelling1", port=80, target_port=80, node_port=8086),
                client.V1ServicePort(name="labelling2", port=8095, target_port=8095, node_port=10236)
            ],
            selector={"app": "labelling"}
        )
    )
    return service

"""
bms
"""

def create_bms_service_object():
    service = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name="bms"),
        spec=client.V1ServiceSpec(
            type="NodePort",
            ports=[
                client.V1ServicePort(port=8081, target_port=8081, node_port=8081)
            ],
            selector={"app": "bms"}
        )
    )
    return service
"""
yoloe
"""

def create_autonn_yoloe_service_object():
    service = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name="yoloe"),
        spec=client.V1ServiceSpec(
            type="NodePort",
            ports=[
                client.V1ServicePort(port=8090, target_port=8090, node_port=8090)
            ],
            selector={"app": "yoloe"}
        )
    )
    return service


"""
autonn_resnet
"""
def create_autonn_resnet_service_object():
    service = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name="resnet"),
        spec=client.V1ServiceSpec(
            type="NodePort",
            ports=[
                client.V1ServicePort(port=8092, target_port=8092, node_port=8092)
            ],
            selector={"app": "resnet"}
        )
    )
    return service

"""
code_gen
"""
def create_code_gen_service_object():
    service = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name="codegen"),
        spec=client.V1ServiceSpec(
            type="NodePort",
            ports=[
                client.V1ServicePort(port=8888, target_port=8888, node_port=8888)
            ],
            selector={"app": "codegen"}
        )
    )
    return service

"""
cloud_deploy
"""
def create_cloud_deploy_service_object():
    service = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name="cloud-deploy"),
        spec=client.V1ServiceSpec(
            type="NodePort",
            ports=[
                client.V1ServicePort(name="cloud-deploy1", port=7007, target_port=7007, node_port=7007),
                client.V1ServicePort(name="cloud-deploy2", port=8080, target_port=8080, node_port=8080),
                client.V1ServicePort(name="cloud-deploy3", port=8890, target_port=8890, node_port=8890)
            ],
            selector={"app": "cloud-deploy"}
        )
    )
    return service

"""
ondevice
"""
def create_ondevice_deploy_service_object():
    service = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name="ondevice"),
        spec=client.V1ServiceSpec(
            type="NodePort",
            ports=[
                client.V1ServicePort(port=8891, target_port=8891, node_port=8891)
            ],
            selector={"app": "ondevice"}
        )
    )
    return service


"""
viz2code
"""
def create_viz2code_deploy_service_object():
    service = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name="viz2code"),
        spec=client.V1ServiceSpec(
            type="NodePort",
            ports=[
                client.V1ServicePort(port=8091, target_port=8091, node_port=8091)
            ],
            selector={"app": "viz2code"}
        )
    )
    return service



def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            print(directory)
            os.makedirs(directory)
        else :
            pass
    except OSError as e:
        print(f"Error: Failed to create the directory {e}")


#네임스페이스 설정
def create_namespace(namespace_name):
    config.load_kube_config()
    api_instance = client.CoreV1Api()


    body = client.V1Namespace(metadata=client.V1ObjectMeta(name=namespace_name))

    try:
        api_instance.create_namespace(body)
        print(f"Namespace {namespace_name} created successfully.")

    except client.exceptions.ApiException as e:
        print(f"Exception when creating Namespace: {e}")

def main():
    config.load_kube_config()

    create_namespace("tango")
    api_instance = client.CoreV1Api()
    deploy_api_instance = client.AppsV1Api()  
    
    createDirectory(f"{tango_root_path}TANGO/labelling/dataset")
    createDirectory(f"{tango_root_path}TANGO/labelling/datadb")
    createDirectory(f"{tango_path}share/postgreSQL")
    
    
    service_obj = create_projectmanager_service_object()
    try:
        api_instance.create_namespaced_service(namespace="tango", body=service_obj)
        print(f"projectmanager Service object created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating projectmanager Service object: {e}")
        

    service_obj = create_postgresservice_service_object()
    try:
        api_instance.create_namespaced_service(namespace="tango", body=service_obj)
        print(f"PostgreSQL Service object created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PostgreSQL Service object: {e}")
        
        

    pvc_obj = create_shared_persistent_volume_claim_object()
    try:
        api_instance.create_namespaced_persistent_volume_claim(
            namespace="tango", body=pvc_obj
        )
        print(f"PersistentVolumeClaim projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolumeClaim projectmanager: {e}")
        
    pv_obj = create_shared_persistent_volume_object()
    try:
        api_instance.create_persistent_volume(body=pv_obj)
        print(f"PersistentVolume projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolume projectmanager: {e}")


    pvc_obj = create_postgresql_persistent_volume_claim_object()
    try:
        api_instance.create_namespaced_persistent_volume_claim(
            namespace="tango", body=pvc_obj
        )
        print(f"PersistentVolumeClaim projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolumeClaim projectmanager: {e}")
        

    pv_obj = create_postgresql_persistent_volume_object()
    try:
        api_instance.create_persistent_volume(body=pv_obj)
        print(f"PersistentVolume projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolume projectmanager: {e}")
        
        

    pvc_obj = create_labelling_dataset_persistent_volume_claim_object()
    try:
        api_instance.create_namespaced_persistent_volume_claim(
            namespace="tango", body=pvc_obj
        )
        print(f"PersistentVolumeClaim projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolumeClaim projectmanager: {e}")
        

    pv_obj = create_labelling_dataset_persistent_volume_object()
    try:
        api_instance.create_persistent_volume(body=pv_obj)
        print(f"PersistentVolume projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolume projectmanager: {e}")
        
        

    pvc_obj = create_labelling_datadb_persistent_volume_claim_object()
    try:
        api_instance.create_namespaced_persistent_volume_claim(
            namespace="tango", body=pvc_obj
        )
        print(f"PersistentVolumeClaim projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolumeClaim projectmanager: {e}")
        

    pv_obj = create_labelling_datadb_persistent_volume_object()
    try:
        api_instance.create_persistent_volume(body=pv_obj)
        print(f"PersistentVolume projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolume projectmanager: {e}")
        
        

    pvc_obj = create_projectmanager_persistent_volume_claim_object()
    try:
        api_instance.create_namespaced_persistent_volume_claim(
            namespace="tango", body=pvc_obj
        )
        print(f"PersistentVolumeClaim projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolumeClaim projectmanager: {e}")
        

    pv_obj = create_projectmanager_persistent_volume_object()
    try:
        api_instance.create_persistent_volume(body=pv_obj)
        print(f"PersistentVolume projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolume projectmanager: {e}")
        
        

    pvc_obj = create_bms_persistent_volume_claim_object()
    try:
        api_instance.create_namespaced_persistent_volume_claim(
            namespace="tango", body=pvc_obj
        )
        print(f"PersistentVolumeClaim projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolumeClaim projectmanager: {e}")
        

    pv_obj = create_bms_persistent_volume_object()
    try:
        api_instance.create_persistent_volume(body=pv_obj)
        print(f"PersistentVolume projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolume projectmanager: {e}")
        
        
        
    pvc_obj = create_yoloe_persistent_volume_claim_object()
    try:
        api_instance.create_namespaced_persistent_volume_claim(
            namespace="tango", body=pvc_obj
        )
        print(f"PersistentVolumeClaim projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolumeClaim projectmanager: {e}")
        

    pv_obj = create_yoloe_persistent_volume_object()
    try:
        api_instance.create_persistent_volume(body=pv_obj)
        print(f"PersistentVolume projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolume projectmanager: {e}")
     
                
    pvc_obj = create_resnet_persistent_volume_claim_object()
    try:
        api_instance.create_namespaced_persistent_volume_claim(
            namespace="tango", body=pvc_obj
        )
        print(f"PersistentVolumeClaim projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolumeClaim projectmanager: {e}")
        

    pv_obj = create_resnet_persistent_volume_object()
    try:
        api_instance.create_persistent_volume(body=pv_obj)
        print(f"PersistentVolume projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolume projectmanager: {e}")    
        
        
    pvc_obj = create_code_gen_persistent_volume_claim_object()
    try:
        api_instance.create_namespaced_persistent_volume_claim(
            namespace="tango", body=pvc_obj
        )
        print(f"PersistentVolumeClaim projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolumeClaim projectmanager: {e}")
        

    pv_obj = create_code_gen_persistent_volume_object()
    try:
        api_instance.create_persistent_volume(body=pv_obj)
        print(f"PersistentVolume projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolume projectmanager: {e}")    
        
        
    pvc_obj = create_cloud_deploy_persistent_volume_claim_object()
    try:
        api_instance.create_namespaced_persistent_volume_claim(
            namespace="tango", body=pvc_obj
        )
        print(f"PersistentVolumeClaim projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolumeClaim projectmanager: {e}")
        

    pv_obj = create_cloud_deploy_persistent_volume_object()
    try:
        api_instance.create_persistent_volume(body=pv_obj)
        print(f"PersistentVolume projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolume projectmanager: {e}")        
        
        

    pvc_obj = create_ondevice_deploy_persistent_volume_claim_object()
    try:
        api_instance.create_namespaced_persistent_volume_claim(
            namespace="tango", body=pvc_obj
        )
        print(f"PersistentVolumeClaim projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolumeClaim projectmanager: {e}")
        

    pv_obj = create_ondevice_deploy_persistent_volume_object()
    try:
        api_instance.create_persistent_volume(body=pv_obj)
        print(f"PersistentVolume projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolume projectmanager: {e}")    
        
        
    pvc_obj = create_viz2code_persistent_volume_claim_object()
    try:
        api_instance.create_namespaced_persistent_volume_claim(
            namespace="tango", body=pvc_obj
        )
        print(f"PersistentVolumeClaim projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolumeClaim projectmanager: {e}")
        

    pv_obj = create_viz2code_persistent_volume_object()
    try:
        api_instance.create_persistent_volume(body=pv_obj)
        print(f"PersistentVolume projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolume projectmanager: {e}")  
        





    # service = create_projectmanager_service_object()
    # try:
    #     api_instance.create_namespaced_service(namespace="tango", body=service)
    #     print(f"servive projectmanager created successfully.")
    # except client.exceptions.ApiException as e:
    #     print(f"Exception when creating PersistentVolume projectmanager: {e}")
        
    service = create_labelling_service_object()
    try:
        api_instance.create_namespaced_service(namespace="tango", body=service)
        print(f"servive projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolume projectmanager: {e}")

    service = create_bms_service_object()
    try:
        api_instance.create_namespaced_service(namespace="tango", body=service)
        print(f"servive projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolume projectmanager: {e}")
        
    service = create_autonn_yoloe_service_object()
    try:
        api_instance.create_namespaced_service(namespace="tango", body=service)
        print(f"servive projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolume projectmanager: {e}")
        
    service = create_autonn_resnet_service_object()
    try:
        api_instance.create_namespaced_service(namespace="tango", body=service)
        print(f"servive projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolume projectmanager: {e}")
        
    service = create_code_gen_service_object()
    try:
        api_instance.create_namespaced_service(namespace="tango", body=service)
        print(f"servive projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolume projectmanager: {e}")
        
    service = create_cloud_deploy_service_object()
    try:
        api_instance.create_namespaced_service(namespace="tango", body=service)
        print(f"servive projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolume projectmanager: {e}")
    
    service = create_ondevice_deploy_service_object()
    try:
        api_instance.create_namespaced_service(namespace="tango", body=service)
        print(f"servive projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolume projectmanager: {e}")

    service = create_viz2code_deploy_service_object()
    try:
        api_instance.create_namespaced_service(namespace="tango", body=service)
        print(f"servive projectmanager created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating PersistentVolume projectmanager: {e}")









        
        
        
        
        
        
        
    deployment_obj = create_postgresql_deployment_object()
    try:
        deploy_api_instance.create_namespaced_deployment(namespace="tango", body=deployment_obj)
        print(f"projectmanager Deployment object created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating projectmanager Deployment object: {e}")        
        
        
        

    deployment_obj = create_projectmanager_deployment_object()
    try:
        deploy_api_instance.create_namespaced_deployment(namespace="tango", body=deployment_obj)
        print(f"projectmanager Deployment object created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating projectmanager Deployment object: {e}")
        
    deployment_obj = create_labelling_deployment_object()
    try:
        deploy_api_instance.create_namespaced_deployment(namespace="tango", body=deployment_obj)
        print(f"labelling Deployment object created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating labelling Deployment object: {e}")
        
        
    deployment_obj = create_bms_deployment_object()
    try:
        deploy_api_instance.create_namespaced_deployment(namespace="tango", body=deployment_obj)
        print(f"bms Deployment object created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating bms Deployment object: {e}")
        
    deployment_obj = create_yoloe_deployment_object()
    try:
        deploy_api_instance.create_namespaced_deployment(namespace="tango", body=deployment_obj)
        print(f"yoloe Deployment object created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating yoloe Deployment object: {e}")
        
        
    deployment_obj = create_resnet_deployment_object()
    try:
        deploy_api_instance.create_namespaced_deployment(namespace="tango", body=deployment_obj)
        print(f"projectmanager Deployment object created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating projectmanager Deployment object: {e}")
        
        
    deployment_obj = create_codegen_deployment_object()
    try:
        deploy_api_instance.create_namespaced_deployment(namespace="tango", body=deployment_obj)
        print(f"codegen Deployment object created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating codegen Deployment object: {e}")
        
        
    deployment_obj = create_cloud_deploy_deployment_object()
    try:
        deploy_api_instance.create_namespaced_deployment(namespace="tango", body=deployment_obj)
        print(f"cloud_deploy Deployment object created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating cloud_deploy Deployment object: {e}")
        
        
    deployment_obj = create_ondevice_deployment_object()
    try:
        deploy_api_instance.create_namespaced_deployment(namespace="tango", body=deployment_obj)
        print(f"ondevice Deployment object created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating ondevice Deployment object: {e}")
        
        
    deployment_obj = create_viz2code_deployment_object()
    try:
        deploy_api_instance.create_namespaced_deployment(namespace="tango", body=deployment_obj)
        print(f"viz2code Deployment object created successfully.")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating viz2code Deployment object: {e}")
        
        


if __name__ == "__main__":
    main()