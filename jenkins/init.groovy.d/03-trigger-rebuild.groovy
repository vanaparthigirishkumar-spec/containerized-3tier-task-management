// One-shot trigger for a rebuild after fixing the Jenkinsfile post step.
import jenkins.model.Jenkins

def jenkins = Jenkins.instance
def job = jenkins.getItemByFullName('containerized-3tier-task-management')
def marker = new File(jenkins.rootDir, 'trigger-rebuild-3')
if (job != null && !marker.exists()) {
    marker.text = new Date().toString()
    println "Rebuild3: scheduling build of ${job.name}"
    job.scheduleBuild2(0)
} else {
    println "Rebuild3: skipped (job missing or already triggered)"
}
