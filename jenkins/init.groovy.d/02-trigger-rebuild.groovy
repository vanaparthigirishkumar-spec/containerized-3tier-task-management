// One-shot trigger for a rebuild after fixing the venv permissions.
import jenkins.model.Jenkins

def jenkins = Jenkins.instance
def job = jenkins.getItemByFullName('containerized-3tier-task-management')
def marker = new File(jenkins.rootDir, 'trigger-rebuild-2')
if (job != null && !marker.exists()) {
    marker.text = new Date().toString()
    println "Rebuild: scheduling build of ${job.name}"
    job.scheduleBuild2(0)
} else {
    println "Rebuild: skipped (job missing or already triggered)"
}
