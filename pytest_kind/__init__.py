"""
kind:
    curl -Lo ./kind https://github.com/kubernetes-sigs/kind/releases/download/v0.5.0/kind-$(OSNAME)-amd64
    chmod +x ./kind

kubectl:
    curl -LO https://storage.googleapis.com/kubernetes-release/release/$$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/$(OSNAME)/amd64/kubectl
    chmod +x ./kubectl
"""

