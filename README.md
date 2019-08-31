# pytest-kind

Test your Python Kubernetes app/operator end-to-end with [kind](https://kind.sigs.k8s.io/) and [pytest](https://pytest.org).

`pytest-kind` is a plugin for pytest which provides the `kind_cluster` fixture.
The fixture will install kind, create a cluster, and provide convenience functionality such as port forwarding.

## Usage

Install `pytest-kind` via pip or via poetry, e.g.:

```
poetry add --dev pytest-kind
```

Write your pytest functions and use the provided `kind_cluster` fixture, e.g.:

```
def test_kubernetes_version(kind_cluster):
    assert kind_cluster.api.version == ('1', '15')
```

To load your custom Docker image and apply deployment manifests:

```
from pykube import Pod

def test_myapp(kind_cluster):
    kind_cluster.load_docker_image("myapp")
    kind_cluster.kubectl("apply", "-f", "deployment.yaml")
    kind_cluster.kubectl("rollout", "status", "deployment/myapp")

    # using Pykube to query pods
    for pod in Pod.objects(kind_cluster.api).filter(selector="app=myapp"):
        assert "Sucessfully started" in pod.logs()
```

See the `examples` directory for sample projects.

## Pytest Options

The kind cluster name can be set via the `--cluster-name` CLI option.

The kind cluster is deleted after each pytest session, you can keep the cluster by passing `--keep-cluster` to pytest.
