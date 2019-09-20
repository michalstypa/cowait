from .definition import TaskDefinition


def test_taskdef_serialization():
    sample = {
        'id':        'lazy-kcjvnrsg',
        'image':     'pipeline/task:lazy', 
        'name':      'lazy', 
        'parent':    'root', 
        'namespace': 'default', 
        'config':    { }, 
        'env':       { }, 
        'meta':      { },
        'inputs':    { }, 
    }

    taskdef = TaskDefinition.deserialize(sample)
    output = taskdef.serialize()
    assert sample == output


def test_taskdef_default_id():
    """ Task definitions should be assigned an autogenerated ID if none is provided. """
    taskdef = TaskDefinition(
        name='test',
        image='image',
    )
    assert isinstance(taskdef.id, str)


def test_taskdef_input_id():
    """ Task definitions can be passed an ID """
    taskdef = TaskDefinition(
        id='123',
        name='test',
        image='image',
    )
    assert taskdef.id == '123'