
from prefect.deployments import Deployment
# import the parent flow from the original flow to be deployed
import sys
sys.path.append('../extraction_aws')
from parameterized_extract_to_s3_docker import extract_to_s3_parent_flow


#The code below was copied from Prefect UI block section
from prefect.infrastructure.container import DockerContainer
docker_container_block = DockerContainer.load("zoomcamp-prefect-container")

docker_dep = Deployment.build_from_flow(
    flow=extract_to_s3_parent_flow,
    name='docker-deployment-flow',
    infrastructure=docker_container_block,
)

if __name__ == "__main__":
    docker_dep.apply()