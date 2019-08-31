import logging
import os
import pykube
import pytest
import requests
import subprocess
import sys

from pathlib import Path

from .cluster import KindCluster


@pytest.fixture(scope="session")
def kind_cluster(request):
    name = request.config.getoption("cluster_name")
    keep = request.config.getoption("keep_cluster")
    cluster = KindCluster(name)
    cluster.create()
    yield cluster
    if not keep:
        cluster.delete()


def pytest_addoption(parser):
    group = parser.getgroup("kind")
    group.addoption(
        "--cluster-name",
        default="pytest-kind",
        help="Name of the Kubernetes kind cluster",
    )
    group.addoption(
        "--keep-cluster",
        action="store_true",
        help="Keep the Kubernetes kind cluster (do not delete after test run)",
    )
