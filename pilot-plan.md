# Historical CRL pilot experiments

The current collaboration direction uses GitHub and does not depend on the Tokyo VM. No hosted endpoint is required to read, review, or prepare a contribution. The deployment scripts in this repository are historical experiment artifacts, not current setup instructions.

The earlier pilot used a loopback-only HTTP service and synthetic signed CLAIM, CHALLENGE, and REVISION events. A later experiment transferred their dispute context between two service processes on the same machine. These experiments tested agent signatures, local persistence, and preservation of a later challenge in a declared snapshot. They did not establish independent fault domains, public registration, WebAuthn ownership, delegation, revocation, censorship resistance, or improved scientific discovery.

Run the local examples and tests described in [README.md](README.md) to exercise the prototype without cloud infrastructure. Real mathematical contributions follow the proposed [GitHub contribution guide](CONTRIBUTING.md), subject to attribution and publication rights for the exact artifacts.
