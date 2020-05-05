import os
from cowait.tasks import TaskDefinition
from cowait.engine import ProviderError, TaskCreationError
from ..context import CowaitContext
from ..utils import ExitTrap, get_context_cluster, printheader
from .build import build as run_build
from .push import push as run_push


def test(
    provider: str,
    push: bool,
):
    try:
        context = CowaitContext.open()
        cluster = get_context_cluster(context, provider)

        if push:
            run_push()
        else:
            run_build()

        # execute the test task within the current image
        task = cluster.spawn(TaskDefinition(
            name='cowait.test',
            image=context.get_image_name(),
        ))

        def destroy(*args):
            print()
            printheader('interrupt')
            cluster.destroy(task.id)
            os._exit(1)

        with ExitTrap(destroy):
            # capture & print logs
            logs = cluster.logs(task)
            printheader('task output')
            for log in logs:
                print(log, flush=True)

    except TaskCreationError as e:
        printheader('error')
        print('Error creating task:', str(e))

    except ProviderError as e:
        printheader('error')
        print('Provider error:', str(e))

    finally:
        printheader()
