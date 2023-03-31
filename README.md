# Command and Control

## Requirements
* python version >= 3.7

## Install dependencies
1. In the server project directory, and in the CLI project directory, run
    ```cmd
   pip install -r requirements.txt
   ```

## Start application

1. Start CLI
   
2. Start agents

## Add command option
Edit `server/commands.yaml`. Add a command in the following format:
```yaml
1:
  command: hostname
  description: Get machine name
  accept_args: false
  force_args: false
```
Params explanation:
* command: string - The actual command to run in the terminal
* description: string - Description of command
* accept_args: boolean - The command may have args
* force_args: boolean - If `accept_args` is True, force sending args