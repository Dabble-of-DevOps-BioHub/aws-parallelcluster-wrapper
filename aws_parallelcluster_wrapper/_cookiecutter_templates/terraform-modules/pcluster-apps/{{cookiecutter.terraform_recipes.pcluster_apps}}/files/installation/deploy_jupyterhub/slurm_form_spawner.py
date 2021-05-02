import shlex

import batchspawner
from jupyterhub.spawner import LocalProcessSpawner

from traitlets import (
    Integer, Unicode, Float, Dict, default
)

class SlurmFormSpawner(batchspawner.SlurmSpawner):

    def _options_form_default(self):

        defaults = {
            'req_nprocs': c.BatchSpawnerBase.req_nprocs,
            'req_memory': c.BatchSpawnerBase.req_memory,
            'req_runtime': c.BatchSpawnerBase.req_runtime,
            'req_partition': c.BatchSpawnerBase.req_partition,
            'req_options': c.BatchSpawnerBase.req_options,
        }

        return """
<div class="form-group">
    <label for="partition">Partition</label>
    <input type="text" class="form-control" value="{req_partition}" placeholder="{req_partition}" id="partition" name="req_partition"/>
</div>
<div class="form-group">
    <label for="cpus">CPUs per task (--cpus-per-task) </label>
    <input type="text" class="form-control" value="{req_nprocs}" placeholder="{req_nprocs}" id="cpus" name="req_nprocs"/>
</div>
<div class="form-group">
    <label for="mem">Memory (--mem)</label>
    <input type="text" class="form-control" value="{req_memory}" placeholder="{req_memory}" id="mem" name="req_memory"/>
</div>
<div class="form-group">
    <label for="runtime">Runtime (--time)</label>
    <input type="text" class="form-control" value="{req_runtime}" placeholder="{req_runtime}" id="runtime" name="req_runtime"/>
</div>
<div class="form-group">
    <label for="runtime">Options (additional options such as --constraint=m4.10xlarge)</label>
    <input type="text" class="form-control" value="{req_options}" placeholder="{req_options}" id="constraint" name="req_options"/>
</div>
        """.format(
            **defaults
        )

    def options_from_form(self, formdata):
        options = {}

        self.log.debug(formdata)
        submission_data = {}
        for key in formdata.keys():
            form_value = formdata.get(key, [''])
            if not form_value[0]:
                form_value[0] = c.BatchSpawnerBase[key]

            submission_data[key] = form_value[0]

        self.log.debug(submission_data)

        for key in submission_data.keys():
            setattr(self, key, submission_data[key])

        return options


# c.JupyterHub.spawner_class = SlurmFormSpawner
