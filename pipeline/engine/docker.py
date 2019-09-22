import docker
from pipeline.tasks import Task, TaskContext, TaskDefinition
from .cluster import ClusterProvider


class DockerTask(Task):
    def __init__(self, cluster: ClusterProvider, taskdef: TaskDefinition, container):
        super().__init__(TaskContext(
            cluster=cluster,
            taskdef=taskdef,
            node=None,
        ))
        self.container = container



class DockerProvider(ClusterProvider):
    def __init__(self, args = { }):
        super().__init__('docker', args)
        self.docker = docker.from_env()
        self.tasks = { }


    def spawn(self, taskdef: TaskDefinition):
        container = self.docker.containers.run(
            detach      = True,
            image       = taskdef.image,
            name        = taskdef.id,
            hostname    = taskdef.id,
            network     = 'tasks',
            environment = self.create_env(taskdef),
            volumes     = {
                '/var/run/docker.sock': {
                    'bind': '/var/run/docker.sock', 
                    'mode': 'ro',
                },
            },
            labels = {
                'task_id': taskdef.id,
                'task_parent_id': taskdef.parent_id,
            },
        )
        print('~~ Spawned docker container with id', container.id[:12])
        return DockerTask(self, taskdef, container)


    def find_child_containers(self, parent_id: str) -> list:
        return self.docker.containers.list(
            filters={
                'label': f'task_parent_id={parent_id}',
            },
        )


    def destroy_children(self, parent_id: str) -> list:
        print('~~ docker: destroy children of', parent_id)
        tasks = [ ]
        children = self.find_child_containers(parent_id)
        for child in children:
            tasks += self.destroy(child.labels['task_id'])
        return tasks


    def destroy(self, task_id):
        def kill_family(container):
            kills = [ ]
            container_task_id = container.labels['task_id']
            print('~~ docker: kill', container_task_id, '->', container.id[:12])

            children = self.find_child_containers(container_task_id)
            print('~~ docker:', task_id, 'children:', children)
            for child in children:
                kills += kill_family(child)

            try:
                container.remove(force=True)
            except docker.errors.NotFound:
                print('~~ docker: kill: task', task_id, 'container not found:', container.id[:12])

            kills.append(task_id)

        print('~~ docker: destroy', task_id)
        container = self.docker.containers.get(task_id)
        return kill_family(container)


    def logs(self, task: DockerTask):
        for log in task.container.logs(stream=True):
            if log[-1] == 10: # newline
                log = log[:-1]
            yield str(log, encoding='utf-8')


    def wait(self, task: DockerTask):
        pass