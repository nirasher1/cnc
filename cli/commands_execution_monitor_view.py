from tabulate import tabulate

TABLE_HEADER_CELLS = ['Execution ID ', 'Command', 'Status', 'Output']


class CommandsExecutionMonitorView:
    """Render server's execution monitor"""

    def __init__(self, io, commands_execution_monitor):
        self.__io = io
        self.__commands_execution_monitor = commands_execution_monitor
        self.__executions = commands_execution_monitor.get_executions()
        self.__statuses = commands_execution_monitor.get_statuses()

    def show(self):
        table = []
        for exec_id, command_execution in self.__executions.items():
            exec_status = self.__statuses[exec_id]
            command_display = command_execution.get_payload()
            if command_execution.get_payload_args():
                command_display += ' ' + ' '.join(command_execution.get_payload_args())
            row = [exec_id, command_display, exec_status.get_status().value, exec_status.get_message()]
            table.append(row)

        self.__io.print(tabulate(table, headers=TABLE_HEADER_CELLS, tablefmt='github'))
