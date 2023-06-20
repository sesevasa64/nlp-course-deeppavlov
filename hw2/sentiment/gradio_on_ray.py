from .gradio_interface import create_demo
from ray.serve.gradio_integrations import GradioServer


deployment = GradioServer.options(ray_actor_options={"num_cpus": 4})
app = deployment.bind(create_demo)
