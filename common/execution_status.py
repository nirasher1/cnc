from enum import Enum, unique


@unique
class ExecutionStatus(Enum):
    RECEIVED = 'received'
    INITIALIZED = 'initialized'
    RUNNING = 'running'
    FINISHED = 'finished'
    ERROR = 'error'

