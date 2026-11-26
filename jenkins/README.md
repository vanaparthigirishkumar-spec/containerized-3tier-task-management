# Local Jenkins Setup Guide

Jenkins is running in Docker, separately from the application stack.

## Current runtime

- **URL:** http://localhost:8081
- **Bound to:** `127.0.0.1` only (not public)
- **Container:** `jenkins` (Jenkins LTS, JDK 21)
- **Build service:** `jenkins-dind` (Docker-in-Docker with TLS, no host Docker socket)
- **Initial admin password:** `45c3c673d84744bd88c7410fa0440be8`
  - Also available with: `docker compose exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword`

Port 8081 is used because port 8080 is occupied by a container from another project on this machine.

## Start / stop

```bash
cd jenkins
JENKINS_HTTP_PORT=8081 docker compose up -d
JENKINS_HTTP_PORT=8081 docker compose ps
JENKINS_HTTP_PORT=8081 docker compose stop
```

## Initial setup (must be done in your browser)

1. Open http://localhost:8081.
2. Paste the initial admin password above.
3. Choose **Install suggested plugins** (the required plugins are already baked into the image, so this is quick).
4. Create your own admin user with your own password.
5. Set the Jenkins URL to `http://localhost:8081/`.
6. Click **Save and Finish**, then **Start using Jenkins**.

No administrator password is hardcoded in any file.

## Create the Pipeline job

1. **New Item** → name it `containerized-3tier-task-management` → select **Pipeline** → OK.
2. Check **GitHub project** and enter:
   `https://github.com/vanaparthigirishkumar-spec/containerized-3tier-task-management`
3. Under **Pipeline**, choose **Pipeline script from SCM**.
4. SCM: **Git**. Repository URL:
   `https://github.com/vanaparthigirishkumar-spec/containerized-3tier-task-management.git`
5. Branch specifier: `*/main`
6. Script path: `Jenkinsfile`
7. Save, then click **Build Now**.

The repository is public, so no GitHub credentials are required for checkout. The pipeline runs on demand (manual trigger) — there is no public webhook and no automatic deployment.

## Notes

- The Jenkinsfile runs tests from the repository root (`python -m pytest tests -v`) because `tests/` lives at the root.
- Docker builds go to the isolated DinD daemon via TLS (`tcp://docker:2376`). The host Docker socket is never mounted.
- Application data (the `postgres_data` volume) is never touched by Jenkins.
