class CommandsExecutionMonitor:
    def __init__(self):
        self.__executions = {}
        self.__statuses = {}

    def update_execution_status(self, execution):
        self.__statuses[execution.get_exec_id()] = execution

    def get_executions(self):
        return self.__executions

    def get_statuses(self):
        return self.__statuses



