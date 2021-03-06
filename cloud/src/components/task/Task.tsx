import React from 'react'
import TaskLog from './TaskLog'
import TaskStatus from './TaskStatus'
import TaskError from './TaskError'
import TaskResult from './TaskResult'
import TaskLink from './TaskLink'
import TaskInputs from './TaskInputs'
import TaskSubTasks from './TaskSubTasks'
import { TaskHeader, TaskHeaderLink, TaskImage, TaskWrapper, ParentWrapper, TaskTitleWrapper, TaskCreatedAt, TaskTitle } from './styled/Task'
import { Task as TaskInterface } from '../../store/tasks/types'

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { formatDate } from '../../utils'

type TaskProps = TaskInterface & {
    maxLogHeight?: number
}

export type TaskComponent = React.FC<TaskProps>

export const Task: TaskComponent = ({ id, status, image, parent, result, error, sub_tasks, inputs, maxLogHeight, created_at }) => {
    return <TaskWrapper>
        <TaskHeader>
            <TaskTitleWrapper>
                <TaskTitle>
                    <TaskHeaderLink to={`/task/${id}`}>{id}</TaskHeaderLink> 
                    <TaskStatus status={status} />
                </TaskTitle>
                <TaskCreatedAt>{formatDate(created_at)}</TaskCreatedAt>
            </TaskTitleWrapper>
            <TaskImage>{image}</TaskImage>
            {parent && <ParentWrapper>
                <FontAwesomeIcon icon="level-up-alt" />
                <TaskLink id={parent}/>
            </ParentWrapper>}
        </TaskHeader>

        <TaskError error={error} />
        <TaskInputs inputs={inputs} />
        <TaskSubTasks sub_tasks={sub_tasks} />
        <TaskLog id={id} maxHeight={maxLogHeight} />
        <TaskResult result={result} />
    </TaskWrapper>
}

export default Task