// Bootstrap the Pipeline job for the Containerized 3-Tier project.
// Init scripts run with full Jenkins privileges at startup, so no API token
// or hardcoded password is needed. A marker file ensures the build is
// triggered only once.
import jenkins.model.Jenkins
import org.jenkinsci.plugins.workflow.job.WorkflowJob
import org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition
import hudson.plugins.git.GitSCM
import hudson.plugins.git.UserRemoteConfig
import hudson.plugins.git.BranchSpec
import hudson.plugins.git.SubmoduleConfig
import hudson.plugins.git.extensions.GitSCMExtension

def jenkins = Jenkins.instance
def jobName = 'containerized-3tier-task-management'
def repoUrl = 'https://github.com/vanaparthigirishkumar-spec/containerized-3tier-task-management.git'

def job = jenkins.getItem(jobName)
if (job == null) {
    job = jenkins.createProject(WorkflowJob.class, jobName)
    println "Bootstrap: created job ${jobName}"
} else {
    println "Bootstrap: job ${jobName} already exists, updating definition"
}

def remote = new UserRemoteConfig(repoUrl, null, null, null)
def branches = Collections.singletonList(new BranchSpec('*/main'))
def scm = new GitSCM(
    Collections.singletonList(remote),
    branches,
    false,
    Collections.<SubmoduleConfig>emptyList(),
    null,
    null,
    Collections.<GitSCMExtension>emptyList()
)

job.setDefinition(new CpsScmFlowDefinition(scm, 'Jenkinsfile'))
job.save()
println "Bootstrap: configured Jenkinsfile from SCM (branch */main)"

def marker = new File(jenkins.rootDir, 'bootstrap-build-triggered')
if (!marker.exists()) {
    marker.text = new Date().toString()
    println "Bootstrap: scheduling build #1 of ${jobName}"
    job.scheduleBuild2(0)
} else {
    println "Bootstrap: build already triggered previously, skipping"
}
