import logging
import os
import pykube
import pytest
import requests
import subprocess
import sys

from pathlib import Path


KIND_VERSION = "v0.5.1"


class KindCluster:
    def __init__(self, name: str):
        self.name = name
        path = Path(".pytest-kind")
        self.path = path / name
        self.path.mkdir(parents=True, exist_ok=True)
        self.kind_path = self.path / "kind"
        self.kubectl_path = self.path / "kubectl"

    def ensure_kind(self):
        if not self.kind_path.exists():
            osname = sys.platform  # "linux" or "darwin"
            url = os.getenv(
                "KIND_DOWNLOAD_URL",
                f"https://github.com/kubernetes-sigs/kind/releases/download/{KIND_VERSION}/kind-{osname}-amd64",
            )
            logging.info(f"Downloading {url}..")
            tmp_file = self.kind_path.with_suffix(".tmp")
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with tmp_file.open("wb") as fd:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            fd.write(chunk)
            tmp_file.chmod(0o755)
            tmp_file.rename(self.kind_path)

    def create(self):
        self.ensure_kind()

        cluster_exists = False
        out = subprocess.check_output(
            [str(self.kind_path), "get", "clusters"], encoding="utf-8"
        )
        for name in out.splitlines():
            if name == self.name:
                cluster_exists = True

        if not cluster_exists:
            logging.info(f"Creating cluster {self.name}..")
            subprocess.run(
                [str(self.kind_path), "create", "cluster", f"--name={self.name}"],
                check=True,
            )
        self.kubeconfig_path = subprocess.check_output(
            [str(self.kind_path), "get", "kubeconfig-path", f"--name={self.name}"],
            encoding="utf-8",
        ).strip()

        config = pykube.KubeConfig.from_file(self.kubeconfig_path)
        self.api = pykube.HTTPClient(config)

    def delete(self):
        subprocess.run(
            [str(self.kind_path), "delete", "cluster", f"--name={self.name}"],
            check=True,
        )


@pytest.fixture(scope="module")
def kind_cluster(request):
    name = getattr(request.module, "kind_cluster_name", "pytest-kind")
    cluster = KindCluster(name)
    cluster.create()
    yield cluster
    cluster.delete()
