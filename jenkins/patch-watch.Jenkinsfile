// Watches for a new Wardogs build and runs the patch update pipeline on it (docs/UPDATE_PIPELINE.md#running-it-from-jenkins).
// Runs on the lead's PC through the agent labelled `wardogs`. It only reads the game files: it never starts or stops
// the game, never pushes, and stops for a human when the usmap is stale.
pipeline {
    agent { label 'wardogs' }

    triggers { cron('H */3 * * *') }

    options {
        disableConcurrentBuilds()
        skipDefaultCheckout()   // the pipeline runs from the main checkout, which owns the update-<label> branches
        buildDiscarder(logRotator(numToKeepStr: '60'))
    }

    parameters {
        string(name: 'LABEL', defaultValue: '', description: 'Label for the new build. Empty: <SEASON>-<Steam build id>.')
    }

    environment {
        MAIN_CHECKOUT = 'E:/Reverse_Engineer/wardogs_analysis/data_docs_clone/wardogs-data-docs'
        STEAM_MANIFEST = 'E:/Steam/steamapps/appmanifest_1867240.acf'
        SEASON = 's2'   // label prefix for automatic runs; change it when a new season starts
        PYTHONUTF8 = '1'
    }

    stages {
        stage('Check for a new build') {
            steps {
                script {
                    if (powershell(returnStatus: true, script: 'if (Get-Process -Name "Wardogs*" -ErrorAction SilentlyContinue) { exit 1 }') != 0) {
                        skip('Wardogs is running')
                        return
                    }
                    def acf = powershell(returnStdout: true, script: 'Get-Content -Raw $env:STEAM_MANIFEST')
                    // StateFlags 4 means fully installed; anything else is a download or update in progress.
                    if (acfValue(acf, 'StateFlags') != '4') {
                        skip('Steam is still updating Wardogs')
                        return
                    }
                    def rc = pipelineCommand('status')
                    if (rc == 0) {
                        skip('no new build')
                        return
                    }
                    if (rc != 10) {
                        error("update_pipeline.py status failed with exit code ${rc}")
                    }
                    env.NEW_LABEL = params.LABEL ?: "${env.SEASON}-${acfValue(acf, 'buildid')}"
                }
            }
        }

        stage('Run the update pipeline') {
            when { expression { env.NEW_LABEL } }
            steps {
                script {
                    currentBuild.description = env.NEW_LABEL
                    def label = env.NEW_LABEL
                    def report = "${buildsRoot()}/${label}/regen-report.md"
                    def rc = pipelineCommand("run --label \"${label}\" --assets")
                    if (rc == 0) {
                        currentBuild.description = "${label}: branch update-${label} ready to review"
                    } else if (rc == 3) {
                        currentBuild.description = "${label}: stale usmap"
                        error("The usmap is stale. Regenerate it with Dumper-7 (docs/UPDATE_PIPELINE.md#stale-usmap), then run: " +
                              "python -I _tools/update_pipeline.py run --label ${label} --assets --force")
                    } else if (rc in [1, 4] && fileExists(report)) {
                        // The worktree and reports exist; some generators or checks failed and need a look.
                        currentBuild.description = "${label}: review generator/check failures"
                        unstable("update_pipeline.py run finished with exit code ${rc}: see regen-report.md")
                    } else {
                        error("update_pipeline.py run failed with exit code ${rc}")
                    }
                }
            }
            post {
                always {
                    script {
                        def dir = "${buildsRoot()}/${env.NEW_LABEL}"
                        powershell """
                            New-Item -ItemType Directory -Force reports | Out-Null
                            foreach (\$f in 'patch-diff.md', 'regen-report.md', 'extract-meta.json') {
                                \$p = Join-Path '${dir}' \$f
                                if (Test-Path \$p) { Copy-Item \$p reports/ }
                            }
                        """
                    }
                    archiveArtifacts artifacts: 'reports/*', allowEmptyArchive: true
                }
            }
        }
    }
}

def skip(String reason) {
    echo "Skipped: ${reason}."
    currentBuild.description = reason
    currentBuild.result = 'NOT_BUILT'
}

// Runs a sub-command of the main checkout's update_pipeline.py and returns its exit code.
def pipelineCommand(String args) {
    return powershell(returnStatus: true, script: "python -I \"\$env:MAIN_CHECKOUT/_tools/update_pipeline.py\" ${args}; exit \$LASTEXITCODE")
}

// The same override the pipeline itself honours.
def buildsRoot() {
    return env.WD_PIPELINE_BUILDS_ROOT ?: 'E:/wardogs_builds'
}

@NonCPS
def acfValue(String acf, String key) {
    def m = acf =~ /"${key}"\s+"([^"]*)"/
    return m.find() ? m.group(1) : null
}
